from engine.draw_trade import BackBet, LayBet
from engine.correct_score import calculate_balanced_cs_stakes
from engine.simulator import simulate_scorelines


def main():

    # Posizione X
    back = BackBet(
        stake=300,
        odds=3.80,
    )

    lays = [
        LayBet(stake=210, odds=3.70),
        LayBet(stake=45, odds=3.65),
        LayBet(stake=45, odds=3.60),
    ]

    # Freebet X
    freebet = 36.75

    # Stake CS bilanciate
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

    print()
    print("=== DRAW + CORRECT SCORE SIMULATION ===")
    print()

    print(f"Freebet X:       €{freebet:.2f}")
    print(f"Stake CS 0-2:    €{stake_02:.4f}")
    print(f"Stake CS 1-2:    €{stake_12:.4f}")

    print()
    print("Scoreline        P&L")
    print("----------------------")

    for score, pnl in results.items():
        print(f"{score:<15} €{pnl:>8.2f}")


if __name__ == "__main__":
    main()
