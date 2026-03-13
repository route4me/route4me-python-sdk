# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from typing import Optional

from .utils import clean_dict


@dataclass
class AdvancedConstraint:

    max_cargo_weight: Optional[float] = None
    max_cargo_volume: Optional[float] = None
    max_capacity: Optional[int] = None
    members_count: int = 10
    vehicles_id: list = field(default_factory=list)
    available_time_windows: list = field(default_factory=list)
    tags: list = field(default_factory=list)
    route4me_members_id: list = field(default_factory=list)
    depot_address: dict = field(default_factory=lambda: {
        "alias": None,
        "address": None,
        "lat": None,
        "lng": None,
    })
    location_sequence_pattern: list = field(default_factory=list)
    group: Optional[str] = None

    def to_dict(self):
        return clean_dict(self.__dict__)
