def calculate_cs_stake(
    freebet: float,
    odds: float,
) -> float:
    """
    Metodo semplice:
    il profitto della singola puntata CS
    è uguale alla freebet.
    """

    if odds <= 1:
        raise ValueError("La quota deve essere maggiore di 1.")

    if freebet < 0:
        raise ValueError("La freebet non può essere negativa.")

    return freebet / (odds - 1)


def calculate_cs_stakes(
    freebet: float,
    odds_02: float,
    odds_12: float,
) -> tuple[float, float]:
    """
    Vecchio metodo:
    il profitto della singola puntata CS
    è uguale alla freebet.
    """

    stake_02 = calculate_cs_stake(
        freebet,
        odds_02,
    )

    stake_12 = calculate_cs_stake(
        freebet,
        odds_12,
    )

    return stake_02, stake_12


def calculate_balanced_cs_stakes(
    freebet: float,
    odds_02: float,
    odds_12: float,
) -> tuple[float, float]:
    """
    Metodo attuale.

    Calcola le stake in modo che:

        P&L netto 0-2 = freebet
        P&L netto 1-2 = freebet
    """

    if freebet < 0:
        raise ValueError(
            "La freebet non può essere negativa."
        )

    if odds_02 <= 1 or odds_12 <= 1:
        raise ValueError(
            "Le quote CS devono essere maggiori di 1."
        )

    a = odds_02 - 1
    b = odds_12 - 1

    denominator = (a * b) - 1

    if denominator <= 0:
        raise ValueError(
            "Le quote CS non consentono "
            "una soluzione valida."
        )

    stake_02 = freebet * (b + 1) / denominator
    stake_12 = freebet * (a + 1) / denominator

    return stake_02, stake_12
