"""The :class:`Notes` resource: route notes (API V5) and custom note types (API V4 and V5)."""

from ._params import compact, require
from ._url import path_segment
from .api_endpoints import (
    NOTE_CUSTOM_TYPES_V4,
    NOTES_BULK_CREATE_V5,
    NOTES_BY_DESTINATION_V5,
    NOTES_BY_ROUTE_V5,
    NOTES_CUSTOM_TYPES_V5,
    NOTES_V5,
)
from .base import Base
from .exceptions import ParamValueException


class Notes(Base):
    """Notes: what drivers and dispatchers record at the stops of a route.

    Use it as ``route4me.notes``. The note methods use API V5
    (``/modules/api/v5.0/notes`` on ``wh.route4me.com``). The custom note
    types, the extra fields a note can carry, exist in API V4
    (:meth:`add_custom_note_type`, :meth:`get_all_custom_note_types`,
    :meth:`remove_custom_note_type`) and in API V5
    (:meth:`create_note_custom_type`, :meth:`get_note_custom_types`).

    The API V4 notes of a route destination are in
    :class:`~route4me.address.Address`: :meth:`~route4me.address.Address.add_address_notes`
    and :meth:`~route4me.address.Address.get_address_notes`.

    Every method returns the decoded JSON reply, or on an API error the
    ``{"errors": ...}`` dict from :meth:`APIException.to_dict
    <route4me.exceptions.APIException.to_dict>` instead of raising.

    .. versionadded:: 1.0.0
    """

    def __init__(self, api):
        """Create the resource.

        :param api: the :class:`~route4me.api.Route4Me` client.
        """
        Base.__init__(self, api)

    # ----------------------------------------------------------- V5 notes --

    def create_note(self, **fields):
        """Add a note to a route or to one of its destinations.

        Sends ``POST /modules/api/v5.0/notes`` with the keywords as the JSON
        body.

        :param fields: the note. Required: ``route_id`` and
            ``strNoteContents``, the text. Optional: ``address_id`` or
            ``destination_uuid`` (the destination), ``strUpdateType`` (e.g.
            ``"dropoff"``), ``dev_lat``, ``dev_lng``, ``remote_speed``,
            ``remote_altitude``, ``device_type``, ``custom_note_type``,
            ``utc_time``, ``workflow_id`` and ``workflow_action_id``.
        :return: the decoded JSON reply, or the ``{"errors": ...}`` dict on an
            API error.
        :raise ParamValueException: when ``route_id`` or ``strNoteContents``
            is missing.

        .. versionadded:: 1.0.0
        """
        require(fields, ["route_id", "strNoteContents"])
        return self._call_api(NOTES_V5, "post", {}, body=fields)

    def bulk_create_notes(self, **fields):
        """Add several notes in one request; the API stores them asynchronously.

        Sends ``POST /modules/api/v5.0/notes/bulk-create`` with the keywords
        as the JSON body.

        :param fields: required: ``notes``, a list of note dicts as for
            :meth:`create_note`, each with ``route_id`` and
            ``strNoteContents`` and optionally an ``upload_id``. Optional:
            ``device_type``.
        :return: the decoded JSON reply, e.g. ``{"status": true, "async":
            true}``, or the ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``notes`` is missing or empty, or a
            note lacks ``route_id`` or ``strNoteContents``.

        .. versionadded:: 1.0.0
        """
        require(fields, ["notes"])
        if not fields["notes"]:
            raise ParamValueException("notes", "Must be a non-empty list of notes")
        for index, note in enumerate(fields["notes"]):
            missing = self._missing(note, ["route_id", "strNoteContents"])
            if missing:
                raise ParamValueException(f"notes[{index}]", "Missing required params: " + ", ".join(missing))
        return self._call_api(NOTES_BULK_CREATE_V5, "post", {}, body=fields)

    def get_note(self, note_id):
        """Get one note.

        Sends ``GET /modules/api/v5.0/notes/{note_id}``.

        :param note_id: ID of the note: the numeric ID or the 32-character
            hex ID.
        :return: the decoded JSON reply, or the ``{"errors": ...}`` dict on an
            API error.
        :raise ParamValueException: when ``note_id`` is empty.

        .. versionadded:: 1.0.0
        """
        return self._call_api(f"{NOTES_V5}/{path_segment(note_id, 'note_id')}", "get", {})

    def update_note(self, note_id, **fields):
        """Change a note.

        Sends ``POST /modules/api/v5.0/notes/{note_id}`` with the keywords as
        the JSON body.

        :param note_id: ID of the note: the numeric ID or the 32-character
            hex ID.
        :param fields: the fields to change: ``strNoteContents``,
            ``strUpdateType``, ``device_type``, ``custom_note_type``,
            ``workflow_id`` or ``workflow_action_id``.
        :return: the decoded JSON reply, or the ``{"errors": ...}`` dict on an
            API error.
        :raise ParamValueException: when ``note_id`` is empty.

        .. versionadded:: 1.0.0
        """
        return self._call_api(f"{NOTES_V5}/{path_segment(note_id, 'note_id')}", "post", {}, body=fields)

    def delete_note(self, note_id):
        """Delete a note.

        Sends ``DELETE /modules/api/v5.0/notes/{note_id}``.

        :param note_id: ID of the note: the numeric ID or the 32-character
            hex ID.
        :return: the decoded JSON reply, e.g. ``{"status": true, "note_id":
            7}``, or the ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``note_id`` is empty.

        .. versionadded:: 1.0.0
        """
        return self._call_api(f"{NOTES_V5}/{path_segment(note_id, 'note_id')}", "delete", {})

    def get_notes_by_route(self, route_id, *, page=None, per_page=None):
        """List the notes of a route, one page at a time.

        Sends ``GET /modules/api/v5.0/notes/route/{route_id}`` with ``page``
        and ``per_page`` in the query when given.

        :param route_id: ID of the route.
        :param page: page number, from 1.
        :param per_page: notes per page.
        :return: the decoded JSON reply, or the ``{"errors": ...}`` dict on an
            API error.
        :raise ParamValueException: when ``route_id`` is empty.

        .. versionadded:: 1.0.0
        """
        url = f"{NOTES_BY_ROUTE_V5}/{path_segment(route_id, 'route_id')}"
        return self._call_api(url, "get", compact(page=page, per_page=per_page))

    def get_notes_by_destination(self, route_destination_id, *, page=None, per_page=None):
        """List the notes of a route destination, one page at a time.

        Sends ``GET /modules/api/v5.0/notes/destination/{route_destination_id}``
        with ``page`` and ``per_page`` in the query when given.

        :param route_destination_id: ID of the route destination: the numeric
            ID or the destination UUID.
        :param page: page number, from 1.
        :param per_page: notes per page.
        :return: the decoded JSON reply, or the ``{"errors": ...}`` dict on an
            API error.
        :raise ParamValueException: when ``route_destination_id`` is empty.

        .. versionadded:: 1.0.0
        """
        url = f"{NOTES_BY_DESTINATION_V5}/{path_segment(route_destination_id, 'route_destination_id')}"
        return self._call_api(url, "get", compact(page=page, per_page=per_page))

    # ---------------------------------------------- V5 note custom types --

    def get_note_custom_types(self):
        """List the custom note types of the account.

        Sends ``GET /modules/api/v5.0/notes/custom-types``.

        :return: the decoded JSON reply, or the ``{"errors": ...}`` dict on an
            API error.

        .. versionadded:: 1.0.0
        """
        return self._call_api(NOTES_CUSTOM_TYPES_V5, "get", {})

    def create_note_custom_type(self, **fields):
        """Add a custom note type.

        Sends ``POST /modules/api/v5.0/notes/custom-types`` with the keywords
        as the JSON body.

        :param fields: required: ``note_custom_type``, the name, and
            ``note_custom_type_values``, a list of strings. Optional:
            ``note_custom_field_type``: 1 select, 2 text, 3 numeric or
            4 integer.
        :return: the decoded JSON reply, or the ``{"errors": ...}`` dict on an
            API error.
        :raise ParamValueException: when a required field is missing.

        .. versionadded:: 1.0.0
        """
        require(fields, ["note_custom_type", "note_custom_type_values"])
        return self._call_api(NOTES_CUSTOM_TYPES_V5, "post", {}, body=fields)

    # ---------------------------------------------- V4 note custom types --

    def add_custom_note_type(self, note_custom_type=None, note_custom_type_values=None):
        """Add a custom note type, a list of values a driver picks from (API V4).

        Sends ``POST /api.v4/note_custom_types.php`` with ``type`` and
        ``values`` as the JSON body, the names the endpoint reads (as the C#
        and PHP SDKs send them; it rejects the spec's ``note_custom_type`` and
        ``note_custom_type_values``).

        :param note_custom_type: the name of the type.
        :param note_custom_type_values: the values, a non-empty list of strings.
        :return: the decoded JSON reply, e.g. ``{"result": "OK", "affected":
            1}``, or the ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when the name or the values are missing.

        .. versionadded:: 1.0.0
        """
        if not note_custom_type:
            raise ParamValueException("note_custom_type", "Missing required params")
        if not note_custom_type_values:
            raise ParamValueException("note_custom_type_values", "Missing required params")
        body = {"type": note_custom_type, "values": list(note_custom_type_values)}
        return self._call_api(NOTE_CUSTOM_TYPES_V4, "post", {}, body=body)

    def get_all_custom_note_types(self):
        """List the custom note types of the account (API V4).

        Sends ``GET /api.v4/note_custom_types.php``.

        :return: the decoded JSON reply, or the ``{"errors": ...}`` dict on an
            API error.

        .. versionadded:: 1.0.0
        """
        return self._call_api(NOTE_CUSTOM_TYPES_V4, "get", {})

    def remove_custom_note_type(self, note_custom_type_id):
        """Delete a custom note type (API V4).

        Sends ``DELETE /api.v4/note_custom_types.php`` with
        ``{"id": note_custom_type_id}`` as the JSON body.

        :param note_custom_type_id: ID of the custom note type, the
            ``note_custom_type_id`` that :meth:`get_all_custom_note_types`
            returns.
        :return: the decoded JSON reply, e.g. ``{"result": "OK", "affected":
            1}``, or the ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``note_custom_type_id`` is empty.

        .. versionadded:: 1.0.0
        """
        if note_custom_type_id is None or not str(note_custom_type_id).strip():
            raise ParamValueException("note_custom_type_id", "must not be empty")
        return self._call_api(NOTE_CUSTOM_TYPES_V4, "delete", {}, body={"id": note_custom_type_id})
