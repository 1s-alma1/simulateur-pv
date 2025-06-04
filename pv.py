
import streamlit as st
import matplotlib.pyplot as plt

# === Arrière-plan simplifié ===
def set_background():
    st.markdown(
        '''
        <style>
        .stApp {
            background-image: url("https://cdn.pixabay.com/photo/2017/03/18/17/45/solar-panel-2157212_1280.jpg");
            background-size: cover;
            background-attachment: fixed;
        }
        </style>
        ''',
        unsafe_allow_html=True
    )

set_background()

# === Interface utilisateur ===
st.title("☀️ Simulateur Photovoltaïque Simple")

type_pv = st.selectbox("Type de panneau :", ["Monocristallin", "Polycristallin", "Amorphe"])
rendements = {"Monocristallin": 0.85, "Polycristallin": 0.80, "Amorphe": 0.65}
couts_kwc = {"Monocristallin": 4000, "Polycristallin": 3500, "Amorphe": 3000}

nb_panneaux = st.slider("Nombre de panneaux (400Wc) :", 5, 30, 20)
condition = st.selectbox("Conditions météo :", ["Ensoleillé", "Nuageux", "Pluie"])
facteurs_meteo = {"Ensoleillé": 1.0, "Nuageux": 0.65, "Pluie": 0.4}
prix_kwh = st.number_input("Tarif électricité (€/kWh)", 0.10, 0.50, 0.25)

# === Calculs ===
puissance_kwc = nb_panneaux * 0.4
irradiation = 1300  # Marseille
prod_brute = puissance_kwc * irradiation * rendements[type_pv] * facteurs_meteo[condition]
conso_maison = 8260
auto_directe = min(prod_brute, conso_maison)
economie = auto_directe * prix_kwh
invest = puissance_kwc * couts_kwc[type_pv]
roi = invest / economie if economie > 0 else float("inf")

# === Résultats ===
st.subheader("📊 Résultats")
st.write(f"Puissance installée : {puissance_kwc:.1f} kWc")
st.write(f"Production annuelle : {prod_brute:.0f} kWh")
st.write(f"Autoconsommation : {auto_directe:.0f} kWh")
st.write(f"Économie annuelle : {economie:.0f} €")
st.write(f"Investissement total : {invest:.0f} €")
st.write(f"ROI estimé : {roi:.1f} ans")

# === Graphique
labels = ["Autoconsommation", "Réseau"]
values = [auto_directe, max(0, conso_maison - auto_directe)]

fig, ax = plt.subplots()
ax.pie(values, labels=labels, autopct="%1.1f%%", colors=["#4CAF50", "#2196F3"])
ax.axis("equal")
st.pyplot(fig)
