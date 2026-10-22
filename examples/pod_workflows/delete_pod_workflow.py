"""Delete a proof of delivery workflow.

Calls :meth:`PodWorkflows.delete_pod_workflow
<route4me.pod_workflows.PodWorkflows.delete_pod_workflow>`, which sends
``DELETE /modules/api/v5.0/workflows/{workflow_guid}`` (API V5, on ``wh.route4me.com``). The API answers
with an empty body, so the example prints ``Deleted`` on success. The workflow is deleted.

Run it with::

    python examples/pod_workflows/delete_pod_workflow.py --api_key <your key> --workflow_guid <workflow GUID>
"""

import argparse

from route4me import Route4Me


def main(api_key, workflow_guid):
    """Delete the POD workflow and say whether it worked.

    :param api_key: Route4Me API key.
    :param workflow_guid: GUID of the POD workflow.
    """
    route4me = Route4Me(api_key)

    response = route4me.pod_workflows.delete_pod_workflow(workflow_guid)
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print("Deleted")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Delete POD Workflow")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--workflow_guid", dest="workflow_guid", help="POD workflow GUID", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key, args.workflow_guid)
