"""The :class:`TerritoriesV5` resource (API V5): generate territories automatically."""

from ._url import path_segment
from .api_endpoints import (
    AUTOMATIC_TERRITORIES_JOB_RESULT_V5,
    AUTOMATIC_TERRITORIES_JOB_STATUS_V5,
    AUTOMATIC_TERRITORIES_V5,
)
from .base import Base
from .exceptions import APIException, ParamValueException


class TerritoriesV5(Base):
    """Territories with API V5: group addresses into territories automatically.

    Use it as ``route4me.territories_v5``. The methods send requests to
    ``/modules/api/v5.0/automatic-territories`` on ``wh.route4me.com``. The
    V4 territory methods are on :class:`~route4me.territory.Territory`.

    Generating territories is an asynchronous job: start it with
    :meth:`create_automatic_territories_job`, poll
    :meth:`get_automatic_territories_job_status` until the job has finished,
    then read the territories with :meth:`get_automatic_territories_job_result`.

    Unless stated otherwise, a method returns the decoded JSON reply, or on an
    API error the ``{"errors": ...}`` dict from :meth:`APIException.to_dict
    <route4me.exceptions.APIException.to_dict>` instead of raising.

    .. versionadded:: 1.0.0
    """

    def create_automatic_territories_job(self, **kwargs):
        """Start a job that groups addresses into territories.

        Sends ``POST /modules/api/v5.0/automatic-territories`` with the
        keywords as the JSON body. The API accepts the job with
        ``202 Accepted`` and returns its ID in the ``X-job-id`` header and the
        URL of its status in the ``Location`` header.

        :param kwargs: the job fields. Required: ``addresses``, a list of
            ``{"id": ..., "lat": ..., "lng": ...}``, or
            ``temporary_addresses_storage_id``, the ID of addresses stored
            earlier. Optional: ``mode``, the clustering mode (``0``, ``1`` or
            ``2``), and ``params``, a list of clustering parameters.
        :return: ``{"job_id": ..., "location": ..., "data": ...}``: the two
            headers, and the decoded body (the raw ``bytes`` when it is not
            JSON); or the ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when neither ``addresses`` nor
            ``temporary_addresses_storage_id`` is given.

        .. versionadded:: 1.0.0
        """
        if "addresses" not in kwargs and "temporary_addresses_storage_id" not in kwargs:
            raise ParamValueException("addresses, temporary_addresses_storage_id", "One of them is required")
        try:
            self.response = self._request(AUTOMATIC_TERRITORIES_V5, {}, "post", json=kwargs)
        except APIException as e:
            return e.to_dict()
        try:
            data = self.response.json()
        except ValueError:
            data = self.response.content
        headers = self.response.headers
        return {"job_id": headers.get("X-job-id"), "location": headers.get("Location"), "data": data}

    def get_automatic_territories_job_status(self, job_id):
        """Get the status of a territories job.

        Sends ``GET /modules/api/v5.0/automatic-territories/job-tracker/status/{job_id}``.
        The API answers ``200`` with ``{"status": "processing"}`` while the
        job runs, and ``303 See Other``, pointing at the result, once it has
        finished. The client follows redirects unless it was created with
        ``redirects=False``.

        :param job_id: ID of the job, from
            :meth:`create_automatic_territories_job`.
        :return: the decoded JSON reply, or the ``{"errors": ...}`` dict on an
            API error.
        :raise ParamValueException: when ``job_id`` is empty.

        .. versionadded:: 1.0.0
        """
        url = f"{AUTOMATIC_TERRITORIES_JOB_STATUS_V5}/{path_segment(job_id, 'job_id')}"
        return self._call_api(url, "get", {})

    def get_automatic_territories_job_result(self, job_id):
        """Get the territories a finished job generated.

        Sends ``GET /modules/api/v5.0/automatic-territories/job-tracker/result/{job_id}``.

        :param job_id: ID of the job, from
            :meth:`create_automatic_territories_job`.
        :return: the decoded JSON reply, with ``job_id`` and the territories
            under ``clusters``, each with ``cluster_id``, ``addresses_count``,
            ``centroid`` and ``shape``; or the ``{"errors": ...}`` dict on an
            API error, e.g. while the job is still running (``409``).
        :raise ParamValueException: when ``job_id`` is empty.

        .. versionadded:: 1.0.0
        """
        url = f"{AUTOMATIC_TERRITORIES_JOB_RESULT_V5}/{path_segment(job_id, 'job_id')}"
        return self._call_api(url, "get", {})
