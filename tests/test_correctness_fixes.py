"""Regression tests for the Phase 6 correctness batch.

Each class here pins a bug that was reachable from normal use. They live
together rather than scattered across the per-module files so the batch is
reviewable as a unit, and so that a future refactor that reintroduces one fails
with an obvious name.
"""

import io

import pytest
import responses

from route4me import Route4Me
from route4me._api_method import make_request
from route4me.api_endpoints import BATCH_GEOCODER, ROUTE_HOST, SINGLE_GEOCODER
from route4me.exceptions import ParamValueException

ROUTE_ID = "5B1E0EFBB8FF6D3A2F6F0BD2C0E60E1E"


class TestDeleteRouteErrorHandler:
    """``Route.delete_route`` had ``except AttributeError: return response.errors``.

    A dict has no ``.errors`` attribute, so whenever the payload was not the
    expected ``{"deleted": ...}`` envelope the *handler itself* raised
    ``AttributeError`` -- replacing the API's response with an exception from
    inside the SDK.

    Note this is ``delete_route`` (singular). ``delete_routes`` (plural) takes a
    list, comma-joins it, and returns the raw payload; it never had this bug.
    """

    def test_the_deleted_envelope_is_unwrapped(self, client, mocked):
        mocked.add(responses.DELETE, ROUTE_HOST, json={"deleted": True}, status=200)

        assert client.route.delete_route(route_id=ROUTE_ID) is True

    def test_an_unexpected_payload_is_returned_not_raised(self, client, mocked):
        mocked.add(responses.DELETE, ROUTE_HOST, json={"status": "queued"}, status=200)

        assert client.route.delete_route(route_id=ROUTE_ID) == {"status": "queued"}

    def test_a_list_payload_is_returned_not_raised(self, client, mocked):
        mocked.add(responses.DELETE, ROUTE_HOST, json=[ROUTE_ID], status=200)

        assert client.route.delete_route(route_id=ROUTE_ID) == [ROUTE_ID]

    def test_an_api_error_still_returns_the_error_dict(self, client, mocked):
        mocked.add(responses.DELETE, ROUTE_HOST, json={"errors": ["nope"]}, status=400)

        assert client.route.delete_route(route_id=ROUTE_ID) == {"errors": ["nope"]}

    def test_a_missing_route_id_raises(self, client):
        with pytest.raises(ParamValueException):
            client.route.delete_route()

    def test_delete_routes_plural_comma_joins_its_ids(self, client, mocked, query_of, last_request):
        mocked.add(responses.DELETE, ROUTE_HOST, json={"deleted": True}, status=200)

        client.route.delete_routes(route_id=[ROUTE_ID, "SECOND"])

        assert query_of(last_request())["route_id"] == f"{ROUTE_ID},SECOND"


class TestBatchFixGeocodesReturnOrder:
    """``address.py``'s error path returned its two values in the wrong order.

    Success returned ``(geocoding_error, addresses)``; the ``JSONDecodeError``
    path returned ``(addresses, [])``. A caller unpacking
    ``errors, addresses = batch_fix_geocodes(...)`` therefore got its addresses
    bound to ``errors`` and an empty list of addresses -- silently, with no
    exception.
    """

    ADDRESSES = [
        {"address": "754 5th Ave New York, NY 10019"},
        {"address": "717 5th Ave New York, NY 10022"},
    ]

    def test_the_success_path_order(self, client, mocked):
        mocked.add(
            responses.POST,
            BATCH_GEOCODER,
            json=[
                {"original": "754 5th Ave New York, NY 10019", "lat": 40.76, "lng": -73.97},
                {"original": "717 5th Ave New York, NY 10022", "lat": 40.77, "lng": -73.96},
            ],
            status=200,
        )

        errors, addresses = client.address.batch_fix_geocodes(list(self.ADDRESSES))

        assert errors == []
        assert len(addresses) == 2
        assert addresses[0]["lat"] == 40.76

    def test_the_error_path_uses_the_same_order(self, client, mocked):
        """A non-JSON body means the whole batch failed, so every address is an
        error -- but ``addresses`` must still be in the second slot."""
        mocked.add(responses.POST, BATCH_GEOCODER, body="<html>502</html>", status=200)

        errors, addresses = client.address.batch_fix_geocodes(list(self.ADDRESSES))

        assert len(errors) == 2, "the failed addresses belong in the first slot"
        assert len(addresses) == 2, "the addresses belong in the second slot"


class TestFixGeocodeBackoff:
    """``fix_geocode`` slept ``random.randrange(1, 5) * 0.5`` -- uniform, so it
    did not actually back off under sustained failure. It now uses the same
    exponential-with-jitter policy as the transport."""

    def test_it_returns_no_error_on_success(self, client, mocked):
        mocked.add(responses.GET, SINGLE_GEOCODER, json={"lat": 40.76, "lng": -73.97}, status=200)

        error, address = client.address.fix_geocode({"address": "754 5th Ave"})

        assert error is None
        assert address["lat"] == 40.76

    def test_delays_grow_exponentially(self, client, mocked, monkeypatch):
        import requests as requests_lib

        slept = []
        monkeypatch.setattr("route4me.address.time.sleep", slept.append)
        monkeypatch.setattr(
            client.address,
            "get_geocode",
            lambda params: (_ for _ in ()).throw(requests_lib.exceptions.ConnectionError()),
        )

        error, _ = client.address.fix_geocode({"address": "754 5th Ave"}, max_attempts=4)

        assert error is not None, "an exhausted retry must report the address as failed"
        assert len(slept) == 3
        # Each wait is larger than the last, jitter notwithstanding (+/-20%
        # cannot close a 2x gap).
        assert slept[0] < slept[1] < slept[2]

    def test_it_reports_the_address_as_the_error_when_exhausted(self, client, monkeypatch):
        import requests as requests_lib

        monkeypatch.setattr("route4me.address.time.sleep", lambda _: None)
        monkeypatch.setattr(
            client.address,
            "get_geocode",
            lambda params: (_ for _ in ()).throw(requests_lib.exceptions.ConnectionError()),
        )
        payload = {"address": "754 5th Ave"}

        error, address = client.address.fix_geocode(payload, max_attempts=2)

        assert error is address is payload


class TestValidateParamsDoesNotMaskBugs:
    """``base.py`` wrapped the *setter call* in ``except AttributeError``, so a
    genuine ``AttributeError`` from inside a setter was reported as
    ``ParamValueException(name, "Not supported")`` -- an SDK bug disguised as an
    unsupported-parameter message."""

    def test_an_unknown_name_is_still_reported_as_unsupported(self, client):
        with pytest.raises(ParamValueException) as excinfo:
            client.optimization.validate_params(definitely_not_a_field=1)

        assert excinfo.value.param == "definitely_not_a_field"
        assert excinfo.value.get_msg() == "Not supported"

    def test_a_non_callable_attribute_is_rejected_clearly(self, client):
        """``params`` is a dict on ``Base``, not a setter."""
        with pytest.raises(ParamValueException) as excinfo:
            client.optimization.validate_params(params={})

        assert excinfo.value.get_msg() == "Not a settable parameter"

    def test_a_validation_failure_still_raises_param_value_exception(self, client):
        with pytest.raises(ParamValueException) as excinfo:
            client.optimization.validate_params(route_name=12345)

        assert excinfo.value.param == "route_name"

    def test_an_attribute_error_from_inside_a_setter_is_not_swallowed(self, client, monkeypatch):
        """The core of the fix: this must surface as itself, not as
        "Not supported"."""

        class Boom:
            def __call__(self, value):
                raise AttributeError("bug inside the setter")

        monkeypatch.setattr(type(client.optimization), "route_name", Boom(), raising=False)

        with pytest.raises(AttributeError, match="bug inside the setter"):
            client.optimization.validate_params(route_name="x")


class TestMakeRequestRequiredValidation:
    """``_api_method`` had ``params if body is None else params`` -- identical
    branches, a leftover from a refactor."""

    def test_required_params_are_validated_against_params(self, client, mocked):
        mocked.add(responses.GET, ROUTE_HOST, json={}, status=200)

        with pytest.raises(ParamValueException):
            make_request(client.route, ROUTE_HOST, "get", {"api_key": "k"}, required=["route_id"])

    def test_it_passes_when_the_requirement_is_met(self, client, mocked):
        mocked.add(responses.GET, ROUTE_HOST, json={"ok": True}, status=200)

        result = make_request(client.route, ROUTE_HOST, "get", {"route_id": ROUTE_ID}, required=["route_id"])

        assert result == {"ok": True}

    def test_a_body_does_not_change_which_dict_is_validated(self, client, mocked):
        """Body-based validation is the caller's job; this helper always checks
        ``params``."""
        mocked.add(responses.POST, ROUTE_HOST, json={"ok": True}, status=200)

        with pytest.raises(ParamValueException):
            make_request(client.route, ROUTE_HOST, "post", {}, required=["route_id"], body={"route_id": ROUTE_ID})


class TestTelematicsDisplayHelpers:
    """``pp_response``/``pp_vendor_comparison`` print by design -- twelve
    ``examples/telematics/`` scripts depend on stdout. They now accept a
    ``file`` so they are testable and redirectable."""

    def test_pp_response_writes_key_value_lines(self):
        buffer = io.StringIO()

        Route4Me("k" * 32).telematics.pp_response({"id": 3, "name": "Vendor"}, file=buffer)

        output = buffer.getvalue()
        assert "id : 3" in output
        assert "name : Vendor" in output

    def test_pp_response_ignores_non_dicts(self):
        buffer = io.StringIO()

        Route4Me("k" * 32).telematics.pp_response(["not", "a", "dict"], file=buffer)

        assert buffer.getvalue() == ""

    def test_pp_vendor_comparison_writes_a_tab_separated_row(self):
        buffer = io.StringIO()
        vendor = {"id": 7, "name": "Acme", "features": [{"name": "gps"}, {"name": "fuel"}]}

        Route4Me("k" * 32).telematics.pp_vendor_comparison(vendor, file=buffer)

        assert buffer.getvalue().strip() == "7\tAcme\tgps, fuel"

    def test_pp_vendor_comparison_tolerates_a_missing_features_key(self):
        """Previously raised ``KeyError`` on a vendor with no ``features``."""
        buffer = io.StringIO()

        Route4Me("k" * 32).telematics.pp_vendor_comparison({"id": 7, "name": "Acme"}, file=buffer)

        # rstrip("\n") only -- the trailing tab is the empty feature column and
        # is part of the expected output.
        assert buffer.getvalue().rstrip("\n") == "7\tAcme\t"
