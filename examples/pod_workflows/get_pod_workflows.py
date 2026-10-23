"""List the proof of delivery workflows.

Calls :meth:`PodWorkflows.get_pod_workflows <route4me.pod_workflows.PodWorkflows.get_pod_workflows>`,
which sends ``GET /modules/api/v5.0/workflows`` (API V5, on ``wh.route4me.com``) with ``per_page`` and
the sort order (``order_by[0][0]=title&order_by[0][1]=asc``) in the query, and prints the first page.

Run it with::

    python examples/pod_workflows/get_pod_workflows.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Print the first page of the POD workflows.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    response = route4me.pod_workflows.get_pod_workflows(per_page=10, order_by=[("title", "asc")])
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get POD Workflows")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
