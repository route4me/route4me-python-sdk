"""Get the status of an asynchronous vehicle job.

Calls :meth:`VehiclesV5.get_vehicle_job_status <route4me.vehicles_v5.VehiclesV5.get_vehicle_job_status>`,
which sends ``GET /modules/api/v5.0/vehicles/job-tracker/status/{job_id}`` (API V5, on
``wh.route4me.com``), and prints the reply.

Run it with::

    python examples/vehicles/get_vehicle_job_status.py --api_key <your key> --job_id <job ID>
"""

import argparse

from route4me import Route4Me


def main(api_key, job_id):
    """Print the status of the job.

    :param api_key: Route4Me API key.
    :param job_id: ID of the job, as returned by a bulk vehicle method.
    """
    route4me = Route4Me(api_key)

    response = route4me.vehicles_v5.get_vehicle_job_status(job_id)
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get a Vehicle Job Status")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument(
        "--job_id", dest="job_id", help="Job ID returned by a bulk vehicle method", type=str, required=True
    )
    args = parser.parse_args()
    main(args.api_key, args.job_id)
