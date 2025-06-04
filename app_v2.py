
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# === Arrière-plan animé adapté au solaire ===
def set_background():
    st.markdown(
        f'''
        <style>
        .stApp {{
            background-image: url("https://images.unsplash.com/photo-1584270354949-1a8abf5d19ae?auto=format&fit=crop&w=1470&q=80");
            background-size: cover;
            background-attachment: fixed;
        }}

        @keyframes fadeIn {{
            0% {{ opacity: 0; }}
            100% {{ opacity: 1; }}
        }}

        .stApp * {{
            animation: fadeIn 1.5s ease-in;
        }}
        </style>
        ''',
        unsafe_allow_html=True
    )

set_background()

# === Données de base ===
base_irradiation = 1300  # moyenne Marseille
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
st.title("🔆 Simulateur Photovoltaïque Avancé")

type_choisi = st.selectbox("Type de panneau :", list(types_panneaux.keys()))
nb_panneaux = st.slider("Nombre de panneaux :", 5, 30, 20)
tarif_kwh = st.number_input("Tarif électricité (€/kWh)", 0.10, 0.50, 0.25, 0.01)
condition = st.selectbox("Conditions météo simulées :", list(conditions_meteo.keys()))

# === Calculs ===
puissance_kwc = nb_panneaux * 0.4
rendement = types_panneaux[type_choisi]["rendement"]
cout_kwc = types_panneaux[type_choisi]["cout_kwc"]
facteur_meteo = conditions_meteo[condition]

production = puissance_kwc * base_irradiation * rendement * facteur_meteo
autoconsommation = min(production, consommation_maison)
economie = autoconsommation * tarif_kwh
investissement = cout_kwc * puissance_kwc
roi = investissement / economie if economie > 0 else float("inf")

# === Résultats ===
st.subheader("📊 Résultats de Simulation")
st.write(f"Puissance installée : {puissance_kwc:.1f} kWc")
st.write(f"Production simulée (avec météo '{condition}') : {production:.0f} kWh/an")
st.write(f"Autoconsommation estimée : {autoconsommation:.0f} kWh/an")
st.write(f"Économie annuelle : {economie:.0f} €")
st.write(f"Investissement total : {investissement:.0f} €")
st.write(f"Retour sur investissement (ROI) : {roi:.1f} ans")

# === Graphique
fig, ax = plt.subplots()
ax.bar(["Production", "Consommation"], [production, consommation_maison], color=["#4CAF50", "#2196F3"])
ax.set_ylabel("kWh/an")
ax.set_title("Production vs. Consommation")
st.pyplot(fig)
