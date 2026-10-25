"""Request-level tests for :class:`route4me.pod_workflows.PodWorkflows`.

Each test pins the HTTP method, URL, query string and JSON body the SDK sends
for one public method.
"""

import json

import pytest
import responses

from route4me.api_endpoints import POD_WORKFLOWS_V5
from route4me.exceptions import ParamValueException

WORKFLOW_GUID = "WORKFLOW-1"
WORKFLOW = {
    "workflow_id": "signature-only",
    "is_enabled": True,
    "title": "Signature only",
    "done_actions": [{"title": "Signature", "type": "signeeName", "required": True}],
}


def body_of(request):
    """Decode a JSON request body, or ``None`` when there is none."""
    return None if request.body is None else json.loads(request.body)


class TestPodWorkflows:
    def test_get_pod_workflows_sends_the_paging_and_the_sort_order(self, client, mocked, last_request, query_of):
        mocked.add(responses.GET, POD_WORKFLOWS_V5, json={"data": [], "next_page_cursor": None}, status=200)

        result = client.pod_workflows.get_pod_workflows(
            cursor="CURSOR-1",
            per_page=10,
            search_query="signature",
            order_by=[("title", "asc"), ("is_enabled", "desc")],
        )

        assert result == {"data": [], "next_page_cursor": None}
        assert last_request().method == "GET"
        assert last_request().url.split("?")[0] == POD_WORKFLOWS_V5
        assert query_of(last_request()) == {
            "cursor": "CURSOR-1",
            "per_page": "10",
            "search_query": "signature",
            "order_by[0][0]": "title",
            "order_by[0][1]": "asc",
            "order_by[1][0]": "is_enabled",
            "order_by[1][1]": "desc",
        }
        assert body_of(last_request()) is None

    def test_get_pod_workflows_without_parameters_sends_no_query(self, client, mocked, last_request, query_of):
        mocked.add(responses.GET, POD_WORKFLOWS_V5, json={"data": []}, status=200)

        client.pod_workflows.get_pod_workflows()

        assert query_of(last_request()) == {}

    def test_get_pod_workflow_puts_the_guid_in_the_path(self, client, mocked, last_request, query_of):
        mocked.add(responses.GET, f"{POD_WORKFLOWS_V5}/{WORKFLOW_GUID}", json={"data": WORKFLOW}, status=200)

        assert client.pod_workflows.get_pod_workflow(WORKFLOW_GUID) == {"data": WORKFLOW}
        assert last_request().method == "GET"
        assert last_request().url.split("?")[0] == f"{POD_WORKFLOWS_V5}/{WORKFLOW_GUID}"
        assert query_of(last_request()) == {}

    def test_create_pod_workflow_posts_the_workflow(self, client, mocked, last_request, query_of):
        mocked.add(responses.POST, POD_WORKFLOWS_V5, json={"data": WORKFLOW}, status=201)

        assert client.pod_workflows.create_pod_workflow(**WORKFLOW) == {"data": WORKFLOW}
        assert last_request().method == "POST"
        assert last_request().url.split("?")[0] == POD_WORKFLOWS_V5
        assert query_of(last_request()) == {}
        assert body_of(last_request()) == WORKFLOW

    def test_update_pod_workflow_puts_the_workflow(self, client, mocked, last_request, query_of):
        mocked.add(responses.PUT, f"{POD_WORKFLOWS_V5}/{WORKFLOW_GUID}", json={"data": WORKFLOW}, status=201)

        client.pod_workflows.update_pod_workflow(WORKFLOW_GUID, **WORKFLOW)

        assert last_request().method == "PUT"
        assert last_request().url.split("?")[0] == f"{POD_WORKFLOWS_V5}/{WORKFLOW_GUID}"
        assert query_of(last_request()) == {}
        assert body_of(last_request()) == WORKFLOW

    @pytest.mark.parametrize("field", ["workflow_id", "is_enabled", "title"])
    @pytest.mark.parametrize(
        "call",
        [
            lambda workflows, fields: workflows.create_pod_workflow(**fields),
            lambda workflows, fields: workflows.update_pod_workflow(WORKFLOW_GUID, **fields),
        ],
    )
    def test_create_and_update_require_the_workflow_fields(self, client, mocked, call, field):
        fields = {name: value for name, value in WORKFLOW.items() if name != field}

        with pytest.raises(ParamValueException) as error:
            call(client.pod_workflows, fields)

        assert error.value.param == field
        assert not mocked.calls

    def test_delete_pod_workflow_returns_the_empty_reply(self, client, mocked, last_request, query_of):
        mocked.add(responses.DELETE, f"{POD_WORKFLOWS_V5}/{WORKFLOW_GUID}", status=204)

        assert client.pod_workflows.delete_pod_workflow(WORKFLOW_GUID) == b""
        assert last_request().method == "DELETE"
        assert last_request().url.split("?")[0] == f"{POD_WORKFLOWS_V5}/{WORKFLOW_GUID}"
        assert query_of(last_request()) == {}
        assert body_of(last_request()) is None

    def test_a_guid_with_a_slash_stays_one_path_segment(self, client, mocked, last_request):
        mocked.add(responses.GET, f"{POD_WORKFLOWS_V5}/a%2Fb", json={}, status=200)

        client.pod_workflows.get_pod_workflow("a/b")

        assert last_request().path_url == "/modules/api/v5.0/workflows/a%2Fb"

    @pytest.mark.parametrize(
        "call",
        [
            lambda workflows: workflows.get_pod_workflow(""),
            lambda workflows: workflows.update_pod_workflow("", **WORKFLOW),
            lambda workflows: workflows.delete_pod_workflow(None),
        ],
    )
    def test_an_empty_guid_is_rejected_before_any_request(self, client, mocked, call):
        with pytest.raises(ParamValueException):
            call(client.pod_workflows)

        assert not mocked.calls

    @pytest.mark.parametrize(("method", "verb"), [("get_pod_workflow", "GET"), ("delete_pod_workflow", "DELETE")])
    def test_an_api_error_is_returned_as_a_dict(self, client, mocked, method, verb):
        mocked.add(
            verb,
            f"{POD_WORKFLOWS_V5}/{WORKFLOW_GUID}",
            json={"status": False, "code": 404, "messages": ["Workflow not found"]},
            status=404,
        )

        assert getattr(client.pod_workflows, method)(WORKFLOW_GUID) == {"errors": ["Workflow not found"]}
