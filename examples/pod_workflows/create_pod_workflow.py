"""Add a proof of delivery workflow.

Calls :meth:`PodWorkflows.create_pod_workflow
<route4me.pod_workflows.PodWorkflows.create_pod_workflow>`, which sends
``POST /modules/api/v5.0/workflows`` (API V5, on ``wh.route4me.com``) with the workflow as the JSON
body: a signature when the stop is done, and a reason when it fails. Prints the reply. The workflow
stays on the account.

Run it with::

    python examples/pod_workflows/create_pod_workflow.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Add a POD workflow and print the reply.

    :param api_key: Route4Me API key.
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
    response = route4me.pod_workflows.create_pod_workflow(**workflow)
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create POD Workflow")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
