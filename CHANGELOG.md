# CHANGELOG

This is the history of changes of the `route4me-python` package

> This file should be filled by maintainers, using pull requests
> Please, follow this [guide](https://keepachangelog.com/en/1.0.0/)

## [0.3.0.0] - 2026-07-28

Resilience release. Brings the transport to parity with the C# SDK's Polly
policy, and makes connection reuse the default.

### Added

-   **Connection pooling.** Each client now reuses one `requests.Session`, so
    calls no longer pay a fresh TCP and TLS handshake each time. This is the
    largest latency improvement available here. Disable with
    `Route4Me(key, use_session=False)`, or inject your own with
    `session=...`.
-   **Retry with exponential backoff**, mirroring the C# `RetryCount` /
    `RetryInitialDelay`. Off by default (`retry_count=0`), matching the C#
    default so upgrading cannot silently multiply the requests a service
    emits. Backoff is `initial_delay * 2 ** (attempt - 1)` with ±20% jitter;
    retryable statuses are 408, 429 and 5xx.
    -   **Only idempotent verbs are retried** (GET, HEAD, OPTIONS, PUT,
        DELETE). POST is deliberately excluded: replaying
        `POST /orders-platform/batch-create` after a 503 can create the orders
        twice, since the server may have processed the first request and failed
        only while responding. The C# Polly policy does retry POST; this SDK
        does not reproduce that hazard.
    -   `Retry-After` is honoured on 429 and clamped to 120s. The C# SDK
        ignores the header.
-   **Circuit breaker**, mirroring the C# `CircuitBreakerFailureThreshold` (5)
    and `CircuitBreakerDuration` (30s). Off by default; enable with
    `enable_circuit_breaker=True`. Opens after a run of consecutive failures,
    then half-opens and admits a single probe. `CircuitBreakerOpen` subclasses
    `requests.RequestException` so existing transport-error handling catches
    it. A 4xx does not count as a failure — that is the server working.
-   `Route4Me.close()` and context-manager support
    (`with Route4Me(key) as client:`) to release pooled connections.
-   `on_retry` and `on_circuit_breaker_open` callbacks. An exception raised
    inside either is logged and swallowed — a user callback cannot turn a
    recoverable failure into a crash.
-   Config resolution is now layered end to end: per-call > constructor >
    `Route4MeConfig` > shipped default.

### Fixed

-   `_make_request` no longer mutates the `params` dict it is given. Every
    resource passes its own long-lived `self.params`, so query parameters
    accumulated on that dict across calls and leaked between them.

## [0.2.0.0] - 2026-07-28

Security and infrastructure release. Two defects here are urgent for anyone
embedding the SDK in a service.

### Security

-   **Requests now time out.** Previously no `timeout` was passed to `requests`
    at all, so a stalled socket blocked the calling thread indefinitely. The
    default is `(6.05, 30.0)` — `(connect, read)` in seconds. The 30s read
    matches the C# SDK's `Route4MeConfig.HttpTimeout`; the 6.05s connect clears
    two TCP SYN retransmits so a blackholed host fails in ~6s rather than 30.
    Configure per call, per client (`Route4Me(key, timeout=...)`), or globally
    (`Route4MeConfig.timeout`). Pass `timeout=None` for the old unbounded
    behaviour.
-   **The API key no longer leaks into tracebacks.** `requests` resolves
    `Response.url` to the fully expanded URL, which for the V4 API carries
    `?api_key=<plaintext>`. That string was stored on `APIException` and
    appeared in `str(exc)`, `repr(exc)`, `exc.args` and every traceback frame —
    and was forwarded verbatim to any error reporter that serialises exception
    attributes. `APIException.url` is now redacted, and the raw URL is not
    retained on the instance at all. Response bodies are scrubbed too, since
    several V4 endpoints echo request parameters back inside error payloads.
    Opt out with `Route4MeConfig.redact_urls = False` (debugging only).
-   **Path injection in `rapid_address`.** `zipcode`, `housenumber`, `pk`,
    `offset` and `limit` were interpolated raw into URL paths, so a value
    containing `/`, `?`, `#` or `..` rewrote the request path against
    `rapid.route4me.com`. Path components are now percent-encoded with
    `safe=""` and validated. New internal helpers `route4me/_url.py`
    (`path_segment`, `path_int`, `join_path`) — mandatory for anything that
    lands in a URL path.

### Added

-   `route4me/config.py` — `Route4MeConfig`, mirroring the C# SDK's config
    class. Resolution order: per-call > constructor > global > default.
-   `route4me/_redact.py` — total (never-raising) redaction helpers for URLs,
    headers, query parameters and response bodies.
-   `APIException.get_url()`.

### Fixed

-   `RapidAddress.get_street_data` never made a request when `offset` and
    `limit` were supplied: it built the URL and then fell off the end of the
    function, returning `None`. It also returned `None` when called with no
    arguments. Both branches now issue the request.
-   `UnboundLocalError` in the `rapid_address` error handlers, where
    `except ValueError: return response.content` wrapped the request itself and
    so referenced `response` before assignment — masking the real error.
-   `APIException.to_dict()` raised out of the error path on three inputs: a
    `None` or non-`str` body (`TypeError`, not covered by `JSONDecodeError`), and
    a body that is valid JSON but not an object such as `[1, 2]`
    (`AttributeError` from `.get`).
-   `APIException.to_dict()` now understands the API V5 error envelope
    (`{"status": false, "code": …, "messages": {…}}`), which has no `errors`
    key. Every V5 failure previously returned `{"errors": None}` and discarded
    the message.
-   `Route4Me(headers=...)` no longer shares one dict between every client.
    `HEADERS` was a module-level dict used as a default argument, so mutating
    one client's headers mutated every other client's and the module constant.

### Changed

-   `APIException.to_dict()` on valid JSON with no `errors` key now returns
    `{"errors": "Unexpected server response"}` rather than `{"errors": None}`.
    An explicit `{"errors": null}` still round-trips as `{"errors": None}`.

## [Unreleased]

### Removed

-   Python 2 compatibility shims and the `six` dependency
-   Dead service configuration: `.scrutinizer.yml`, `.codebeatignore`, and all
    115 `# codebeat:disable/enable[...]` pragmas across the package and examples

### Added

-   `AvoidanceZones` — correctly spelled class name. `AvoindanceZones` is kept
    as a permanent backwards-compatible alias
-   `clean_dict()`-backed `to_dict()` on `AdvancedConstraint` and `Bundling`
-   Shared `make_request()` CRUD helper (`route4me/_api_method.py`)
-   `ValidatedField` descriptor system (`route4me/_fields.py`), replacing 46
    boilerplate setter methods on `Base`

### Changed

-   `print()` calls in library code replaced with the `logging` and `warnings`
    modules
-   `AdvancedConstraint` and `Bundling` converted to dataclasses

### Fixed

-   Missing `raise`, an undefined variable, a missing `return`, mutable default
    arguments, resource leaks, and pointless re-raises

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
