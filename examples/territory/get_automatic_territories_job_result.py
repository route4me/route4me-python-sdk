"""Get the territories an automatic territories job generated, with API V5.

Calls :meth:`TerritoriesV5.get_automatic_territories_job_result
<route4me.territories_v5.TerritoriesV5.get_automatic_territories_job_result>`, which sends
``GET /modules/api/v5.0/automatic-territories/job-tracker/result/{job_id}`` (API V5, on
``wh.route4me.com``), and prints each territory with its number of addresses.

Run it with::

    python examples/territory/get_automatic_territories_job_result.py --api_key <your key> --job_id <job ID>
"""

import argparse

from route4me import Route4Me


def main(api_key, job_id):
    """Print the territories of the job.

    :param api_key: Route4Me API key.
    :param job_id: ID of the job.
    """
    route4me = Route4Me(api_key)

    territories = route4me.territories_v5
    response = territories.get_automatic_territories_job_result(job_id)
    if "errors" in response.keys():
        print(response["errors"])
    else:
        for cluster in response.get("clusters", []):
            print(f"Territory {cluster.get('cluster_id')}: {cluster.get('addresses_count')} addresses")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Automatic Territories Job Result")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--job_id", dest="job_id", help="Job ID", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key, args.job_id)
