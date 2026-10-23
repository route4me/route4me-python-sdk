"""The :class:`AdvancedConstraint` model for an optimization's ``advanced_constraints``."""

from dataclasses import dataclass, field
from typing import Optional

from .utils import clean_dict


@dataclass
class AdvancedConstraint:
    """One advanced constraint: limits and resources for a group of routes.

    Pass a list of ``constraint.to_dict()`` results to
    :meth:`Optimization.advanced_constraints
    <route4me.base.Base.advanced_constraints>`.

    :param max_cargo_weight: maximum cargo weight per route.
    :param max_cargo_volume: maximum cargo volume per route.
    :param max_capacity: maximum cargo per route, in capacity units.
    :param members_count: number of routes (drivers) this constraint applies
        to.
    :param vehicles_id: IDs of the vehicles available.
    :param available_time_windows: available time windows, as ``[start,
        end]`` pairs in seconds, e.g. ``[[25200, 75000]]``.
    :param tags: driver tags; only drivers with these tags are used.
    :param route4me_members_id: IDs of the members (drivers) available.
    :param depot_address: the depot: ``alias``, ``address``, ``lat`` and
        ``lng``.
    :param location_sequence_pattern: locations in the order the routes must
        visit them.
    :param group: name of the constraint group.
    """

    max_cargo_weight: Optional[float] = None
    max_cargo_volume: Optional[float] = None
    max_capacity: Optional[int] = None
    members_count: int = 10
    vehicles_id: list = field(default_factory=list)
    available_time_windows: list = field(default_factory=list)
    tags: list = field(default_factory=list)
    route4me_members_id: list = field(default_factory=list)
    depot_address: dict = field(
        default_factory=lambda: {
            "alias": None,
            "address": None,
            "lat": None,
            "lng": None,
        }
    )
    location_sequence_pattern: list = field(default_factory=list)
    group: Optional[str] = None

    def to_dict(self):
        """Return the constraint as a dict for the request body.

        Fields that are ``None`` or empty are left out (see
        :func:`~route4me.utils.clean_dict`).

        :return: the constraint's fields, or ``None`` when none is set.
        """
        return clean_dict(self.__dict__)
