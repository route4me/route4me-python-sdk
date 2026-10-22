"""The :class:`VehiclesV5` resource (API V5): vehicles, their bulk actions and asynchronous jobs."""

from ._url import path_segment
from ._v5_params import query, require
from .api_endpoints import (
    VEHICLES_ASSIGN_V5,
    VEHICLES_BULK_ACTIVATE_V5,
    VEHICLES_BULK_DEACTIVATE_V5,
    VEHICLES_BULK_DELETE_V5,
    VEHICLES_BULK_RESTORE_V5,
    VEHICLES_BULK_UPDATE_V5,
    VEHICLES_EXECUTE_V5,
    VEHICLES_JOB_RESULT_V5,
    VEHICLES_JOB_STATUS_V5,
    VEHICLES_LICENSE_V5,
    VEHICLES_PAGINATE_V5,
    VEHICLES_SEARCH_V5,
    VEHICLES_SYNC_PENDING_V5,
    VEHICLES_V5,
)
from .base import Base
from .exceptions import APIException


class VehiclesV5(Base):
    """Vehicles of the account (API V5).

    Use it as ``route4me.vehicles_v5``. It mirrors the C# SDK's
    ``VehicleManagerV5``; :class:`~route4me.vehicles.Vehicle`
    (``route4me.vehicles``) keeps the older V4 call. Every method sends a
    request under ``/modules/api/v5.0/vehicles`` on ``wh.route4me.com``.

    Query parameters and JSON bodies are passed as keyword arguments. In a
    query, a ``bool`` is sent as ``1`` or ``0``.

    The bulk methods (:meth:`activate_vehicles`, :meth:`deactivate_vehicles`,
    :meth:`delete_vehicles`, :meth:`restore_vehicles` and
    :meth:`update_vehicles`) start an asynchronous job; follow it with
    :meth:`get_vehicle_job_status` and :meth:`get_vehicle_job_result`.

    Unless stated otherwise, a method returns the decoded JSON reply, or on an
    API error the ``{"errors": ...}`` dict from :meth:`APIException.to_dict
    <route4me.exceptions.APIException.to_dict>` instead of raising.
    """

    def __init__(self, api):
        """Create the resource.

        :param api: the :class:`~route4me.api.Route4Me` client.
        """
        Base.__init__(self, api)

    @staticmethod
    def _vehicle_url(vehicle_id, suffix=""):
        """Build a vehicle URL with ``vehicle_id`` encoded as one path segment.

        :param vehicle_id: ID of the vehicle.
        :param suffix: path after the vehicle ID, e.g. ``"/track"``.
        :return: the absolute URL.
        :raise ParamValueException: when ``vehicle_id`` is empty.
        """
        return f"{VEHICLES_V5}/{path_segment(vehicle_id, 'vehicle_id')}{suffix}"

    def _start_job(self, endpoint, body):
        """Send a bulk request, which the API runs as an asynchronous job.

        :param endpoint: absolute URL of the bulk endpoint.
        :param body: the JSON body.
        :return: the decoded JSON reply when it has one. The API usually
            answers ``202 Accepted`` with no body; then the return value is
            ``{"job_id": ..., "location": ...}``, read from the ``X-Job-Id``
            and ``Location`` headers (``job_id`` falls back to the last
            segment of ``Location``; either value is ``None`` when its header
            is missing). On an API error, the ``{"errors": ...}`` dict.
        """
        try:
            self.response = self._request(endpoint, {}, "post", json=body)
        except APIException as e:
            return e.to_dict()
        try:
            return self.response.json()
        except ValueError:
            location = self.response.headers.get("Location")
            job_id = self.response.headers.get("X-Job-Id")
            if not job_id and location:
                job_id = location.rstrip("/").rsplit("/", 1)[-1]
            return {"job_id": job_id, "location": location}

    def get_vehicles(self, **kwargs):
        """List the vehicles.

        Sends ``GET /modules/api/v5.0/vehicles``.

        :param kwargs: query parameters, e.g. ``show`` (``"active"``, the
            API default, ``"pending"``, ``"deleted"`` or ``"all"``),
            ``search_query``, ``is_operational``, ``only_with_profile``,
            ``with_multi_unit_fields``, ``telematics_connection_ids`` or
            ``facility_ids``.
        :return: the decoded JSON reply: the list of vehicles, or the
            ``{"errors": ...}`` dict on an API error.

        .. versionadded:: 1.0.0
        """
        return self._call_api(VEHICLES_V5, "get", query(kwargs))

    def create_vehicle(self, **kwargs):
        """Create a vehicle.

        Sends ``POST /modules/api/v5.0/vehicles`` with the keywords as the JSON
        body.

        :param kwargs: the vehicle fields, e.g. ``vehicle_alias``,
            ``vehicle_license_plate``, ``vehicle_make``, ``vehicle_model``,
            ``vehicle_type_id``, ``vehicle_profile_id`` or
            ``vehicle_capacity_profile_id``. Required: ``vehicle_alias``.
        :return: the decoded JSON reply: the new vehicle, or the
            ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``vehicle_alias`` is missing.

        .. versionadded:: 1.0.0
        """
        require(kwargs, ["vehicle_alias"])
        return self._call_api(VEHICLES_V5, "post", {}, body=kwargs)

    def get_paginated_vehicles_list(self, **kwargs):
        """List the vehicles one page at a time.

        Sends ``GET /modules/api/v5.0/vehicles/paginate``.

        :param kwargs: query parameters: ``page`` and ``per_page``, and the
            filters of :meth:`get_vehicles`, e.g. ``show`` or
            ``search_query``.
        :return: the decoded JSON reply: one page of vehicles, or the
            ``{"errors": ...}`` dict on an API error.

        .. versionadded:: 1.0.0
        """
        return self._call_api(VEHICLES_PAGINATE_V5, "get", query(kwargs))

    def get_vehicle_by_id(self, vehicle_id):
        """Get one vehicle.

        Sends ``GET /modules/api/v5.0/vehicles/{vehicle_id}``.

        :param vehicle_id: ID of the vehicle.
        :return: the decoded JSON reply: the vehicle, or the
            ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``vehicle_id`` is empty.

        .. versionadded:: 1.0.0
        """
        return self._call_api(self._vehicle_url(vehicle_id), "get", {})

    def delete_vehicle(self, vehicle_id):
        """Delete one vehicle.

        Sends ``DELETE /modules/api/v5.0/vehicles/{vehicle_id}``.

        :param vehicle_id: ID of the vehicle.
        :return: the decoded JSON reply: the deleted vehicle, or the
            ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``vehicle_id`` is empty.

        .. versionadded:: 1.0.0
        """
        return self._call_api(self._vehicle_url(vehicle_id), "delete", {})

    def get_vehicle_track(self, vehicle_id, **kwargs):
        """Get the track of one vehicle.

        Sends ``GET /modules/api/v5.0/vehicles/{vehicle_id}/track``.

        :param vehicle_id: ID of the vehicle.
        :param kwargs: query parameters: ``start`` and ``end``, the dates that
            bound the track, as ``YYYY-MM-DD``.
        :return: the decoded JSON reply: the track, or the ``{"errors": ...}``
            dict on an API error.
        :raise ParamValueException: when ``vehicle_id`` is empty.

        .. versionadded:: 1.0.0
        """
        return self._call_api(self._vehicle_url(vehicle_id, "/track"), "get", query(kwargs))

    def create_temporary_vehicle(self, **kwargs):
        """Assign a vehicle to a member until a given time.

        Sends ``POST /modules/api/v5.0/vehicles/assign`` with the keywords as
        the JSON body.

        :param kwargs: the assignment: ``vehicle_id``, ``assigned_member_id``,
            ``expires_at`` (a Unix timestamp), and optionally
            ``vehicle_license_plate``, ``accepting_new_tasks`` and
            ``force-assignment`` (pass it as ``**{"force-assignment": True}``).
            Required: ``vehicle_id``, ``assigned_member_id`` and
            ``expires_at``.
        :return: the decoded JSON reply: the assignment, or the
            ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when a required field is missing.

        .. versionadded:: 1.0.0
        """
        require(kwargs, ["vehicle_id", "assigned_member_id", "expires_at"])
        return self._call_api(VEHICLES_ASSIGN_V5, "post", {}, body=kwargs)

    def execute_vehicle_order(self, **kwargs):
        """Execute the order of a vehicle at a location.

        Sends ``POST /modules/api/v5.0/vehicles/execute`` with the keywords as
        the JSON body.

        :param kwargs: ``vehicle_id``, ``lat`` and ``lng``, all required.
        :return: the decoded JSON reply: the order, or the ``{"errors": ...}``
            dict on an API error.
        :raise ParamValueException: when a required field is missing.

        .. versionadded:: 1.0.0
        """
        require(kwargs, ["vehicle_id", "lat", "lng"])
        return self._call_api(VEHICLES_EXECUTE_V5, "post", {}, body=kwargs)

    def get_vehicle_by_license_plate(self, **kwargs):
        """Find a vehicle by its license plate.

        Sends ``GET /modules/api/v5.0/vehicles/license``.

        :param kwargs: query parameters. Required: ``vehicle_license_plate``.
        :return: the decoded JSON reply: the vehicle, or the
            ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``vehicle_license_plate`` is missing.

        .. versionadded:: 1.0.0
        """
        require(kwargs, ["vehicle_license_plate"])
        return self._call_api(VEHICLES_LICENSE_V5, "get", query(kwargs))

    def search_vehicles(self, **kwargs):
        """Search the given vehicles around a location.

        Sends ``POST /modules/api/v5.0/vehicles/search`` with the keywords as
        the JSON body.

        :param kwargs: ``vehicle_ids`` (a list of vehicle IDs), ``lat`` and
            ``lng``, all required.
        :return: the decoded JSON reply: the vehicles found, or the
            ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when a required field is missing.

        .. versionadded:: 1.0.0
        """
        require(kwargs, ["vehicle_ids", "lat", "lng"])
        return self._call_api(VEHICLES_SEARCH_V5, "post", {}, body=kwargs)

    def sync_pending_telematics_data(self, **kwargs):
        """Sync a pending vehicle from a telematics connection.

        Sends ``POST /modules/api/v5.0/vehicles/sync/pending`` with the
        keywords as the JSON body.

        :param kwargs: the vehicle fields. The API documents ``vehicle_alias``,
            ``r4m_telematics_gateway_connection_id`` and
            ``r4m_telematics_gateway_vehicle_id`` as the ones that identify the
            vehicle.
        :return: the decoded JSON reply: the synced vehicle, or the
            ``{"errors": ...}`` dict on an API error.

        .. versionadded:: 1.0.0
        """
        return self._call_api(VEHICLES_SYNC_PENDING_V5, "post", {}, body=kwargs)

    def activate_vehicles(self, **kwargs):
        """Activate several vehicles, as an asynchronous job.

        Sends ``POST /modules/api/v5.0/vehicles/bulk/activate`` with the
        keywords as the JSON body.

        :param kwargs: ``vehicle_ids``, the list of vehicle IDs. Required.
        :return: the decoded JSON reply, or for a ``202 Accepted`` reply
            without a body ``{"job_id": ..., "location": ...}``, read from its
            headers; or the ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``vehicle_ids`` is missing.

        .. versionadded:: 1.0.0
        """
        require(kwargs, ["vehicle_ids"])
        return self._start_job(VEHICLES_BULK_ACTIVATE_V5, kwargs)

    def deactivate_vehicles(self, **kwargs):
        """Deactivate several vehicles, as an asynchronous job.

        Sends ``POST /modules/api/v5.0/vehicles/bulk/deactivate`` with the
        keywords as the JSON body.

        :param kwargs: ``vehicle_ids``, the list of vehicle IDs. Required.
        :return: the decoded JSON reply, or for a ``202 Accepted`` reply
            without a body ``{"job_id": ..., "location": ...}``, read from its
            headers; or the ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``vehicle_ids`` is missing.

        .. versionadded:: 1.0.0
        """
        require(kwargs, ["vehicle_ids"])
        return self._start_job(VEHICLES_BULK_DEACTIVATE_V5, kwargs)

    def delete_vehicles(self, **kwargs):
        """Delete several vehicles, as an asynchronous job.

        Sends ``POST /modules/api/v5.0/vehicles/bulk/delete`` with the keywords
        as the JSON body.

        :param kwargs: ``vehicle_ids``, the list of vehicle IDs. Required.
        :return: the decoded JSON reply, or for a ``202 Accepted`` reply
            without a body ``{"job_id": ..., "location": ...}``, read from its
            headers; or the ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``vehicle_ids`` is missing.

        .. versionadded:: 1.0.0
        """
        require(kwargs, ["vehicle_ids"])
        return self._start_job(VEHICLES_BULK_DELETE_V5, kwargs)

    def restore_vehicles(self, **kwargs):
        """Restore several deleted vehicles, as an asynchronous job.

        Sends ``POST /modules/api/v5.0/vehicles/bulk/restore`` with the
        keywords as the JSON body.

        :param kwargs: ``vehicle_ids``, the list of vehicle IDs. Required.
        :return: the decoded JSON reply, or for a ``202 Accepted`` reply
            without a body ``{"job_id": ..., "location": ...}``, read from its
            headers; or the ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``vehicle_ids`` is missing.

        .. versionadded:: 1.0.0
        """
        require(kwargs, ["vehicle_ids"])
        return self._start_job(VEHICLES_BULK_RESTORE_V5, kwargs)

    def update_vehicles(self, **kwargs):
        """Update several vehicles at once, as an asynchronous job.

        Sends ``POST /modules/api/v5.0/vehicles/bulk/update`` with the keywords
        as the JSON body.

        :param kwargs: ``vehicles``, a list of vehicle dicts, each with its
            ``vehicle_id`` and the fields to change. Required.
        :return: the decoded JSON reply, or for a ``202 Accepted`` reply
            without a body ``{"job_id": ..., "location": ...}``, read from its
            headers; or the ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``vehicles`` is missing.

        .. versionadded:: 1.0.0
        """
        require(kwargs, ["vehicles"])
        return self._start_job(VEHICLES_BULK_UPDATE_V5, kwargs)

    def get_vehicle_job_status(self, job_id):
        """Get the status of an asynchronous vehicle job.

        Sends ``GET /modules/api/v5.0/vehicles/job-tracker/status/{job_id}``.
        While the job runs, the reply is ``{"status": "processing"}``. Once it
        is over, the API answers ``303 See Other`` towards the job result: with
        redirects on (the client default) the return value is that result, as
        from :meth:`get_vehicle_job_result`; with them off, it is
        ``{"status": "processed"}``, ``"failed"`` or ``"canceled"``.

        :param job_id: ID of the job, from the bulk method that started it.
        :return: the decoded JSON reply, or the ``{"errors": ...}`` dict on an
            API error.
        :raise ParamValueException: when ``job_id`` is empty.

        .. versionadded:: 1.0.0
        """
        url = f"{VEHICLES_JOB_STATUS_V5}/{path_segment(job_id, 'job_id')}"
        return self._call_api(url, "get", {})

    def get_vehicle_job_result(self, job_id):
        """Get the result of an asynchronous vehicle job.

        Sends ``GET /modules/api/v5.0/vehicles/job-tracker/result/{job_id}``.

        :param job_id: ID of the job, from the bulk method that started it.
        :return: the decoded JSON reply: the job result, or the
            ``{"errors": ...}`` dict on an API error (for example while the
            job still runs).
        :raise ParamValueException: when ``job_id`` is empty.

        .. versionadded:: 1.0.0
        """
        url = f"{VEHICLES_JOB_RESULT_V5}/{path_segment(job_id, 'job_id')}"
        return self._call_api(url, "get", {})
