from dataclasses import dataclass


@dataclass
class BackBet:
    stake: float
    odds: float


@dataclass
class LayBet:
    stake: float
    odds: float


def calculate_draw_freebet(back: BackBet, lays: list[LayBet]) -> float:
    """
    Calcola il profitto residuo sulla X dopo tutte le bancate.

    Back X:
        profitto = stake * (odds - 1)

    Lay X:
        liability = stake * (odds - 1)

    Il risultato positivo viene considerato la 'freebet' residua sulla X.
    """

    back_profit = back.stake * (back.odds - 1)

    total_lay_liability = sum(
        lay.stake * (lay.odds - 1)
        for lay in lays
    )

    return back_profit - total_lay_liability


def calculate_draw_freebet(
    back_bet: BackBet,
    lay_bets: list[LayBet],
) -> float:
    """
    Calcola il profitto netto sulla X
    quando il pareggio si verifica.

    La freebet è il P&L positivo ottenuto
    se esce la X dopo le bancate progressive.
    """

    pnl = back_bet.stake * (back_bet.odds - 1)

    for lay in lay_bets:
        pnl -= lay.stake * (lay.odds - 1)

    return pnl
