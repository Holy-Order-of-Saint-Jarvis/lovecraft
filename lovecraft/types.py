# coding: utf-8

from enum import Enum
import re
from typing import Dict

import attr


class Orientation(str, Enum):
    NORTH = 'N'
    EAST = 'E'
    SOUTH = 'S'
    WEST = 'W'
    NORTHEAST = 'NE'
    SOUTHEAST = 'SE'
    SOUTHWEST = 'SW'
    NORTHWEST = 'NW'


class Faction(str, Enum):
    ENL = 'Enlightened'
    RES = 'Resistance'

    @property
    def abbreviation(self):
        return self.value[:3].upper()


@attr.s(slots=True, frozen=True, auto_attribs=True)
class Resonator(object):
    owner: str = attr.ib()
    level: int = attr.ib()
    health: int = attr.ib(default=100)

    @owner.validator
    def _check_owner(self, attribute, value):
        attr.validators.instance_of(str)(self, attribute, value)
        if not re.match(r'^[a-zA-Z0-9-]+$', value):
            raise ValueError(f"invalid agent name '{value}'")

    @level.validator
    def _check_level(self, attribute, value):
        attr.validators.instance_of(int)(self, attribute, value)
        if value < 1 or value > 8:
            raise ValueError('level must be between 1 and 8, inclusive')

    @health.validator
    def _check_health(self, attribute, value):
        attr.validators.instance_of(int)(self, attribute, value)
        if value <= 0 or value > 100:
            raise ValueError('health must be between 1 and 100, inclusive')


@attr.s(slots=True, frozen=True, auto_attribs=True)
class Portal(object):
    title: str = attr.ib(validator=attr.validators.instance_of(str))
    faction: Faction = attr.ib(default=None)
    owner: str = attr.ib(default=None)
    resonators: Dict[Orientation, Resonator] = attr.ib(
            default=attr.Factory(dict))

    @faction.validator
    def _check_faction(self, attribute, value):
        inst = attr.validators.instance_of(Faction)
        attr.validators.optional(inst)(self, attribute, value)

    @owner.validator
    def _check_owner(self, attribute, value):
        inst = attr.validators.instance_of(str)
        attr.validators.optional(inst)(self, attribute, value)
        if value is not None:
            Resonator(owner=value, level=1, health=100)

    @resonators.validator
    def _check_resonators(self, attribute, value):
        attr.validators.instance_of(dict)(self, attribute, value)
        for position, reso in value.items():
            if not isinstance(position, Orientation):
                raise TypeError(f"invalid position '{position}'")
            if not isinstance(reso, Resonator):
                raise TypeError(f"invalid resonator '{reso}'")

    def deploy(self,
               agent: str,
               faction: Faction,
               position: Orientation,
               level: int) -> 'Portal':
        reso = Resonator(owner=agent, level=level)

        existing = self.resonators.get(position)

        if existing and existing.level >= reso.level:
            raise ValueError('higher-level resonator already deployed')

        if len(self.resonators) == 0 and not self.owner and not self.faction:
            # initial capture!
            owner = agent
            faction = faction
        else:
            owner = self.owner
            faction = self.faction

        resos = {}
        resos.update(self.resonators)
        resos[position] = reso
        return attr.evolve(self,
                           owner=owner,
                           faction=faction,
                           resonators=resos)

    def damage(self, position: Orientation, amount: int) -> 'Portal':
        reso = self.resonators.get(position)
        if not reso:
            return self

        try:
            reso = attr.evolve(reso, health=reso.health - amount)
        except ValueError:
            reso = None

        resos = {}
        resos.update(self.resonators)
        if reso:
            resos[position] = reso
        else:
            del resos[position]

        if len(resos) == 0:
            owner = None
            faction = None
        else:
            owner = self.owner
            faction = self.faction
        return attr.evolve(self,
                           resonators=resos,
                           owner=owner,
                           faction=faction)
