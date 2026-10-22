# CHANGELOG

This is the history of changes of the `route4me` package.

> This file should be filled by maintainers, using pull requests
> Please, follow this [guide](https://keepachangelog.com/en/1.0.0/)

## [1.0.0] - Unreleased

This is the first release since 0.1.7.0, and PyPI still serves 0.0.7.1 from 2020.

It fixes every open bug report (#19, #26, #30–#43), adds 214 API methods for the operations the coverage issues list (#44–#107), and hardens how the SDK handles the API key. It also adds an offline test suite of 1,369 tests behind a request guard. Several fixes change behaviour that code may rely on, so read **Breaking changes** before upgrading.

### Breaking changes

**Requirements**
- **Python 3.9 or later.** Python 2 and the `six` dependency are gone.
- The dependency floors follow security fixes:
  - Python 3.10 and later: `requests>=2.33.0` and `urllib3>=2.8.0`.
  - Python 3.9: `requests>=2.32.5` and `urllib3>=2.6.3`. See `SECURITY.md`.

**Transport**
- **Requests time out after `(6.05, 30.0)` seconds** (connect, read) by default.
  - A long call now raises `requests.ReadTimeout` or `ConnectTimeout`, which resource methods do not catch.
  - Pass `timeout=None` for the old unbounded behaviour.
  - The route update methods also take a per-call `timeout=`.
- **API V5 requests send the key as `Authorization: Bearer <key>`** instead of the `api_key` query parameter, so the key no longer appears in URLs. V4 requests are unchanged.
- **API V5 requests send `Accept: application/json, */*;q=0.8`.** With `*/*`, API V5 answered errors with an HTML page, so their messages were lost. File exports still work, and an `Accept` you set on the client is kept.
- **Each client uses one pooled `requests.Session`.**
  - Patching `requests.get`, `post` or `request` no longer intercepts the SDK's calls. Patch `requests.Session.send`, or use `responses`.
  - Cookies now persist for the life of a client.
- **Retries stay off by default.**
  - With `retry_count` set, only GET, HEAD, OPTIONS and DELETE are retried.
  - POST and PUT are never retried, because replaying them can create or insert things twice.
  - Cloudflare's 520–524 errors now count as retryable.
- `redirects=False` now also applies to PUT and DELETE.
- **Boolean query values are sent as `1` and `0`.** `requests` sent them as `"True"` and `"False"`; PHP reads `"False"` as true, and the API V5 validation rejects both strings. `get_address_notes()` now sends `notes=1`.
- **API V5 list and dict query values are sent with bracketed keys**, for example `ids[]=1&ids[]=2` and `filters[status]=1`. PHP keeps only the last value of a repeated plain key, and `requests` could not send a dict or a nested list at all.

**Errors and return values**
- **`APIException.to_dict()["errors"]` is always a non-empty list of strings.** It holds:
  - the V4 `errors`;
  - the flattened V5 `messages`;
  - the `message` value;
  - or `["Unexpected server response"]`.

  It used to be a string for a non-JSON reply, and `None` when the reply had no `errors`, so `". ".join(result["errors"])` printed letter by letter or raised. The API V5 `error` message (for example "the required feature is not enabled") is read too.
- `APIException.url` and `.response` are redacted, which changes `str(exc)` and `exc.args`.
- `re_optimization()` raises `APIException` on an HTTP error.
- `get_optimization()` and `parse_response()` return the payload; they used to return `None`.
- `route_start_date_local()` raises on an invalid date, including a date with a time part.
- `Members` validation errors name the missing parameters; they used to always name `"order"`.
- `Address.fix_geocode()` copies only `lat` and `lng` from the first geocoder result. An API error, or a reply without coordinates, is reported as a failure.
- `Address.batch_fix_geocodes()` returns `(geocoding_error, addresses)` in the documented order, and reports unmatched results instead of raising `KeyError`.

**API surface**
- **Setters on resources take one positional value.** `opt.route_name(...)` and similar are now descriptors.
  - `opt.route_name(route_name=...)` now raises `TypeError`.
  - The 0/1 fields reject floats such as `1.0`.
- `from route4me.api import AvoindanceZones` no longer works. Import `AvoidanceZones`, or the alias `AvoindanceZones`, from `route4me.avoidance_zones`.
- `AdvancedConstraint` and `Bundling` are dataclasses: they compare by value and are no longer hashable.
- `ServiceTimeRules` keeps its rules as dict items instead of class attributes. Attribute access still works.
- `Bundling.to_dict()` returns a snapshot, not the live `__dict__`. Its `service_time_rules` holds only the rules that are set.
- `clean_dict()`, and so `AdvancedConstraint.to_dict()`, keeps `0`, `0.0` and `False`.
- **Per-call values no longer stick to a resource (#36).** A `route_id` passed to `get_route()`, a vendor ID, or `redirect=0` used to stay in the resource's `params` and travel with later requests. Code that relied on that must pass the value on every call.
- The internal `_request_get`, `_request_post`, `_request_put` and `_request_delete` helpers take keyword-only options. The `route4me._api_method` module is gone; `Base._call_api` replaces it.
- `Route4Me(headers=...)` defaults to `None`, which still means `HEADERS`.
- The library logs through `logging` and warns through `warnings` instead of printing.

### Security
- **Route IDs in URL paths are percent-encoded.**
  - `RouteStatus` and `Route.export_route_v5` inserted `route_id` raw.
  - `requests` resolves dot segments, so `route-status/../secret` reached `/modules/api/v5.0/secret` with the caller's key.
  - The `rapid_address` path components are now encoded the same way.
- **The API key stays out of request bodies.** `Optimization.update_optimization` and `ActivityFeed.log_specific_message` copied it there.
- **Credential-like query parameters are redacted by name**, not only the known list. Any name ending in `api_key`, `apikey`, `_token`, `_secret` or `password` is redacted, so `organization_api_key` (API V5 member configuration settings) never reaches a traceback.
- **The API key stays out of URLs, tracebacks and logs:**
  - URLs, for API V5, which now uses a bearer token;
  - tracebacks: `APIException` redacts URLs and bodies, including those of the V4 endpoints that echo parameters back;
  - logs.
- **No request state is shared between calls (#36).** This is the class of bug that sent the PHP SDK's requests to the wrong host.
- **A guard checks every test request:** https only, Route4Me hosts only, registered endpoints only, and the key only in its expected place.
- **CI hardening.**
  - CI actions are pinned to commit SHAs and use read-only tokens.
  - gitleaks runs in CI and as a pre-commit hook.
  - `SECURITY.md` describes how to report a vulnerability.

### Added
- **API coverage: 214 new methods (#44–#107).** They cover the Route4Me API V4 and V5 operations the coverage issues list. Every request shape comes from the OpenAPI specs, then the C# SDK; the issues' own paths were often wrong. Each method has a unit test and a runnable example.
  - **New resources on the client:**
    - Address book: `address_book_v5`, `address_barcodes`.
    - Vehicles: `vehicles_v5`, `vehicle_profiles`, `vehicle_capacity_profiles`.
    - Routes: `routes_v5`, `route_destinations_v5`.
    - Team and account: `team_v5`, `account_profile`, `auth_history`, `configuration_settings`, `configuration_settings_v5`.
    - Orders and schedules: `orders_v5`, `recurring_routes`.
    - Notes and proof of delivery: `notes`, `driver_reviews`, `pod_workflows`.
    - Places: `customers`, `facilities`, `locations` (with location types), `territories_v5`.
    - Tracking: `tracking_history`, `route_breaks`, `asset_tracking`.
    - Lookups: `distance`, `drivers`, `autocomplete`.
  - **Existing resources gain methods:**
    - `AddressBook`: groups, search by filter, saving geocoded addresses.
    - `Address`: move a destination to another route, delete destinations, mark visited or departed.
    - `Route.rename_route`.
    - `RouteStatus`: `set_route_stop_status`, `update_route_status_as_planned`, and cancel reasons in `set_route_status`.
    - `Members`: create, update and delete users, and member capabilities.
    - `Order`: filter, updates and custom user fields.
    - `Optimization`: hybrid optimizations and time prediction.
    - `OptimizationProfiles`: CRUD and entities.
    - `GPS`: batch pings, user locations and vehicle locations.
    - `FileUploading`: the JSON upload for bulk geocoding.
  - **Not implemented, with the reason recorded on each issue:**
    - operations on retired hosts or 404 endpoints;
    - the MyQ and OCR operations, which are not Route4Me APIs;
    - `expire_session.php`, which ends a browser session and is not an API-key call.
- PATCH requests (`Base._call_api(..., "patch", ...)`), used by API V5 partial updates. Like PUT, they are never retried.
- `Telematics.get_vendors_v5(**filters)` and `Telematics.get_vendor_v5(vendor_id)`, on `GET /modules/api/v5.0/telematics/vendors(/all)`.
- `Optimization.reset()` clears a staged optimization, so one client can build another (#26).
- `Base.validated_params(**kwargs)` runs the field setters on a copy.
- A `timeout=` argument on `Route.insert_address_into_route`, `move_addresses_from_route`, `update_route_parameters` and `update_route`.
- `Optimization.bundling()` accepts a `Bundling` object (#43), and `advanced_constraints()` accepts `AdvancedConstraint` objects.
- `Route.merge_routes(route_ids=...)` accepts a list of IDs.
- **Connection pooling, plus opt-in retry and an opt-in circuit breaker, mirroring the C# SDK.**
  - Retry uses exponential backoff.
  - Options: `retry_count`, `retry_initial_delay`, `enable_circuit_breaker`, `circuit_breaker_failure_threshold`, `circuit_breaker_duration`, `on_retry`, `on_circuit_breaker_open`, `use_session` and `session`.
  - `Retry-After` is honoured, capped at 120 s.
- `Route4Me.close()`, and use as a context manager (`with Route4Me(key) as r4m:`).
- `CircuitBreaker.state`: `"closed"`, `"open"` or `"half-open"`.
- `route4me.config.Route4MeConfig` for process-wide defaults. Precedence: per call, then constructor, then global, then default.
- `route4me/_redact.py` and `route4me/_url.py`, the redaction and URL helpers.
- `APIException.get_url()`.
- `Telematics.pp_response()` takes a `file=` stream.
- `AvoidanceZones`, the correctly spelled name. `AvoindanceZones` remains as an alias.
- Docstrings on every public module, class and method.

### Deprecated
- `Telematics.get_vendors`, `get_vendor`, `search_vendor` and `compare_vendors`: `telematics.route4me.com` is retired. Use `get_vendors_v5` and `get_vendor_v5`.
- `Telematics.pp_vendor_comparison`: it prints the features of the retired `compare_vendors` reply, and API V5 vendors have none.
- `RapidAddress.get_street_data`, `get_street_data_zip` and `get_street_data_service`: the street-data endpoints return 404 and have no replacement.
- `Route.export_route`: the V4 export endpoint returns 404. Use `export_route_v5`.
- `Members.webinar_registration(webiinar_date=...)`: pass `webinar_date`.

### Removed
- Python 2 support and `six`.
- The `route4me._api_method` module.
- Configs for dead services: Travis, AppVeyor, Scrutinizer, Codebeat (115 pragmas) and Codecov.
- Tests that called the live API. The suite is offline; `pytest-socket` blocks any connection.
- The seven `examples/rapid_address` examples, whose endpoints are gone.

### Fixed
- #19: four route methods sent their body as form data from 0.1.6.0 on, which the API cannot read for nested values. They send JSON again. The methods are `insert_address_into_route`, `move_addresses_from_route`, `update_route_parameters` and `update_route`. A slow insert no longer risks a duplicating retry.
- #26: a reused client accumulated addresses. Use `Optimization.reset()`.
- #30: `get_optimization()` raised `TypeError` for every real response.
- #31: `route_start_date_local()` silently accepted an invalid date (a missing `raise`).
- #32: `Telematics.delete_connection()` swallowed errors (a missing `return`).
- #33, #40: `ServiceTimeRules` shared its lists between instances, and its rules never reached the API.
- #34: `Route4Me(proxies=...)` and `Route4Me(headers=...)` shared one dict between clients.
- #35: `OrdersGroup.get_orders_group()` raised `TypeError` instead of `ParamValueException`.
- #36: per-call parameters leaked into later requests, at nine sites. `_make_request` also changed the `params` dict it was given.
- #37: `export_result_to_json()` had never worked, and both JSON exporters failed on non-ASCII text on Windows.
- #38: transport errors in `OrdersGroup` and `OptimizationProfiles` surfaced as `UnboundLocalError`, and so did errors in `RapidAddress`.
- #39: `Route.delete_route()` raised `AttributeError` from its own error handler. The same pattern is fixed in `Address.get_address()` and `get_address_notes()`.
- #41: `clean_dict()` dropped `0` and `False`, corrupting time windows such as `[0, 3600]`.
- #42: `RapidAddress.get_street_data()` sent no request when given `offset` and `limit`, or no arguments.
- #43: `Optimization.bundling()` rejected the `Bundling` object its error message asked for.
- **Optimization:**
  - `update_optimization()` sent its addresses as unreadable form data, and `reoptimize=True` as `"True"`.
  - `re_optimization()` never raised on an HTTP error.
- **Routes:**
  - `delete_routes()` split a single route ID string into one ID per character.
  - `merge_routes()` form-encoded a list of IDs as one field per ID.
  - `export_route_v5()` sent form data where the API takes JSON.
- **Address:**
  - `get_route_id()` and `get_route_destination_id()` called a method that did not exist.
  - `add_address_notes()` raised `KeyError` without `activity_type`.
  - `geocode()` sent the address list in the URL.
  - `batch_fix_geocodes()` returned its two values swapped.
  - `request_address()` changed the caller's dict.
- `Members.webinar_registration()` required and sent the misspelled `webiinar_date`.
- `export_request_to_json()` had the same encoding problem as #37.
- `APIException.to_dict()` raised on `None`, bytes or list bodies, and discarded V5 error messages.
- The circuit breaker's half-open state let every request through, and a failed probe did not re-open the breaker.
- `Slowdowns` accepted `True` and `False` as integers.
- `json2obj` raised on keys that are not identifiers.
- Several setter error messages named the wrong type or values.
- `Base.validate_params()` reported SDK bugs as "Not supported".
- `Telematics.pp_vendor_comparison()` raised `KeyError` for a vendor without `features`.

### Examples
- **337 examples**, one per method, including 214 for the new API coverage. Every example has a docstring saying what it shows, which SDK method it calls, the request it sends, and how to run it. All of them pass pylint.
- The vendor examples use API V5.
- New examples:
  - `members/get_api_key_users.py` (#112);
  - `geocoding/get_geocode.py` (#111);
  - `tracking/get_device_locations.py` (#109, #110).
- Broken examples are fixed:
  - wrong argument names or shapes;
  - the sixth item picked instead of the first;
  - a depot moved out of first place;
  - `update_route_parameters` reassigning the route to member 1;
  - error checks that could never be true.
- The member and share-route examples use `example.com` addresses.

### Internal
- Packaging moved to `pyproject.toml` (hatchling); `setup.py` is a shim.
- 1,369 offline tests with 97% line and branch coverage, and a 90% floor. Every request is checked against an endpoint registry built from the Route4Me OpenAPI specs.
- pylint gives zero messages on the package, the tests and the examples. ruff formats the code. mypy passes, with strict checks on the tier-A modules, and blocks CI.
- CI runs Python 3.9–3.14 on Linux, and Python 3.12 on macOS and Windows.

## [0.1.7.0] - 2024-06-24

### Changed

-   Optimization Profiles endpoint
-   README

## [0.1.6.0] - 2024-06-10

### Added

-   Optimization based on Orders Group
-   Slowdowns support, with example

### Changed

-   `make_request` behaviour
-   `clean_dict` — expanded test coverage and adjusted behaviour

### Fixed

-   Assorted bugs

## [0.1.5.1] - 2023-06-02

### Added

-   `clean_dict` utility function

### Fixed

-   Bug in `advanced_constraint.py`

## [0.1.5.0] - 2023-05-01

### Added

-   Route Status: set, get and rollback

## [0.1.4.5] - 2023-04-13

### Fixed

-   Bug in the merge-routes method

## [0.1.4.4] - 2023-03-16

### Fixed

-   Double JSON dump in request bodies

## [0.1.4.3] - 2023-01-20

### Added

-   Custom User-Agent header

## [0.1.4.2] - 2022-12-24

### Added

-   Order creation without geo-coordinates
-   Route creation with `order_id` or `contact_id`

## [0.1.4.1] - 2022-05-23

### Fixed

-   Issue #18 — empty list (mutable value) used as a default argument in
    multiple functions

## [0.1.4.0] - 2022-04-18

### Added

-   Pickup/Dropoff examples
-   Insert Locations examples

### Removed

-   Hardcoded `API_KEY` values from all examples

## [0.1.3.0] - 2022-03-31

### Added

-   Stop Bundling, with examples
-   Further Advanced Constraints examples

## [0.1.2.1] - 2022-02-08

### Added

-   Advanced Constraints feature

## [0.1.2.0] - 2021-08-13

### Added

-   Route multiple-stops re-sequence

## [0.1.1.0] - 2021-08-02

### Added

-   Route Exporter (API V5)

## [0.1.0.1] - 2021-03-23

### Added

-   Get, Update and Delete Telematics Connection

### Fixed

-   AppVeyor build script and version number

## [0.1.0.0] - 2020-08-31

### Added

-   Telematics Gateway

## [0.0.7.0] - 2020-09-01

### Removed

-   Python 2 support
-   Pypy build
-   Set Tracking Data Test

### Added

-   Documentation
-   Changelog file
-   Tox
-   MANIFEST file
-   VERSION file

### Fixed

-   Bug in Optimization Callback example
-   Some Test Cases that were failing

### Changed

-   setup.py
-   Travis config file

## [0.0.6.1] - 2019-11-11

### Added

-   Added Exception when the server could not geo-code some addresses

## [0.0.6.1] - 2019-11-06

### Added

-   Redirect flag to QS when redirects are disable

### Fixed

-   Bug on batch geocoding

## [0.0.6.0] - 2019-10-24

### Changed

-   Batch Geocodig method converted to POST request.

### Fixed

-   Bug that assign the geo-coordinates to the wrong addresses

## [0.0.5.2] - 2018-08-24

### Changed

-   All Examples to work with JSON response

### Fixed

-   Some Bugs

## [0.0.5.1] - 2018-08-22

### Changed

-   Changed all responses to JSON.

### Fixed

-   All examples to support JSON response
-   GPS Test

## [0.0.5.0] - 2018-02-26

### Added

-   Address-Book example to query for any field

### Removed

-   Lib xmltodict dependency.
-   Limit and offset as required fields in addressbook service

### Changed

-   Addresses service

## [0.0.4.0] - 2017-08-03

### Added

-   Optimized Callback URL feature and example

## [0.0.3.11] - 2016-11-02

### Added

-   Python 3 support

## [0.0.3.10] - 2016-09-19

### Added

-   Routes Management and Missing Examples

## [0.0.3.9] - 2016-09-16

### Added

-   Members Management

## [0.0.3.8] - 2016-09-12

### Added

-   Activity Feed Support and Examples
-   Optimization missing Examples
-   Rapid Address missing Examples, remove python env from all examples, moved geocoding examples to its own folder
-   File Uploading feature and examples
-   Avoidance Zone missing Examples

## [0.0.3.7] - 2016-07-25

### Added

-   Territory Support

## [0.0.3.6] - 2016-07-14

### Added

-   Rapid Address Support and Examples
-   Optimization Example

## [0.0.3.5] - 2016-06-22

### Added

-   Orders support

## [0.0.3.4] - 2016-04-22

### Added

-   Avoidance Zone Management
-   Address Book Management, Route Tracking

## [0.0.3.3] - 2016-04-18

### Added

-   Generic Example, Notes, Delete Route, Single Depot Multiple Driver, Single Depot Multiple Driver TW Examples and Features

## [0.0.3.2] - 2016-03-24

### Added

-   Activities, Optimizations, Routes, Telematics, and Users Examples
-   Notes, and Activities Services

## [0.0.3.1] - 2016-01-21

### Added

-   Trucking hazardous goods features

## [0.0.3.0] - 2016-01-19

### Added

-   Example to update address attributes/details in an existing route (i.e. custom data, alias, order details, weight)
-   Example to insert address into existing route
-   Example to remove address from existing route
-   Example to move address from one stop into another

## [0.0.2.14] - 2015-12-17

### Added

-   Optimization trucking parameters and min_tour_size

## [0.0.2.13] - 2015-12-03

### Changed

-   Exceptions and Algorithm Type verification

## [0.0.2.12] - 2015-11-28

### Added

-   Optimization parameters, added support to Algorithm 100 and 101

## [0.0.2.11] - 2015-08-13

### Fixed

-   Examples

## [0.0.2.10] - 2015-07-16

### Added

-   Turns Avoidance uturn and leftturn support

## [0.0.2.9] - 2015-05-12

### Changed

-   Enabled follow redirects feature

## [0.0.2.8] - 2015-04-27

### Added

-   Optimization parameter max_tour_size

## [0.0.2.7] - 2015-04-22

### Added

-   Disable redirects

## [0.0.2.6] - 2015-04-19

### Added

-   Retry feature in case of geocoding error

## [0.0.2.5] - 2015-04-08

### Changed

-   Multiple depot multiple driver example

### Added

-   Geo-localization getter retry functionality in case of failure

## [0.0.2.4] - 2015-04-01

### Added

-   Optimization quality and route start date feature
-   Geocoding Example

## [0.0.2.3] - 2015-03-31

### Fixed

-   Multiple Depot, Multiple Driver, Time window Example

## [0.0.2.2] - 2015-03-01

### Added

-   API Endpoints
-   Batch and single address geocoding

## [0.0.2.1] - 2015-02-20

### Added

-   Route Exporter feature

## [0.0.2.0] - 2015-02-19

### Added

-   Geocoding feature

## [0.0.1.0] - 2014-07-01

### Added

-   First commit of the package.
