from dataclasses import dataclass


@dataclass
class ScorelinePosition:
    score: str
    pnl: float


def back_pnl(stake: float, odds: float, wins: bool) -> float:
    """
    P&L di una puntata BACK.

    Se vince:
        stake * (odds - 1)

    Se perde:
        -stake
    """
    if wins:
        return stake * (odds - 1)

    return -stake


def lay_pnl(stake: float, odds: float, wins: bool) -> float:
    """
    P&L di una puntata LAY.

    Se l'evento NON avviene:
        +stake

    Se l'evento avviene:
        -liability
    """
    if wins:
        return -stake * (odds - 1)

    return stake


def calculate_draw_pnl(
    back_stake: float,
    back_odds: float,
    lay_bets: list,
    draw_happens: bool,
) -> float:
    """
    Calcola il P&L complessivo della posizione sulla X.
    """

    pnl = back_pnl(
        stake=back_stake,
        odds=back_odds,
        wins=draw_happens,
    )

    for lay in lay_bets:
        pnl += lay_pnl(
            stake=lay.stake,
            odds=lay.odds,
            wins=draw_happens,
        )

    return pnl


def calculate_cs_pnl(
    stake_02: float,
    odds_02: float,
    stake_12: float,
    odds_12: float,
    score: str,
) -> float:
    """
    Calcola il P&L delle due puntate Correct Score
    per uno specifico risultato.
    """

    pnl = 0.0

    # Correct Score 0-2
    if score == "0-2":
        pnl += stake_02 * (odds_02 - 1)
    else:
        pnl -= stake_02

    # Correct Score 1-2
    if score == "1-2":
        pnl += stake_12 * (odds_12 - 1)
    else:
        pnl -= stake_12

    return pnl


def calculate_total_pnl(
    score: str,
    back_stake: float,
    back_odds: float,
    lay_bets: list,
    stake_02: float,
    odds_02: float,
    stake_12: float,
    odds_12: float,
) -> float:
    """
    Calcola il P&L totale della strategia
    per uno specifico scoreline.
    """

    home_goals, away_goals = map(int, score.split("-"))

    draw_happens = home_goals == away_goals

    draw_pnl = calculate_draw_pnl(
        back_stake=back_stake,
        back_odds=back_odds,
        lay_bets=lay_bets,
        draw_happens=draw_happens,
    )

    cs_pnl = calculate_cs_pnl(
        stake_02=stake_02,
        odds_02=odds_02,
        stake_12=stake_12,
        odds_12=odds_12,
        score=score,
    )

    return draw_pnl + cs_pnl
