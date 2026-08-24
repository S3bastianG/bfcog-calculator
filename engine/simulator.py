from engine.pnl import calculate_total_pnl
from engine.scorelines import generate_scorelines


def simulate_scorelines(
    back_stake: float,
    back_odds: float,
    lay_bets: list,
    stake_02: float,
    odds_02: float,
    stake_12: float,
    odds_12: float,
) -> dict[str, float]:

    results = {}

    for score in generate_scorelines():
        results[score] = calculate_total_pnl(
            score=score,
            back_stake=back_stake,
            back_odds=back_odds,
            lay_bets=lay_bets,
            stake_02=stake_02,
            odds_02=odds_02,
            stake_12=stake_12,
            odds_12=odds_12,
        )

    return results
