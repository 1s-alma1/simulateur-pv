
import streamlit as st
import matplotlib.pyplot as plt

# === Fond dynamique selon météo ===
def set_weather_background(condition):
    if condition == "Ensoleillé":
        bg_url = "https://cdn.pixabay.com/photo/2016/03/27/07/08/sunrise-1283275_1280.jpg"
    elif condition == "Nuageux":
        bg_url = "https://cdn.pixabay.com/photo/2018/10/30/12/32/clouds-3788377_1280.jpg"
    elif condition == "Pluie":
        bg_url = "https://cdn.pixabay.com/photo/2017/08/01/08/29/rain-2568886_1280.jpg"
    else:
        bg_url = "https://cdn.pixabay.com/photo/2020/03/26/14/25/sky-4969689_1280.jpg"

    st.markdown(f'''
        <style>
        .stApp {{
            background-image: url("{bg_url}");
            background-size: cover;
            background-attachment: fixed;
            color: white;
        }}
        </style>
    ''', unsafe_allow_html=True)

# === Page config & météo
st.set_page_config(layout="centered")
condition = st.selectbox("🌦️ Conditions météo :", ["Ensoleillé", "Partiellement nuageux", "Nuageux", "Pluie"])
set_weather_background(condition)

# === Entrées utilisateur
st.title("🔆 Simulateur PV dynamique selon la météo")

type_pv = st.selectbox("🔋 Type de panneau :", [
    "Monocristallin", "Polycristallin", "Amorphe", "Hétérojonction", "Bifacial"
])
rendements = {
    "Monocristallin": 0.85, "Polycristallin": 0.80, "Amorphe": 0.65,
    "Hétérojonction": 0.88, "Bifacial": 0.92
}
couts_kwc = {
    "Monocristallin": 4000, "Polycristallin": 3500, "Amorphe": 3000,
    "Hétérojonction": 5000, "Bifacial": 5500
}
facteurs_meteo = {
    "Ensoleillé": 1.0, "Partiellement nuageux": 0.85,
    "Nuageux": 0.65, "Pluie": 0.4
}

nb_panneaux = st.slider("🔢 Nombre de panneaux (400Wc)", 5, 30, 20)
prix_kwh = st.number_input("💶 Tarif électricité (€/kWh)", 0.10, 0.50, 0.25)

# === Calculs
puissance_kwc = nb_panneaux * 0.4
irradiation = 1300
prod_brute = puissance_kwc * irradiation * rendements[type_pv] * facteurs_meteo[condition]
conso_maison = 8260
auto_directe = min(prod_brute, conso_maison)
economie = auto_directe * prix_kwh
invest = puissance_kwc * couts_kwc[type_pv]
roi = invest / economie if economie > 0 else float("inf")
indice_perf = prod_brute / invest * 1000

# === Résultats
st.subheader("📊 Résultats")
st.markdown(f"""
- ☀️ **Production estimée** : `{prod_brute:.0f} kWh/an`
- 🏠 **Autoconsommation** : `{auto_directe:.0f} kWh/an`
- 💶 **Économie annuelle** : `{economie:.0f} €`
- 💰 **Investissement** : `{invest:.0f} €`
- ⏳ **ROI estimé** : `{roi:.1f} ans`
- 📈 **Indice performance PV** : `{indice_perf:.1f} kWh / 1000 €`
""")

if roi < 8:
    st.success("Excellent rendement ☀️ : rentabilité rapide.")
elif roi < 12:
    st.info("Rentabilité correcte. Peut être optimisé.")
else:
    st.warning("ROI élevé. Essayez un autre panneau ou moins de puissance.")

# === Graphique
labels = ["Autoconsommation", "Réseau"]
values = [auto_directe, max(0, conso_maison - auto_directe)]
fig, ax = plt.subplots()
ax.pie(values, labels=labels, autopct="%1.1f%%", colors=["#4CAF50", "#2196F3"])
ax.axis("equal")
st.pyplot(fig)

