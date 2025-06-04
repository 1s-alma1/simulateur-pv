
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# === Arrière-plan stylisé ===
def set_background():
    st.markdown(
        f'''
        <style>
        .stApp {{
            background-image: url("https://images.unsplash.com/photo-1584270354949-1a8abf5d19ae?auto=format&fit=crop&w=1470&q=80");
            background-size: cover;
            background-attachment: fixed;
            color: white;
        }}
        @keyframes blink {{
            50% {{ opacity: 0.4; }}
        }}
        .solar {{
            animation: blink 2s infinite;
            font-size: 20px;
            color: #FFD700;
        }}
        </style>
        ''',
        unsafe_allow_html=True
    )

set_background()

# === Paramètres de base ===
base_irradiation = 1300  # Marseille kWh/kWc/an
consommation_maison = 8260  # kWh/an

types_panneaux = {
    "Monocristallin": {"rendement": 0.85, "cout_kwc": 4000},
    "Polycristallin": {"rendement": 0.80, "cout_kwc": 3500},
    "Amorphe": {"rendement": 0.65, "cout_kwc": 3000},
    "Hétérojonction": {"rendement": 0.88, "cout_kwc": 5000},
    "Bifacial": {"rendement": 0.90, "cout_kwc": 5500},
}

conditions_meteo = {
    "Ensoleillé": 1.0,
    "Partiellement nuageux": 0.85,
    "Nuageux": 0.65,
    "Pluie": 0.40,
    "Brume / pollution": 0.55
}

# === Interface utilisateur ===
st.title("🔆 Simulateur Photovoltaïque + Batterie")

type_choisi = st.selectbox("Type de panneau :", list(types_panneaux.keys()))
nb_panneaux = st.slider("Nombre de panneaux :", 5, 30, 20)
tarif_kwh = st.number_input("Tarif électricité (€/kWh)", 0.10, 0.50, 0.25, 0.01)
condition = st.selectbox("Conditions météo :", list(conditions_meteo.keys()))
capacite_batterie = st.slider("Capacité batterie (kWh)", 0, 20, 10)

# === Calculs ===
puissance_kwc = nb_panneaux * 0.4
rendement = types_panneaux[type_choisi]["rendement"]
cout_kwc = types_panneaux[type_choisi]["cout_kwc"]
facteur_meteo = conditions_meteo[condition]

production = puissance_kwc * base_irradiation * rendement * facteur_meteo
autoconsommation = min(production, consommation_maison)
surplus = max(0, production - autoconsommation)

# Simulation simple de batterie
batterie_chargee = min(capacite_batterie, surplus * 0.6)  # suppose qu'on stocke 60% du surplus
batterie_utilisee = min(batterie_chargee, consommation_maison - autoconsommation)
autonomie_totale = autoconsommation + batterie_utilisee

economie = autonomie_totale * tarif_kwh
investissement = cout_kwc * puissance_kwc + capacite_batterie * 800  # coût batterie env. 800€/kWh
roi = investissement / economie if economie > 0 else float("inf")

# === Résultats ===
st.subheader("📊 Résultats de Simulation")
st.write(f"Production totale : {production:.0f} kWh/an")
st.write(f"Autoconsommation directe : {autoconsommation:.0f} kWh/an")
st.write(f"Surplus solaire : {surplus:.0f} kWh/an")
st.write(f"Stocké en batterie : {batterie_chargee:.0f} kWh/an")
st.write(f"Utilisé depuis batterie : {batterie_utilisee:.0f} kWh/an")
st.write(f"Autoconsommation totale (PV + batterie) : {autonomie_totale:.0f} kWh/an")
st.write(f"Économie annuelle : {economie:.0f} €")
st.write(f"Investissement total : {investissement:.0f} €")
st.write(f"Retour sur investissement (ROI) : {roi:.1f} ans")

# === Graphiques
labels = ["Autoconsommation directe", "Batterie", "Réseau"]
values = [
    autoconsommation,
    batterie_utilisee,
    max(0, consommation_maison - autonomie_totale)
]

fig1, ax1 = plt.subplots()
ax1.pie(values, labels=labels, autopct='%1.1f%%', startangle=90, colors=["#4CAF50", "#FFC107", "#2196F3"])
ax1.axis('equal')
st.pyplot(fig1)

# === Animation texte
st.markdown(f'<div class="solar">☀️ Production influencée par : {condition}</div>', unsafe_allow_html=True)
