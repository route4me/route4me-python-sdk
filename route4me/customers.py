"""The :class:`Customers` resource (API V5): create, read, update and delete customers."""

from ._url import path_segment
from .api_endpoints import CUSTOMERS_V5
from .base import Base
from .exceptions import ParamValueException


class Customers(Base):
    """Customers: the businesses an account delivers to (API V5).

    Use it as ``route4me.customers``. Every method sends a request to
    ``/modules/api/v5.0/customers`` on ``wh.route4me.com``. The methods mirror
    ``CustomerManagerV5`` of the C# SDK.

    Unless stated otherwise, a method returns the decoded JSON reply, or on an
    API error the ``{"errors": ...}`` dict from :meth:`APIException.to_dict
    <route4me.exceptions.APIException.to_dict>` instead of raising.

    .. versionadded:: 1.0.0
    """

    @staticmethod
    def _customer_url(customer_id):
        """Build the URL of one customer, with ``customer_id`` encoded as one path segment.

        :param customer_id: ID of the customer.
        :return: the absolute URL.
        :raise ParamValueException: when ``customer_id`` is empty.
        """
        return f"{CUSTOMERS_V5}/{path_segment(customer_id, 'customer_id')}"

    def create_customer(self, **kwargs):
        """Create a customer.

        Sends ``POST /modules/api/v5.0/customers`` with the keywords as the
        JSON body.

        :param kwargs: the customer fields. Required: ``name`` and
            ``accountable_person_id``, the member accountable for the customer.
            Optional fields include ``external_id``, ``contacts``,
            ``addresses``, ``currency``, ``tax_id``, ``status`` (``1`` active,
            ``0`` inactive), ``facility_ids``, ``asset_ids`` and
            ``custom_data``.
        :return: the decoded JSON reply: the new customer, or the
            ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when a required field is missing.

        .. versionadded:: 1.0.0
        """
        missing = self._missing(kwargs, ("name", "accountable_person_id"))
        if missing:
            raise ParamValueException(", ".join(missing), "Missing required params")
        return self._call_api(CUSTOMERS_V5, "post", {}, body=kwargs)

    def get_customer_by_id(self, customer_id):
        """Get one customer.

        Sends ``GET /modules/api/v5.0/customers/{customer_id}``.

        :param customer_id: ID of the customer.
        :return: the decoded JSON reply: the customer, or the
            ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``customer_id`` is empty.

        .. versionadded:: 1.0.0
        """
        return self._call_api(self._customer_url(customer_id), "get", {})

    def update_customer(self, customer_id, **kwargs):
        """Update a customer.

        Sends ``PUT /modules/api/v5.0/customers/{customer_id}`` with the
        keywords as the JSON body.

        :param customer_id: ID of the customer.
        :param kwargs: the fields to change, with the names of
            :meth:`create_customer`.
        :return: the decoded JSON reply: the updated customer, or the
            ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``customer_id`` is empty.

        .. versionadded:: 1.0.0
        """
        return self._call_api(self._customer_url(customer_id), "put", {}, body=kwargs)

    def delete_customer(self, customer_id):
        """Delete a customer.

        Sends ``DELETE /modules/api/v5.0/customers/{customer_id}``. The API
        answers ``204 No Content`` on success.

        :param customer_id: ID of the customer.
        :return: the reply body: empty (``b""``) on success, or the
            ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``customer_id`` is empty.

        .. versionadded:: 1.0.0
        """
        return self._request_decoded(self._customer_url(customer_id), {}, "delete")
