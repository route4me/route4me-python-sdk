"""Replace a proof of delivery workflow.

Calls :meth:`PodWorkflows.update_pod_workflow
<route4me.pod_workflows.PodWorkflows.update_pod_workflow>`, which sends
``PUT /modules/api/v5.0/workflows/{workflow_guid}`` (API V5, on ``wh.route4me.com``) with the whole
workflow as the JSON body, and prints the reply. This changes the workflow.

Run it with::

    python examples/pod_workflows/update_pod_workflow.py --api_key <your key> --workflow_guid <workflow GUID>
"""

import argparse

from route4me import Route4Me


def main(api_key, workflow_guid):
    """Replace the POD workflow and print the reply.

    :param api_key: Route4Me API key.
    :param workflow_guid: GUID of the POD workflow.
    """
    route4me = Route4Me(api_key)

    workflow = {
        "workflow_id": "example-signature",
        "title": "Signature or reason",
        "is_enabled": True,
        "is_default": False,
        "done_actions": [{"title": "Signature", "type": "signeeName", "required": True}],
        "failed_actions": [
            {
                "title": "Reason",
                "type": "multiplyChoice",
                "required": True,
                "options": [{"value": "Nobody home"}, {"value": "Wrong address"}],
            }
        ],
    }
    response = route4me.pod_workflows.update_pod_workflow(workflow_guid, **workflow)
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update POD Workflow")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--workflow_guid", dest="workflow_guid", help="POD workflow GUID", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key, args.workflow_guid)
