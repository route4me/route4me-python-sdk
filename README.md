# Route4Me Route Optimization Python SDK

[![CI](https://github.com/route4me/route4me-python-sdk/actions/workflows/ci.yml/badge.svg)](https://github.com/route4me/route4me-python-sdk/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/route4me.svg)](https://pypi.org/project/route4me/)
[![Python versions](https://img.shields.io/pypi/pyversions/route4me.svg)](https://pypi.org/project/route4me/)

The official Python client for the [Route4Me](https://route4me.com) API: route optimization, routes, orders, address book, members, tracking, telematics and more.

## Requirements

- Python 3.9 or later. On Python 3.9 some fixed `requests` and `urllib3` releases are not available; see [SECURITY.md](https://github.com/route4me/route4me-python-sdk/blob/master/SECURITY.md).
- A Route4Me API key, from **Settings → API** in your Route4Me account.

## Installation

```bash
pip install route4me
```

To install the development version from GitHub:

```bash
pip install git+https://github.com/route4me/route4me-python-sdk.git
```

## Quick start

Plan and optimize a round trip for one driver:

```python
import os

from route4me import Route4Me
from route4me.constants import ALGORITHM_TYPE, DISTANCE_UNIT, OPTIMIZE, TRAVEL_MODE
from route4me.exceptions import APIException

# The demo key 11111111111111111111111111111111 works with these sample addresses.
r4m = Route4Me(os.environ["ROUTE4ME_API_KEY"])

optimization = r4m.optimization
optimization.algorithm_type(ALGORITHM_TYPE.TSP)
optimization.route_name("Single Driver Round Trip")
optimization.rt(1)
optimization.optimize(OPTIMIZE.TIME)
optimization.distance_unit(DISTANCE_UNIT.MI)
optimization.travel_mode(TRAVEL_MODE.DRIVING)
optimization.route_max_duration(86400)

address = r4m.address
address.add_address(
    address="754 5th Ave New York, NY 10019",
    lat=40.7636197,
    lng=-73.9744388,
    alias="Bergdorf Goodman",
    is_depot=1,
    time=0,
)
address.add_address(
    address="717 5th Ave New York, NY 10022",
    lat=40.7669692,
    lng=-73.9693864,
    alias="Giorgio Armani",
    time=60,
)
address.add_address(
    address="888 Madison Ave New York, NY 10014",
    lat=40.7715154,
    lng=-73.9669241,
    alias="Ralph Lauren Women's and Home",
    time=60,
)

try:
    response = r4m.run_optimization()
except APIException as error:
    print(". ".join(error.to_dict()["errors"]))
else:
    print(f"Optimization problem ID: {response['optimization_problem_id']}")
    for stop in response["addresses"]:
        print(f"{stop['sequence_no']} - {stop['alias']} - {stop['address']}")
```

Keep the API key out of your code: read it from an environment variable or a secrets store, as above.

## Usage

### The client

`Route4Me(api_key)` gives access to every part of the API through its attributes, for example `r4m.optimization`, `r4m.route`, `r4m.address`, `r4m.address_book`, `r4m.members`, `r4m.order`, `r4m.vehicles`, `r4m.territory`, `r4m.telematics` and `r4m.gps`. The [examples](https://github.com/route4me/route4me-python-sdk/tree/master/examples) show each one.

Each client reuses one HTTP connection pool. Close it when you are done, or use the client as a context manager:

```python
with Route4Me(api_key) as r4m:
    routes = r4m.route.get_routes(limit=10, offset=0)
```

### Authentication

The SDK sends the key the way each API expects it:

- **API V4** (`api.route4me.com`): as the `api_key` query parameter.
- **API V5** (`wh.route4me.com/modules/api/v5.0`): as an `Authorization: Bearer` header, so the key never appears in a URL.

The key is never put in a request body, and it is removed from the URLs and bodies stored on exceptions.

### Errors

- **Resource methods** such as `r4m.route.get_route()` do not raise on an API error. They return `{"errors": [...]}`, a non-empty list of messages:

  ```python
  result = r4m.route.get_route(route_id=route_id)
  if "errors" in result:
      print(". ".join(result["errors"]))
  ```

- **Client methods** such as `r4m.run_optimization()` raise `route4me.exceptions.APIException`. Its `to_dict()` returns the same `{"errors": [...]}` dict.
- **A missing or invalid parameter** raises `route4me.exceptions.ParamValueException` before any request is sent.
- **Network errors and timeouts** raise the `requests` exception, for example `requests.ConnectionError` or `requests.ReadTimeout`.

### Timeouts, retries and the circuit breaker

- **Timeouts.** Requests time out after 6.05 seconds to connect and 30 seconds to read. Pass `timeout=` to the client: a number, a `(connect, read)` pair, or `None` to wait forever.
- **Retries** are off by default. Set `retry_count=` to retry failed GET, HEAD, OPTIONS and DELETE requests with exponential backoff.
  - Only connection errors, timeouts, and the statuses 408, 429, 500, 502–504 and Cloudflare's 520–524 are retried.
  - POST and PUT are never retried, since replaying them can create something twice.
  - A `Retry-After` header is honoured, up to 120 seconds.
- **The circuit breaker** is opt-in: `enable_circuit_breaker=True` stops sending requests for a while after repeated failures.

```python
from route4me import Route4Me
from route4me.config import Route4MeConfig

# For one client:
r4m = Route4Me(api_key, timeout=(5, 60), retry_count=3, enable_circuit_breaker=True)

# For every client in the process:
Route4MeConfig.timeout = (5, 60)
```

A value passed to a call wins over one passed to the client, which wins over `Route4MeConfig`.

### API V5

The V5 methods take and return plain dicts. For example, list the telematics vendors:

```python
vendors = r4m.telematics.get_vendors_v5(search="geotab")
for vendor in vendors["data"]:
    print(vendor["id"], vendor["name"])
```

### Deprecated methods

The methods that call retired Route4Me hosts still exist, but they emit a `DeprecationWarning` and will be removed in 2.0. Each warning names its replacement where there is one. See the [CHANGELOG](https://github.com/route4me/route4me-python-sdk/blob/master/CHANGELOG.md).

## Upgrading from 0.x

1.0.0 fixes many long-standing bugs, and some of those fixes change behaviour. Read **Breaking changes** in the [CHANGELOG](https://github.com/route4me/route4me-python-sdk/blob/master/CHANGELOG.md) before upgrading. The changes most likely to affect existing code:

- Requests now time out.
- Setters take one positional value: `opt.route_name("Monday")`, not `opt.route_name(route_name="Monday")`.
- Values passed to one call no longer leak into later calls on the same resource.
- `errors` is always a list of strings.

## Examples

The [examples](https://github.com/route4me/route4me-python-sdk/tree/master/examples) folder has a runnable script for almost every method. Each takes the API key on the command line:

```bash
python examples/routes/get_routes.py --api_key <your key>
```

## Development

```bash
pip install -e ".[dev]"

pytest                                   # offline unit tests, with coverage
pylint route4me --rcfile=pyproject.toml  # library lint
pylint tests --rcfile=tests/pylintrc
pylint --rcfile=examples/pylintrc $(git ls-files 'examples/*.py')
ruff format --check route4me tests examples
mypy route4me
```

The test suite never touches the network: `pytest-socket` blocks connections and `responses` fakes the API. A guard also checks every request a test sends: https only, Route4Me hosts only, endpoints from the OpenAPI specs only, and the API key only in its expected place.

## Security

See [SECURITY.md](https://github.com/route4me/route4me-python-sdk/blob/master/SECURITY.md) to report a vulnerability. Never commit an API key; if one leaks, rotate it in your Route4Me account.

## License

See [LICENSE.md](https://github.com/route4me/route4me-python-sdk/blob/master/LICENSE.md).

## FAQ

### What does Route4Me do?

In layman's terms Route4Me solves complex variations of the [traveling salesman problem](https://blog.route4me.com/traveling-salesman-problem/) and the [vehicle routing problem](https://blog.route4me.com/vehicle-routing-problems-real-life-solutions/). In more technical terms, Route4Me solves NP-hard logistics problems that span several mathematical and scientific disciplines such as industrial engineering, operations research, algorithmic graph theory, computational geometry, combinatorial optimization, fleet management, field service management, [telematics](https://route4me.com/integrations/telematics).

### What does the Route4Me SDK permit me to do?

This SDK makes it easier for you to use the Route4Me API. The API has many features, including [route optimization](https://route4me.io/), and the primary features are related to creating orders and then [creating optimally sequenced driving routes](https://route4me.com) for many drivers.

### Who can use the Route4Me SDK (and API)?

The service is typically used by organizations who must route many drivers to many destinations. In addition to route optimization for new (future) routes, the API can also be used to analyze historical routes, and to distribute routes to field personnel.

### Who is prohibited from using the Route4Me SDK (and API)?

The Route4Me SDK and API cannot be resold or used in a product or system that competes directly with Route4Me. This means that developers cannot resell route optimization services to other businesses or developers. However, developers can integrate our route optimization SDK/API into their software applications. Developers and startups are also permitted to use our software for internal purposes (i.e. a same day delivery startup).

### How does the API/SDK Integration Work?

A Route4Me customer, integrator, or partner incorporates the Route4Me SDK or API into their code base.
Route4Me permits any paying subscriber to interact with every part of its system using its API.
The API is RESTful, which means that it’s web based and can be accessed by other programs and machines
The API/SDK should be used to automate the route planning process, or to generate many routes with minimal manual intervention

### Do optimized routes automatically appear inside my Route4Me account?

Every Route4Me SDK instance needs a unique API key. The API key can be retrieved inside your Route4Me.com account, inside the Settings tab called API. When a route is planned, it appears inside the corresponding Route4Me account. Because Route4Me web and mobile accounts are synchronized, the routes will appear in both environments at the same time.

### Can I test the SDK with other addresses without a valid API Key?

No. The sample API key only permits you to optimize routes with the sample address coordinates that are part of this SDK.

### Does the SDK have rate limits?

The number of requests you can make per second is limited by your current subscription plan. Typically, there are different rate limits for these core features:
Address Geocoding & Address Reverse Geocoding
Route Optimization & Management
Viewing a Route

### What is the recommended integration architecture for the Route4Me SDK?

There are two typical integration strategies that we recommend. Using this SDK, you can make optimization requests and then the SDK polls the Route4Me API to detect state changes as the optimization progresses. Alternatively, you can provide a webhook/callback url, and the API will notify that callback URL every time there is a state change.

### I don't need route management or mobile capabilities. Can I just use the route planning and route optimization API?

There are no additional costs to use the web interface or the mobile application to view your [optimized routes](https://support.route4me.com/route-planner-routes-list/), which mean that you can use only the API without paying extra
for our web app or mobile app.

### How fast is the route Route4Me Optimization Web Service?

Most routes having less than 200 destinations are optimized in 1 second or less. Larger routes having thousands of stops are split into their
most reasonably optimal geographical regions, and then each of those regions is independently optimized in parallel. Whether you use polling or push,
you will be able to retrieve all the routes optimized that were created from a large optimization problem set.

### Can I disable optimization when planning routes?

Yes. You can send routes with optimization disabled if you want to conveniently see them on a map, or distribute them to your drivers in the order you prefer.

### Can the API be used for aerial vehicles such as drones or self-driving cars?

Yes. The API can accept lat/lng and an unlimited amount metadata per destination (e.g. altitude, weight, pieces, cubic dimension). The metadata will be preserved as passthrough data by our API, so that the receiving service or device will have access to critical data when our API invokes a webhook callback to the device.

### Are all my optimized routes permanently stored in the Route4Me database?

Yes. Unless your contract specifies otherwise, all routes are permanently stored in the database and are no longer accessible to you after your subscription is terminated. Route4Me auto-prunes route data
based on your subscription plan, with more expensive plans typically permitting a longer archival period.

### Can I incorporate your API into my mobile application that requires routing, navigation, or route planning?

Route4Me's route planning and optimization technology can only be added into applications that do not directly compete with Route4Me.
This means the application’s primary capabilities must be unrelated to route optimization, route planning, or navigation.

### Can I pay you to develop a custom algorithm?

Yes

### Can I use your API and resell it to my customers?

White-labeling and private-labeling Route4Me is possible but the deal's licensing terms vary considerably based on customer count, route count, and the level of support that Route4Me should provide to your customers.

### Does the API/SDK have TMS or EDI, or EDI translator capabilities?

Yes

### Can the API/SDK send notifications back to our system using callbacks, notifications, pushes, or webhooks?

Because Route4Me processes all routes asynchronously, Route4Me will immediately notify the endpoint you specify as a route optimization job progresses through each state of the optimization. Every stage of the route optimization process has a unique stage id.

### Does the Route4Me API and SDK work in my country?

Route4Me.com, as well as all of Route4Me’s mobile applications use the Route4Me SDK’s and API.
Since Route4Me works globally, this means that all of Route4Me’s capabilities are available using the SDK’s in almost every country that has well digitized maps.

### Will the Route4Me API/SDK work in my program on Linux/\*Nix/Kubernetes/Docker, Windows, Mac?

Customers are encouraged to select their preferred operating system environment. The Route4Me API/SDK will function on any operating system that supports the preferred programming language of the customer. At this point in time, almost every supported SDK can run on any operating system.

### Does the Route4Me API/SDK require me to buy my own servers?

Route4Me has its own computing infrastructure that you can access using the API and SDKs. Customers typically have to run the SDK code on their own computers and/or servers to access this infrastructure.

### Does Route4Me have an on-premise solution?

Route4Me does not currently lease or sell servers, and does not have on-premise appliance solution. This would only be possible in exceptionally unique scenarios.

### Does the Route4Me API/SDK require me to have my own programmers?

The time required to integrate the SDK can be as little as 1 hour or may take several weeks, depending on the number of features being incorporated into the customer’s application and how much integration testing will be done by the client. A programmer’s involvement is almost always required to use Route4Me’s technology when accessing it through the API.
