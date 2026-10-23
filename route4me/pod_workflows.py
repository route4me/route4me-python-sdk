"""The :class:`PodWorkflows` resource (API V5): proof of delivery workflows."""

from ._params import compact, require
from ._url import path_segment
from .api_endpoints import POD_WORKFLOWS_V5
from .base import Base

#: Body fields that :meth:`PodWorkflows.create_pod_workflow` and
#: :meth:`PodWorkflows.update_pod_workflow` require.
REQUIRED_WORKFLOW_FIELDS = ("workflow_id", "is_enabled", "title")


class PodWorkflows(Base):
    """Proof of delivery (POD) workflows: what a driver must record to complete or fail a stop (API V5).

    A workflow lists the ``done_actions`` and ``failed_actions`` the driver
    app asks for, such as a signature, a photo or a questionnaire. Use it as
    ``route4me.pod_workflows``. Every method sends a request to
    ``/modules/api/v5.0/workflows`` on ``wh.route4me.com``.

    Unless stated otherwise, a method returns the decoded JSON reply, or on an
    API error the ``{"errors": ...}`` dict from :meth:`APIException.to_dict
    <route4me.exceptions.APIException.to_dict>` instead of raising.

    .. versionadded:: 1.0.0
    """

    def __init__(self, api):
        """Create the resource.

        :param api: the :class:`~route4me.api.Route4Me` client.
        """
        Base.__init__(self, api)

    @staticmethod
    def _workflow_url(workflow_guid):
        """Build the URL of one workflow, with ``workflow_guid`` encoded as one path segment.

        :param workflow_guid: GUID of the workflow.
        :return: the absolute URL.
        :raise ParamValueException: when ``workflow_guid`` is empty.
        """
        return f"{POD_WORKFLOWS_V5}/{path_segment(workflow_guid, 'workflow_guid')}"

    def get_pod_workflows(self, *, cursor=None, per_page=None, search_query=None, order_by=None):
        """List the POD workflows, one page at a time.

        Sends ``GET /modules/api/v5.0/workflows`` with the given parameters in
        the query.

        :param cursor: the ``next_page_cursor`` of the previous page.
        :param per_page: workflows per page, 1 to 10000.
        :param search_query: only workflows that match this text.
        :param order_by: sort order, a list of ``(field, direction)`` pairs
            such as ``[("title", "asc")]``. It is sent as
            ``order_by[0][0]=title&order_by[0][1]=asc``.
        :return: the decoded JSON reply, or the ``{"errors": ...}`` dict on an
            API error.

        .. versionadded:: 1.0.0
        """
        query = compact(cursor=cursor, per_page=per_page, search_query=search_query)
        for index, pair in enumerate(order_by or []):
            for position, value in enumerate(pair):
                query[f"order_by[{index}][{position}]"] = value
        return self._call_api(POD_WORKFLOWS_V5, "get", query)

    def get_pod_workflow(self, workflow_guid):
        """Get one POD workflow.

        Sends ``GET /modules/api/v5.0/workflows/{workflow_guid}``.

        :param workflow_guid: GUID of the workflow, its ``workflow_guid``.
        :return: the decoded JSON reply, or the ``{"errors": ...}`` dict on an
            API error.
        :raise ParamValueException: when ``workflow_guid`` is empty.

        .. versionadded:: 1.0.0
        """
        return self._call_api(self._workflow_url(workflow_guid), "get", {})

    def create_pod_workflow(self, **fields):
        """Add a POD workflow.

        Sends ``POST /modules/api/v5.0/workflows`` with the keywords as the
        JSON body.

        :param fields: the workflow. Required: ``workflow_id``, your own ID
            for it; ``is_enabled``; and ``title``. Optional: ``is_default``,
            ``done_actions`` and ``failed_actions``, lists of actions, each a
            dict with ``title``, ``type`` (e.g. ``"signeeName"``),
            ``required`` and optionally ``options``.
        :return: the decoded JSON reply, or the ``{"errors": ...}`` dict on an
            API error.
        :raise ParamValueException: when a required field is missing.

        .. versionadded:: 1.0.0
        """
        require(fields, REQUIRED_WORKFLOW_FIELDS)
        return self._call_api(POD_WORKFLOWS_V5, "post", {}, body=fields)

    def update_pod_workflow(self, workflow_guid, **fields):
        """Replace a POD workflow.

        Sends ``PUT /modules/api/v5.0/workflows/{workflow_guid}`` with the
        keywords as the JSON body.

        :param workflow_guid: GUID of the workflow, its ``workflow_guid``.
        :param fields: the whole workflow, as for :meth:`create_pod_workflow`.
            Required: ``workflow_id``, ``is_enabled`` and ``title``.
        :return: the decoded JSON reply, or the ``{"errors": ...}`` dict on an
            API error.
        :raise ParamValueException: when ``workflow_guid`` is empty or a
            required field is missing.

        .. versionadded:: 1.0.0
        """
        url = self._workflow_url(workflow_guid)
        require(fields, REQUIRED_WORKFLOW_FIELDS)
        return self._call_api(url, "put", {}, body=fields)

    def delete_pod_workflow(self, workflow_guid):
        """Delete a POD workflow.

        Sends ``DELETE /modules/api/v5.0/workflows/{workflow_guid}``.

        :param workflow_guid: GUID of the workflow, its ``workflow_guid``.
        :return: the reply body: empty (``b""``) on success, since the API
            answers ``204 No Content``; the decoded JSON reply if there is
            one; or the ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``workflow_guid`` is empty.

        .. versionadded:: 1.0.0
        """
        return self._request_decoded(self._workflow_url(workflow_guid), {}, "delete")
