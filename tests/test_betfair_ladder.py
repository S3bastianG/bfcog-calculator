import pytest

from engine.betfair_ladder import previous_tick
from engine.betfair_ladder import next_tick


def test_one_tick_below_380():
    assert previous_tick(3.80) == 3.75


def test_two_ticks_below_380():
    assert previous_tick(3.80, 2) == 3.70


def test_one_tick_below_370():
    assert previous_tick(3.70) == 3.65


def test_one_tick_below_365():
    assert previous_tick(3.65) == 3.60


def test_crossing_400_boundary():
    assert previous_tick(4.10) == 4.00
    assert previous_tick(4.00) == 3.95


def test_invalid_odds():
    with pytest.raises(ValueError):
        previous_tick(3.81)


def test_zero_ticks():
    with pytest.raises(ValueError):
        previous_tick(3.80, 0)
        
def test_one_tick_above_380():
    assert next_tick(3.80) == 3.85


def test_two_ticks_above_380():
    assert next_tick(3.80, 2) == 3.90


def test_one_tick_above_400():
    assert next_tick(4.00) == 4.10
