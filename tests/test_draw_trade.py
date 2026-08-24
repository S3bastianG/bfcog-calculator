import pytest

from engine.draw_trade import BackBet, LayBet, calculate_draw_freebet
from engine.correct_score import calculate_cs_stakes
from engine.pnl import calculate_total_pnl
from engine.correct_score import calculate_balanced_cs_stakes
from engine.calculator import calculate_minimum_back_stake



def test_example_freebet():

    back = BackBet(
        stake=300,
        odds=3.80,
    )

    lays = [
        LayBet(stake=210, odds=3.70),
        LayBet(stake=45, odds=3.65),
        LayBet(stake=45, odds=3.60),
    ]

    freebet = calculate_draw_freebet(back, lays)

    assert freebet == pytest.approx(36.75)


def test_example_cs_stakes():

    freebet = 36.75

    stake_02, stake_12 = calculate_cs_stakes(
        freebet=freebet,
        odds_02=20,
        odds_12=10,
    )

    assert stake_02 == pytest.approx(1.9342105263)
    assert stake_12 == pytest.approx(4.0833333333)

def test_total_pnl_example():

    back_stake = 300
    back_odds = 3.80

    lays = [
        LayBet(stake=210, odds=3.70),
        LayBet(stake=45, odds=3.65),
        LayBet(stake=45, odds=3.60),
    ]

    stake_02, stake_12 = calculate_balanced_cs_stakes(
        freebet=36.75,
        odds_02=20,
        odds_12=10,
    )


    pnl_02 = calculate_total_pnl(
        score="0-2",
        back_stake=back_stake,
        back_odds=back_odds,
        lay_bets=lays,
        stake_02=stake_02,
        odds_02=20,
        stake_12=stake_12,
        odds_12=10,
    )

    pnl_12 = calculate_total_pnl(
        score="1-2",
        back_stake=back_stake,
        back_odds=back_odds,
        lay_bets=lays,
        stake_02=stake_02,
        odds_02=20,
        stake_12=stake_12,
        odds_12=10,
    )

    assert pnl_02 == pytest.approx(36.75)
    assert pnl_12 == pytest.approx(36.75)


def test_balanced_cs_stakes():

    freebet = 36.75

    stake_02, stake_12 = calculate_balanced_cs_stakes(
        freebet=freebet,
        odds_02=20,
        odds_12=10,
    )

    assert stake_02 == pytest.approx(2.1617647)
    assert stake_12 == pytest.approx(4.3235294)


def test_calculate_draw_freebet():

    back = BackBet(
        stake=300,
        odds=3.80,
    )

    lays = [
        LayBet(stake=210, odds=3.70),
        LayBet(stake=45, odds=3.65),
        LayBet(stake=45, odds=3.60),
    ]

    freebet = calculate_draw_freebet(
        back_bet=back,
        lay_bets=lays,
    )

    assert freebet == pytest.approx(36.75)

def test_minimum_back_stake_target_is_highest_cs_requirement():

    result = calculate_minimum_back_stake(
        back_odds=4.10,
        odds_02=23,
        odds_12=13,
    )

    assert result["target_freebet"] == pytest.approx(22.00)

    assert result["required_freebet_02"] == pytest.approx(22.00)

    assert result["required_freebet_12"] == pytest.approx(12.00)


def test_minimum_back_stake_produces_executable_cs():

    result = calculate_minimum_back_stake(
        back_odds=4.10,
        odds_02=23,
        odds_12=13,
    )

    trade = result["result"]

    assert trade["stake_02"] >= 1.00
    assert trade["stake_12"] >= 1.00

    assert trade["freebet"] == pytest.approx(22.00)
