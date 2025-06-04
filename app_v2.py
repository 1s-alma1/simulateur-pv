
import streamlit as st
import matplotlib.pyplot as plt

# === Fond personnalisé + soleil animé ===
def set_background():
    st.markdown(
        '''
        <style>
        .stApp {
            background-image: url("https://cdn.pixabay.com/photo/2017/08/06/00/07/solar-panels-2585405_1280.jpg");
            background-size: cover;
            background-attachment: fixed;
            color: white;
        }

        .sun {
            font-size: 40px;
            animation: pulse 2s infinite;
            text-align: center;
            padding: 10px;
        }

        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.4; }
            100% { opacity: 1; }
        }
        </style>
        ''',
        unsafe_allow_html=True
    )

set_background()

st.markdown('<div class="sun">☀️</div>', unsafe_allow_html=True)

# === Interface utilisateur ===
st.title("🔆 Simulateur Photovoltaïque Créatif")

type_pv = st.selectbox("Type de panneau :", [
    "Monocristallin", "Polycristallin", "Amorphe", "Hétérojonction", "Bifacial"
])
rendements = {
    "Monocristallin": 0.85,
    "Polycristallin": 0.80,
    "Amorphe": 0.65,
    "Hétérojonction": 0.88,
    "Bifacial": 0.92
}
couts_kwc = {
    "Monocristallin": 4000,
    "Polycristallin": 3500,
    "Amorphe": 3000,
    "Hétérojonction": 5000,
    "Bifacial": 5500
}

nb_panneaux = st.slider("Nombre de panneaux (400Wc)", 5, 30, 20)
condition = st.selectbox("Conditions météo :", ["Ensoleillé", "Partiellement nuageux", "Nuageux", "Pluie"])
facteurs_meteo = {
    "Ensoleillé": 1.0,
    "Partiellement nuageux": 0.85,
    "Nuageux": 0.65,
    "Pluie": 0.4
}
prix_kwh = st.number_input("Tarif électricité (€/kWh)", 0.10, 0.50, 0.25)

# === Calculs ===
puissance_kwc = nb_panneaux * 0.4
irradiation = 1300
prod_brute = puissance_kwc * irradiation * rendements[type_pv] * facteurs_meteo[condition]
conso_maison = 8260
auto_directe = min(prod_brute, conso_maison)
economie = auto_directe * prix_kwh
invest = puissance_kwc * couts_kwc[type_pv]
roi = invest / economie if economie > 0 else float("inf")
indice_perf = prod_brute / invest * 1000  # production par euro investi (kWh/1000€)

# === Résultats ===
st.subheader("📊 Résultats")
st.write(f"Puissance installée : **{puissance_kwc:.1f} kWc**")
st.write(f"Production estimée : **{prod_brute:.0f} kWh/an**")
st.write(f"Autoconsommation : **{auto_directe:.0f} kWh/an**")
st.write(f"Économie annuelle : **{economie:.0f} €**")
st.write(f"Investissement total : **{invest:.0f} €**")
st.write(f"Retour sur investissement (ROI) : **{roi:.1f} ans**")
st.write(f"🔎 Indice de performance PV : **{indice_perf:.1f} kWh / 1000 € investi**")

# === Recommandation intelligente
if roi < 8:
    st.success("✅ Excellent choix : retour rapide sur investissement !")
elif roi <= 12:
    st.warning("ℹ️ Choix correct mais peut être optimisé.")
else:
    st.error("❌ ROI trop long, essayez un autre type ou moins de panneaux.")

# === Graphique
labels = ["Autoconsommation", "Réseau"]
values = [auto_directe, max(0, conso_maison - auto_directe)]
fig, ax = plt.subplots()
ax.pie(values, labels=labels, autopct="%1.1f%%", colors=["#4CAF50", "#2196F3"])
ax.axis("equal")
st.pyplot(fig)
