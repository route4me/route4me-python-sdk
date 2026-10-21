import json
import logging
import time

import requests

from ._resilience import backoff_delay
from .api_endpoints import (
    ADD_ROUTE_NOTES_HOST,
    ADDRESS_HOST,
    BATCH_GEOCODER,
    SINGLE_GEOCODER,
)
from .base import Base
from .exceptions import APIException, ParamValueException

logger = logging.getLogger(__name__)

#: Attempts (including the first) when geocoding a single address.
MAX_GEOCODE_ATTEMPTS = 6

#: Backoff base for geocode retries, in seconds. Larger than the transport's
#: 0.2s because a geocoding failure usually means the geocoder is saturated
#: rather than momentarily unreachable.
GEOCODE_RETRY_INITIAL_DELAY = 0.5


class Address(Base):
    """
    An Address is a destination in a route or optimization problem.
    Addresses can be depots, which means they are a departure points.
    Addresses can belong to only one route and one optimization problem,
    except for depots. One depot can be part of many routes if we have a
    VRP (multi-route) solution.
    """

    REQUIRED_FIELDS = [
        "lat",
        "lng",
    ]

    def __init__(self, api):
        """
        Address Instance
        :param api:
        :param addresses:
        :return:
        """
        self.addresses = []
        Base.__init__(self, api)

    def get_route_id(self):
        """
        Return Route ID
        :return:
        """
        return self.get_response()["route_id"]

    def get_route_destination_id(self):
        """
        Return Destination ID
        :return:
        """
        return self.get_response()["route_destination_id"]

    def get_addresses(self):
        """
        Return Addresses
        :return:
        """
        return self.addresses

    def add_address(self, **kwargs):
        """
        Add addresses to optimization
        :param kwargs:
        :return:
        """
        if (
            self.check_required_params(kwargs, self.REQUIRED_FIELDS)
            or self.check_required_params(kwargs, ["order_id"])
            or self.check_required_params(kwargs, ["contact_id"])
        ):
            self.addresses.append(kwargs)
            self.api.optimization.data["addresses"] = self.addresses
        else:
            raise ParamValueException("addresses", "Params are not complete")

    def batch_fix_geocodes(self, addresses):
        geocoding_error = []
        params = {
            "format": "json",
        }
        addresses_map = {x["address"].replace("/", " - "): x for x in addresses}
        data = {"addresses": "||".join([x["address"] for x in addresses])}
        try:
            json_data = self.get_batch_geocodes(params, data)
        except json.decoder.JSONDecodeError:
            logger.warning("Error Geocoding some of the Addresses. Please check the addresses and try again.")
            # Returns (geocoding_error, addresses), matching the success path at
            # the end of this method. This used to return `addresses, []` --
            # the two slots swapped -- so a caller unpacking
            # `errors, addresses = batch_fix_geocodes(...)` silently got its
            # addresses in the error variable and an empty list of addresses.
            # The whole batch failed, so every address is an error.
            return list(addresses), addresses
        geocoded_addresses = []
        for address in json_data:
            try:
                original_address = addresses_map[address["original"]]
                original_address.update(
                    {
                        "lat": address["lat"],
                        "lng": address["lng"],
                    }
                )
                geocoded_addresses.append(original_address)
            except (IndexError, ValueError):
                geocoding_error.append(address)
        return geocoding_error, addresses

    def get_geocode(self, params):
        """
        Get Geocodes from given address
        :param params:
        :return: response as a object
        """
        try:
            self.response = self._request(SINGLE_GEOCODER, params, "get", data=[])
            return self.response.json()
        except APIException as e:
            return e.to_dict()

    def get_batch_geocodes(self, params, data):
        """
        Get Geocodes from given addresses
        :param params:
        :param data:
        :return: response as a object
        """
        try:
            self.response = self._request(BATCH_GEOCODER, params, "post", data=data)
            return self.response.json()
        except APIException as e:
            return e.to_dict()

    def fix_geocode(self, address, max_attempts=MAX_GEOCODE_ATTEMPTS):
        """Geocode one address, retrying transient failures.

        :returns: ``(geocoding_error, address)`` -- ``geocoding_error`` is
            ``None`` on success, or the address itself when every attempt failed.

        .. versionchanged:: 0.3.1
           Backoff now comes from :func:`route4me._resilience.backoff_delay`,
           the same exponential-with-jitter policy the transport uses. The
           previous loop slept ``random.randrange(1, 5) * 0.5`` -- uniform, not
           exponential, so it did not back off under sustained failure.
        """
        params = {"format": "json", "address": address.get("address")}
        for attempt in range(1, max_attempts + 1):
            try:
                json_data = self.get_geocode(params)
                address.update(json_data)
                return None, address
            except (AttributeError, requests.exceptions.ConnectionError):
                if attempt >= max_attempts:
                    return address, address
                time.sleep(backoff_delay(attempt, GEOCODE_RETRY_INITIAL_DELAY))
        # Unreachable: the loop either returns or exhausts max_attempts above.
        return address, address

    def request_address(self, params):
        params.update({"api_key": self.api.key})
        try:
            response = self._request(ADDRESS_HOST, params, "get")
            return response
        except APIException as e:
            return e.to_dict()

    def get_address(self, route_id, route_destination_id):
        params = {"route_id": route_id, "route_destination_id": route_destination_id}
        response = self.request_address(params)
        return response.json()

    def get_address_notes(self, route_id, route_destination_id):
        params = {
            "route_id": route_id,
            "route_destination_id": route_destination_id,
            "notes": True,
        }
        response = self.request_address(params)
        return response.json()

    def update_address(self, data, route_id, route_destination_id):
        params = {"route_id": route_id, "route_destination_id": route_destination_id}
        params.update({"api_key": self.api.key})
        try:
            response = self._request(ADDRESS_HOST, params, "put", json=data)
            return response.json()
        except APIException as e:
            return e.to_dict()

    def delete_address_from_route(self, route_id, route_destination_id):
        params = {"route_id": route_id, "route_destination_id": route_destination_id}
        params.update({"api_key": self.api.key})
        try:
            response = self._request(ADDRESS_HOST, params, "delete")
            return response.json()
        except APIException as e:
            return e.to_dict()

    def add_address_notes(self, note, **kwargs):
        """
        Add Address  Note using POST request
        :return: API response
        :raise: ParamValueException if required params are not present.
        """
        if self.check_required_params(kwargs, ["address_id", "route_id"]):
            data = {"strUpdateType": kwargs.pop("activity_type"), "strNoteContents": note}
            kwargs.update(
                {
                    "api_key": self.params["api_key"],
                }
            )
            try:
                self.response = self._request(ADD_ROUTE_NOTES_HOST, kwargs, "post", data=data)
                return self.response.json()
            except APIException as e:
                return e.to_dict()
        else:
            raise ParamValueException("params", "Params are not complete")

    def geocode(self, **kwargs):
        """
        Bulk Geocoder using POST request
        :return: API response
        :raise: ParamValueException if required params are not present.
        """
        if "format" not in kwargs:
            kwargs.update({"format": "csv"})
        kwargs.update(
            {
                "api_key": self.params["api_key"],
            }
        )
        if self.check_required_params(
            kwargs,
            [
                "addresses",
            ],
        ):
            try:
                response = self._request(BATCH_GEOCODER, kwargs, "post")
                return response.content
            except APIException as e:
                return e.to_dict()
        else:
            raise ParamValueException("params", "Params are not complete")
