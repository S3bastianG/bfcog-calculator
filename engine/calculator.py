from engine.draw_trade import BackBet, LayBet, calculate_draw_freebet
from engine.lay_plan import calculate_lay_plan


def calculate_cs_trade(
    back_stake: float,
    back_odds: float,
    odds_02: float = 0.0,
    odds_12: float = 0.0,
    solo_x: bool = False,
) -> dict:
    """
    Calcola l'intera operazione:

    1. Crea automaticamente il piano Lay X:
       - 70% a -2 tick
       - 15% a -1 tick
       - 15% a -1 tick

    2. Calcola la freebet ottenuta sulla X.

    3. Calcola le stake CS in modo che il profitto
       di ciascun CS sia uguale alla freebet X.
    """

    if back_stake <= 0:
        raise ValueError("back_stake deve essere > 0")

    if back_odds <= 1.01:
        raise ValueError("back_odds deve essere > 1.01")
    if not solo_x:
        if odds_02 <= 1.01:
            raise ValueError("odds_02 deve essere > 1.01")

        if odds_12 <= 1.01:
            raise ValueError("odds_12 deve essere > 1.01")

    # --------------------------------------------------
    # 1. BACK X
    # --------------------------------------------------

    back_bet = BackBet(
        stake=back_stake,
        odds=back_odds,
    )

    # --------------------------------------------------
    # 2. PIANO LAY AUTOMATICO
    # --------------------------------------------------

    lay_plan = calculate_lay_plan(
        back_stake=back_stake,
        back_odds=back_odds,
    )

    lay_bets = [
        LayBet(
            stake=lay.stake,
            odds=lay.odds,
        )
        for lay in lay_plan
    ]

    # --------------------------------------------------
    # 3. FREEBET X
    # --------------------------------------------------

    freebet = calculate_draw_freebet(
        back_bet=back_bet,
        lay_bets=lay_bets,
    )

    # --------------------------------------------------
    # 4. STAKE CORRECT SCORE
    # --------------------------------------------------

    if solo_x:
        stake_02 = 0.0
        stake_12 = 0.0
        stake_02_executable = True
        stake_12_executable = True
    else:
        stake_02 = freebet / (odds_02 - 1)
        stake_12 = freebet / (odds_12 - 1)

        MIN_BET_STAKE = 1.00

        stake_02_executable = stake_02 >= MIN_BET_STAKE
        stake_12_executable = stake_12 >= MIN_BET_STAKE



    return {
        "freebet": freebet,
        "stake_02": stake_02,
        "stake_12": stake_12,
        "stake_02_executable": stake_02_executable,
        "stake_12_executable": stake_12_executable,
        "lay_plan": lay_plan,
    }

def calculate_minimum_back_stake(
    back_odds: float,
    odds_02: float,
    odds_12: float,
    min_cs_stake: float = 1.00,
) -> dict:
    """
    Calcola la stake X minima necessaria affinché entrambe
    le stake CS raggiungano almeno min_cs_stake.

    La freebet target viene determinata dalla CS che richiede
    la maggiore freebet per raggiungere la stake minima.

    Esempio:

        CS 0-2 @ 23
        CS 1-2 @ 13
        minimo stake = €1

        target freebet:
        max(1 * (23 - 1), 1 * (13 - 1))
        = €22
    """

    if back_odds <= 1.01:
        raise ValueError("back_odds deve essere > 1.01")

    if odds_02 <= 1.01:
        raise ValueError("odds_02 deve essere > 1.01")

    if odds_12 <= 1.01:
        raise ValueError("odds_12 deve essere > 1.01")

    if min_cs_stake <= 0:
        raise ValueError("min_cs_stake deve essere > 0")

    # --------------------------------------------------
    # FREEBET MINIMA NECESSARIA
    # --------------------------------------------------

    required_freebet_02 = min_cs_stake * (odds_02 - 1)
    required_freebet_12 = min_cs_stake * (odds_12 - 1)

    target_freebet = max(
        required_freebet_02,
        required_freebet_12,
    )

    # --------------------------------------------------
    # CALCOLO FREEBET PER €1 DI BACK X
    # --------------------------------------------------

    reference_result = calculate_cs_trade(
        back_stake=1.00,
        back_odds=back_odds,
        odds_02=odds_02,
        odds_12=odds_12,
    )

    freebet_per_unit = reference_result["freebet"]

    if freebet_per_unit <= 0:
        raise ValueError(
            "Impossibile calcolare una freebet positiva."
        )

    # --------------------------------------------------
    # STAKE X MINIMA
    # --------------------------------------------------

    minimum_back_stake = (
        target_freebet / freebet_per_unit
    )

    # --------------------------------------------------
    # VERIFICA REALE
    # --------------------------------------------------

    verification = calculate_cs_trade(
        back_stake=minimum_back_stake,
        back_odds=back_odds,
        odds_02=odds_02,
        odds_12=odds_12,
    )

    return {
        "minimum_back_stake": minimum_back_stake,
        "target_freebet": target_freebet,
        "required_freebet_02": required_freebet_02,
        "required_freebet_12": required_freebet_12,
        "result": verification,
    }
