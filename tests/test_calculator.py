import pytest

from engine.calculator import calculate_cs_trade


def test_calculate_cs_trade_example():

    result = calculate_cs_trade(
        back_stake=300,
        back_odds=3.80,
        odds_02=20,
        odds_12=10,
    )

    assert result["freebet"] == pytest.approx(36.75)

    assert result["stake_02"] == pytest.approx(
        36.75 / 19
    )

    assert result["stake_12"] == pytest.approx(
        36.75 / 9
    )


def test_cs_profit_equals_freebet():

    result = calculate_cs_trade(
        back_stake=300,
        back_odds=3.80,
        odds_02=20,
        odds_12=10,
    )

    freebet = result["freebet"]

    profit_02 = result["stake_02"] * (20 - 1)
    profit_12 = result["stake_12"] * (10 - 1)

    assert profit_02 == pytest.approx(freebet)
    assert profit_12 == pytest.approx(freebet)


def test_automatic_lay_plan():

    result = calculate_cs_trade(
        back_stake=300,
        back_odds=3.80,
        odds_02=20,
        odds_12=10,
    )

    plan = result["lay_plan"]

    assert plan[0].stake == pytest.approx(210)
    assert plan[0].odds == 3.70

    assert plan[1].stake == pytest.approx(45)
    assert plan[1].odds == 3.65

    assert plan[2].stake == pytest.approx(45)
    assert plan[2].odds == 3.60

def test_cs_stakes_below_betfair_minimum():

    result = calculate_cs_trade(
        back_stake=5,
        back_odds=4.10,
        odds_02=29,
        odds_12=13,
    )

    assert result["stake_02"] < 1
    assert result["stake_12"] < 1

    assert result["stake_02_executable"] is False
    assert result["stake_12_executable"] is False
