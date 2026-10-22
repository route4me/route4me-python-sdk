"""Start a job that groups addresses into territories, with API V5.

Calls :meth:`TerritoriesV5.create_automatic_territories_job
<route4me.territories_v5.TerritoriesV5.create_automatic_territories_job>`, which sends
``POST /modules/api/v5.0/automatic-territories`` (API V5, on ``wh.route4me.com``) with ``addresses``,
``mode`` and ``params`` as the JSON body, and prints the job ID the API returns. Poll the job with
``examples/territory/get_automatic_territories_job_status.py``. The addresses are samples.

Run it with::

    python examples/territory/create_automatic_territories_job.py --api_key <your key>
"""

import argparse

from route4me import Route4Me

ADDRESSES = [
    {"id": 1, "lat": 40.7636197, "lng": -73.9744388},
    {"id": 2, "lat": 40.7484405, "lng": -73.9856644},
    {"id": 3, "lat": 40.6892494, "lng": -74.0445004},
    {"id": 4, "lat": 40.7061927, "lng": -74.0091604},
]


def main(api_key):
    """Start the job and print its ID.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    territories = route4me.territories_v5
    response = territories.create_automatic_territories_job(addresses=ADDRESSES, mode=0, params=[])
    if "errors" in response:
        print(response["errors"])
    else:
        print(f"Job ID: {response['job_id']}")
        print(f"Status URL: {response['location']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create Automatic Territories Job")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
