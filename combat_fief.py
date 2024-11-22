import streamlit as st
import random

def simulate_combat(attacker_units, defender_units, attacker_bonus=0, defender_bonus=0):
    def roll_dice(unit_count, bonus):
        results = [random.randint(1, 6) + bonus for _ in range(unit_count)]
        hits = sum(1 for result in results if result >= 4)
        return hits, results

    unit_points = {"sergent": 1, "chevalier": 2, "bombarde": 3}

    attacker_dice = sum(unit_points[unit] * count for unit, count in attacker_units.items())
    defender_dice = sum(unit_points[unit] * count for unit, count in defender_units.items())

    attacker_hits, attacker_rolls = roll_dice(attacker_dice, attacker_bonus)
    defender_hits, defender_rolls = roll_dice(defender_dice, defender_bonus)

    attacker_losses = min(attacker_hits, sum(defender_units.values()))
    defender_losses = min(defender_hits, sum(attacker_units.values()))

    attacker_units_remaining = max(0, sum(attacker_units.values()) - defender_hits)
    defender_units_remaining = max(0, sum(defender_units.values()) - attacker_hits)

    results = {
        "attacker_hits": attacker_hits,
        "defender_hits": defender_hits,
        "attacker_rolls": attacker_rolls,
        "defender_rolls": defender_rolls,
        "attacker_losses": defender_losses,
        "defender_losses": attacker_losses,
        "attacker_units_remaining": attacker_units_remaining,
        "defender_units_remaining": defender_units_remaining,
        "winner": "attacker" if defender_units_remaining == 0 else "defender" if attacker_units_remaining == 0 else "undecided"
    }
    return results

st.title("Simulation de Combat - Fief France")

st.header("Configuration du Combat")
attacker_sergents = st.number_input("Sergents attaquants", min_value=0, value=5)
attacker_chevaliers = st.number_input("Chevaliers attaquants", min_value=0, value=2)
defender_sergents = st.number_input("Sergents défenseurs", min_value=0, value=3)
defender_chevaliers = st.number_input("Chevaliers défenseurs", min_value=0, value=1)
defender_bombardes = st.number_input("Bombardes défenseurs", min_value=0, value=1)

attacker_bonus = st.number_input("Bonus attaquant", min_value=0, value=0)
defender_bonus = st.number_input("Bonus défenseur", min_value=0, value=0)

if st.button("Simuler le Combat"):
    attacker = {"sergent": attacker_sergents, "chevalier": attacker_chevaliers}
    defender = {"sergent": defender_sergents, "chevalier": defender_chevaliers, "bombarde": defender_bombardes}
    results = simulate_combat(attacker, defender, attacker_bonus, defender_bonus)

    st.subheader("Résultats")
    st.write("**Touches de l'attaquant :**", results["attacker_hits"])
    st.write("**Touches du défenseur :**", results["defender_hits"])
    st.write("**Pertes attaquantes :**", results["attacker_losses"])
    st.write("**Pertes défensives :**", results["defender_losses"])
    st.write("**Unité(s) restante(s) attaquantes :**", results["attacker_units_remaining"])
    st.write("**Unité(s) restante(s) défensives :**", results["defender_units_remaining"])
    st.write("**Gagnant :**", results["winner"])
