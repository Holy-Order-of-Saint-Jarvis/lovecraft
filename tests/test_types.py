# coding: utf-8

import pytest
from lovecraft import types


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


def test_portal_kwargs():
    p = types.Portal(title='testing')
    assert p.title == 'testing'
    assert p.owner is None
    assert p.faction is None
    assert p.resonators == {}

    p = types.Portal(title='testing', owner='bob', faction=types.Faction.ENL)
    assert p.title == 'testing'
    assert p.owner == 'bob'
    assert p.faction == types.Faction.ENL
    assert p.resonators == {}


def test_portal_posargs():
    p = types.Portal('testing')
    assert p.title == 'testing'
    assert p.owner is None
    assert p.faction is None
    assert p.resonators == {}

    p = types.Portal('testing', types.Faction.ENL, 'bob')
    assert p.title == 'testing'
    assert p.faction == types.Faction.ENL
    assert p.owner == 'bob'
    assert p.resonators == {}


def test_portal_validate_resonators():
    reso = types.Resonator(owner='bob', level=8)
    with pytest.raises(TypeError):
        # invalid position
        types.Portal(title='testing', resonators={'answer': reso})

    with pytest.raises(TypeError):
        # invalid reso
        types.Portal(title='testing', resonators={types.Orientation.NORTH: 0})


def test_portal_deploy():
    p = types.Portal('testing')
    assert p.title == 'testing'
    assert p.owner is None
    assert p.faction is None
    assert p.resonators == {}

    p2 = p.deploy(agent='bob',
                  faction=types.Faction.ENL,
                  position=types.Orientation.NORTH,
                  level=8)
    assert p2.title == 'testing'
    assert p2.faction == types.Faction.ENL
    assert p2.owner == 'bob'
    assert p2.resonators == {
        types.Orientation.NORTH:
            types.Resonator(owner='bob',
                            level=8)}

    p3 = p2.deploy('alice', types.Faction.ENL, types.Orientation.SOUTH, 8)
    assert p3.title == 'testing'
    assert p3.faction == types.Faction.ENL
    assert p3.owner == 'bob'
    assert p3.resonators == {
        types.Orientation.NORTH:
            types.Resonator(owner='bob', level=8),
        types.Orientation.SOUTH:
            types.Resonator(owner='alice', level=8),
    }

    with pytest.raises(ValueError):
        # can't deploy lower-level reso
        p3.deploy('bob', types.Faction.ENL, types.Orientation.NORTH, 7)


def test_portal_damage():
    p = types.Portal(title='testing')
    p = p.deploy('bob', types.Faction.ENL, types.Orientation.NORTH, 8)

    p2 = p.damage(types.Orientation.NORTH, 77)
    assert p2.title == 'testing'
    assert p2.owner == 'bob'
    assert p2.faction == types.Faction.ENL
    assert p2.resonators == {
        types.Orientation.NORTH:
            types.Resonator(owner='bob', level=8, health=23)}

    p3 = p2.damage(types.Orientation.NORTH, 50)
    assert p3.title == 'testing'
    assert p3.owner is None
    assert p3.faction is None
    assert p3.resonators == {}

    p4 = p3.damage(types.Orientation.NORTH, 100)
    assert p4 == p3
