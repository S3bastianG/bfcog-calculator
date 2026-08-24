import pytest

from engine.draw_trade import BackBet, LayBet
from engine.correct_score import calculate_balanced_cs_stakes
from engine.simulator import simulate_scorelines


def test_simulator():

    back = BackBet(
        stake=300,
        odds=3.80,
    )

    lays = [
        LayBet(stake=210, odds=3.70),
        LayBet(stake=45, odds=3.65),
        LayBet(stake=45, odds=3.60),
    ]

    freebet = 36.75

    stake_02, stake_12 = calculate_balanced_cs_stakes(
        freebet=freebet,
        odds_02=20,
        odds_12=10,
    )

    results = simulate_scorelines(
        back_stake=back.stake,
        back_odds=back.odds,
        lay_bets=lays,
        stake_02=stake_02,
        odds_02=20,
        stake_12=stake_12,
        odds_12=10,
    )

    assert len(results) == 9

    assert results["0-2"] == pytest.approx(36.75)
    assert results["1-2"] == pytest.approx(36.75)
