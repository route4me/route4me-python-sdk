"""The :class:`Bundling` model and its mode constants, for an optimization's ``bundling`` parameter."""

from dataclasses import dataclass, field

from .constants import enum

BUNDLING_MODE = enum(BY_ADDRESS=1, BY_COORDINATES=2, BY_STATIC_FIELD=3, BY_CUSTOM_DATA=4)

BUNDLING_MERGE_MODE = enum(KEEP_SEPARATED=1, MERGE_INTO_SINGLE=2)

BUNDLING_FIRST_ITEM_MODE = enum(KEEP_ORIGINAL_SERVICE_TIME=1, USE_CUSTOM_SERVICE_TIME=2)

BUNDLING_ADDITIONAL_ITEM_MODE = enum(KEEP_ORIGINAL_SERVICE_TIME=1, USE_CUSTOM_SERVICE_TIME=2, DO_NOT_ADD_SERVICE_TIME=3)


class ServiceTimeRules(dict):
    """How service time is counted for the stops of a bundle.

    ``first_item_mode`` is a :data:`BUNDLING_FIRST_ITEM_MODE` value for the
    first stop of a bundle, and ``additional_items_mode`` a
    :data:`BUNDLING_ADDITIONAL_ITEM_MODE` value for the others. The
    ``*_params`` lists hold the custom service times, in seconds, used by the
    ``USE_CUSTOM_SERVICE_TIME`` modes.
    """

    first_item_mode = None
    first_item_mode_params = []
    additional_items_mode = None
    additional_items_mode_params = []

    def __init__(self):
        pass

    def to_dict(self):
        """Return the rules as a dict.

        :return: the rules.
        """
        return self.__dict__


@dataclass
class Bundling:
    """Settings for bundling stops, i.e. serving several stops as one.

    Pass ``Bundling().to_dict()`` to :meth:`Optimization.bundling
    <route4me.base.Base.bundling>`.

    :param mode: what makes stops a bundle: a :data:`BUNDLING_MODE` value.
    :param merge_mode: whether a bundle stays separate stops or becomes one: a
        :data:`BUNDLING_MERGE_MODE` value.
    :param mode_params: parameters of ``mode``: the address field names for
        ``BUNDLING_MODE.BY_STATIC_FIELD``, or the custom field names for
        ``BUNDLING_MODE.BY_CUSTOM_DATA``.
    :param service_time_rules: how service time is counted for a bundle.
    """

    mode: int = BUNDLING_MODE.BY_ADDRESS
    merge_mode: int = BUNDLING_MERGE_MODE.KEEP_SEPARATED
    mode_params: list = field(default_factory=list)
    service_time_rules: ServiceTimeRules = field(default_factory=ServiceTimeRules)

    def to_dict(self):
        """Return the settings as a dict for the request body.

        :return: the settings, keyed by field name.
        """
        return self.__dict__
