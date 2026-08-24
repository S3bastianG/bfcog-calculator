"""
Betfair Classic Odds Ladder.

Gestisce i tick della ladder Betfair:
- previous_tick(odds)      -> quota 1 tick più bassa
- previous_tick(odds, n)   -> quota n tick più bassa
"""

BETFAIR_LADDER = [
    # 1.01 - 2.00
    *[round(1.01 + i * 0.01, 2) for i in range(100)],

    # 2.02 - 3.00
    *[round(2.02 + i * 0.02, 2) for i in range(50)],

    # 3.05 - 4.00
    *[round(3.05 + i * 0.05, 2) for i in range(20)],

    # 4.10 - 6.00
    *[round(4.10 + i * 0.10, 2) for i in range(20)],

    # 6.20 - 10.00
    *[round(6.20 + i * 0.20, 2) for i in range(20)],

    # 10.50 - 20.00
    *[round(10.50 + i * 0.50, 2) for i in range(20)],

    # 21 - 30
    *[float(21 + i) for i in range(10)],

    # 32 - 50
    *[float(32 + i * 2) for i in range(10)],

    # 55 - 100
    *[float(55 + i * 5) for i in range(10)],

    # 110 - 1000
    *[float(110 + i * 10) for i in range(90)],
]


def previous_tick(odds: float, ticks: int = 1) -> float:
    """
    Restituisce la quota di `ticks` tick inferiore
    rispetto alla quota indicata.

    Esempi:

        previous_tick(3.80)
        -> 3.75

        previous_tick(3.80, 2)
        -> 3.70

        previous_tick(3.70)
        -> 3.65
    """

    if ticks < 1:
        raise ValueError("ticks deve essere >= 1")

    odds = round(float(odds), 2)

    try:
        index = BETFAIR_LADDER.index(odds)
    except ValueError:
        raise ValueError(
            f"La quota {odds:.2f} non è una quota valida della ladder Betfair"
        )

    new_index = index - ticks

    if new_index < 0:
        raise ValueError(
            f"Impossibile scendere di {ticks} tick da quota {odds:.2f}"
        )

    return BETFAIR_LADDER[new_index]

def next_tick(odds: float, ticks: int = 1) -> float:
    """
    Restituisce la quota di `ticks` tick superiore
    rispetto alla quota indicata.
    """

    if ticks < 1:
        raise ValueError("ticks deve essere >= 1")

    odds = round(float(odds), 2)

    try:
        index = BETFAIR_LADDER.index(odds)
    except ValueError:
        raise ValueError(
            f"La quota {odds:.2f} non è una quota valida della ladder Betfair"
        )

    new_index = index + ticks

    if new_index >= len(BETFAIR_LADDER):
        raise ValueError(
            f"Impossibile salire di {ticks} tick da quota {odds:.2f}"
        )

    return BETFAIR_LADDER[new_index]
