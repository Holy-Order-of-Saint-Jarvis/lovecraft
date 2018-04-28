# coding: utf-8

from lovecraft import types

import pytest


def test_orientation():
    known = set([
        types.Orientation.NORTH,
        types.Orientation.EAST,
        types.Orientation.SOUTH,
        types.Orientation.WEST,
        types.Orientation.NORTHEAST,
        types.Orientation.SOUTHEAST,
        types.Orientation.SOUTHWEST,
        types.Orientation.NORTHWEST,
    ])
    all_values = set(types.Orientation)
    assert known == all_values


def test_faction():
    assert types.Faction.ENL.value == 'Enlightened'
    assert types.Faction.RES.value == 'Resistance'
    assert types.Faction.ENL.abbreviation == 'ENL'
    assert types.Faction.RES.abbreviation == 'RES'


def test_resonator_kwargs():
    l1 = types.Resonator(owner='bob', level=1)

    assert l1.owner == 'bob'
    assert l1.level == 1
    assert l1.health == 100

    l4 = types.Resonator(health=7, level=4, owner='bob')

    assert l4.owner == 'bob'
    assert l4.level == 4
    assert l4.health == 7

    with pytest.raises(TypeError):
        # level must be specified
        types.Resonator(owner='bob')

    with pytest.raises(TypeError):
        # owner must be specified
        types.Resonator(level=4)


def test_resonator_posargs():
    l1 = types.Resonator('bob', 1)

    assert l1.owner == 'bob'
    assert l1.level == 1
    assert l1.health == 100

    l4 = types.Resonator('bob', 4, 7)

    assert l4.owner == 'bob'
    assert l4.level == 4
    assert l4.health == 7

    with pytest.raises(TypeError):
        # owner and level must be specified
        types.Resonator('bob')


def test_resonator_validate_agentname():
    with pytest.raises(TypeError):
        types.Resonator(owner=42, level=8)

    with pytest.raises(ValueError):
        types.Resonator(owner='invalid_agent_name', level=8)


def test_resonator_validate_level():
    with pytest.raises(TypeError):
        # not an integer
        types.Resonator(owner='bob', level=None)

    with pytest.raises(ValueError):
        # lower than 1
        types.Resonator(owner='bob', level=0)

    with pytest.raises(ValueError):
        # higher than 8
        types.Resonator(owner='bob', level=10)


def test_resonator_validate_health():
    with pytest.raises(TypeError):
        types.Resonator(owner='bob', level=1, health='healthy')

    with pytest.raises(ValueError):
        types.Resonator(owner='bob', level=1, health=0)

    with pytest.raises(ValueError):
        types.Resonator(owner='bob', level=1, health=999)
