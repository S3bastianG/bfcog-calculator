from dataclasses import dataclass

from engine.betfair_ladder import previous_tick


@dataclass(frozen=True)
class LayPlan:
    stake: float
    odds: float
    percentage: float


def calculate_lay_plan(
    back_stake: float,
    back_odds: float
) -> list[LayPlan]:
    """
    Crea il piano Lay X:

    70% dello stake a -2 tick
    20% dello stake a -2 tick
    10% dello stake a -6 tick

    Esempio:
        Back 300 @ 3.80

        -> 210 @ 3.70
        -> 60  @ 3.60
        -> 30  @ 3.30
    """

    if back_stake <= 0:
        raise ValueError("back_stake deve essere > 0")

    if back_odds <= 1.01:
        raise ValueError("back_odds deve essere > 1.01")

    stake_70 = back_stake * 0.70
    stake_20 = back_stake * 0.20
    stake_10 = back_stake * 0.10

    odds_1 = previous_tick(back_odds, 2)
    odds_2 = previous_tick(odds_1, 2)
    odds_3 = previous_tick(odds_2, 6)

    return [
        LayPlan(stake=stake_70, odds=odds_1, percentage=70),
        LayPlan(stake=stake_20, odds=odds_2, percentage=20),
        LayPlan(stake=stake_10, odds=odds_3, percentage=10),
    ]
