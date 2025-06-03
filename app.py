
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# === Données de base ===
irradiation = 1300  # Marseille, en kWh/kWc/an
consommation_maison = 8260  # kWh/an

# === Types de panneaux ===
types_panneaux = {
    "Monocristallin": {"rendement": 0.85, "cout_kwc": 4000},
    "Polycristallin": {"rendement": 0.80, "cout_kwc": 3500},
    "Amorphe": {"rendement": 0.65, "cout_kwc": 3000},
    "Hétérojonction": {"rendement": 0.88, "cout_kwc": 5000},
    "Bifacial": {"rendement": 0.90, "cout_kwc": 5500},
}

# === Interface utilisateur ===
st.title("🔆 Simulateur Photovoltaïque Intelligent")

type_choisi = st.selectbox("Type de panneau :", list(types_panneaux.keys()))
nb_panneaux = st.slider("Nombre de panneaux installés :", 5, 30, 20)
tarif_kwh = st.number_input("Tarif électricité (€/kWh)", 0.10, 0.50, 0.25, 0.01)

# === Calculs ===
puissance_kwc = nb_panneaux * 0.4
rendement = types_panneaux[type_choisi]["rendement"]
cout_kwc = types_panneaux[type_choisi]["cout_kwc"]
production = puissance_kwc * irradiation * rendement
autoconsommation = min(production, consommation_maison)
economie = autoconsommation * tarif_kwh
investissement = cout_kwc * puissance_kwc
roi = investissement / economie if economie > 0 else float("inf")

# === Affichage des résultats ===
st.subheader("📈 Résultats")
st.write(f"**Puissance installée :** {puissance_kwc:.1f} kWc")
st.write(f"**Production annuelle estimée :** {production:.0f} kWh")
st.write(f"**Autoconsommation estimée :** {autoconsommation:.0f} kWh")
st.write(f"**Économie annuelle :** {economie:.0f} €")
st.write(f"**Investissement total :** {investissement:.0f} €")
st.write(f"**Retour sur investissement (ROI) :** {roi:.1f} années")

# === Graphique barres : production vs consommation
fig, ax = plt.subplots()
ax.bar(["Production", "Consommation maison"], [production, consommation_maison], color=["#4CAF50", "#2196F3"])
ax.set_ylabel("kWh/an")
ax.set_title("Production vs. Consommation")
st.pyplot(fig)
