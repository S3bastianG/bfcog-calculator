import pytest

from engine.lay_plan import calculate_lay_plan


def test_lay_plan_example():

    plan = calculate_lay_plan(
        back_stake=300,
        back_odds=3.80,
    )

    assert len(plan) == 3

    assert plan[0].stake == pytest.approx(210)
    assert plan[0].odds == 3.70

    assert plan[1].stake == pytest.approx(45)
    assert plan[1].odds == 3.65

    assert plan[2].stake == pytest.approx(45)
    assert plan[2].odds == 3.60


def test_lay_plan_total_stake():

    plan = calculate_lay_plan(
        back_stake=300,
        back_odds=3.80,
    )

    total = sum(lay.stake for lay in plan)

    assert total == pytest.approx(300)


def test_lay_plan_invalid_stake():

    with pytest.raises(ValueError):
        calculate_lay_plan(
            back_stake=0,
            back_odds=3.80,
        )


def test_lay_plan_invalid_odds():

    with pytest.raises(ValueError):
        calculate_lay_plan(
            back_stake=300,
            back_odds=1.01,
        )
