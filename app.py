import streamlit as st
import pandas as pd
from datetime import datetime
import json

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Sicily Insider - Curated Travel Guide",
    page_icon="🇮🇹",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# SICILIAN EDITORIAL CSS (refined)
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Lato:wght@300;400;700&display=swap');

.stApp {
    background-color: #FAF9F6;
    color: #2C2C2C;
    font-family: 'Lato', sans-serif;
}

.content-card {
    background: #FFFFFF;
    padding: 50px;
    margin: 40px 0;
    border-top: 6px solid #C85A54;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
}

.feature-card {
    background: #FFFFFF;
    border: 1px solid #E8E4DC;
    border-left: 4px solid #D4A574;
    padding: 30px;
    margin: 20px 0;
}

h1, h2, h3 {
    font-family: 'Playfair Display', serif !important;
}

h2 {
    color: #B34A44 !important;
}

.hero-section {
    text-align: center;
    padding: 80px 20px;
    background: linear-gradient(180deg, #FFFFFF 0%, #F8F6F2 100%);
}

.section-header {
    text-align: center;
    margin: 60px 0 40px 0;
}

.stButton>button {
    background: #C85A54;
    color: white;
    border-radius: 0;
    padding: 14px 36px;
    font-weight: 600;
    letter-spacing: 1.5px;
}

.number-badge {
    display: inline-block;
    background: #C85A54;
    color: white;
    width: 32px;
    height: 32px;
    line-height: 32px;
    text-align: center;
    border-radius: 50%;
    margin-right: 12px;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# SESSION STATE
# =========================================================
if "bookmarks" not in st.session_state:
    st.session_state.bookmarks = []

# =========================================================
# DESTINATIONS DATA (UNCHANGED)
# =========================================================
destinations = {
    "Palermo & Western Sicily": {
        "tagline": "Where Arab Domes Meet Norman Grandeur",
        "beaches": {"Mondello": "Art Nouveau beach"},
        "experiences": {"Street Food Tour": "Markets"},
        "must_visit": ["Palatine Chapel"],
        "where_to_eat": {"Cappello": "Cannoli"},
        "lat": 38.1157,
        "lon": 13.3615,
        "days": "4-5 days",
        "best_time": "April–June"
    },
    "Catania, Etna & Eastern Sicily": {
        "tagline": "Living in the Shadow of the Volcano",
        "beaches": {"Aci Trezza": "Cyclops rocks"},
        "experiences": {"Etna Hike": "Volcano"},
        "must_visit": ["Piazza Duomo"],
        "where_to_eat": {"Savia": "Arancini"},
        "lat": 37.5079,
        "lon": 15.0830,
        "days": "3-4 days",
        "best_time": "April–June"
    },
    "Syracuse & Baroque Southeast": {
        "tagline": "Where Greece Meets Baroque",
        "beaches": {"Vendicari": "Nature reserve"},
        "experiences": {"Greek Theater": "Classical drama"},
        "must_visit": ["Ortigia"],
        "where_to_eat": {"Caffè Sicilia": "Granita"},
        "lat": 37.0755,
        "lon": 15.2866,
        "days": "4-5 days",
        "best_time": "May–June"
    }
}

# =========================================================
# ITINERARY GENERATOR
# =========================================================
def generate_itinerary(duration, travel_style, interests):
    score = {}

    for region, data in destinations.items():
        score[region] = 0

        if travel_style == "Beach & Relaxation":
            score[region] += len(data["beaches"]) * 2
        if travel_style == "Culture & History":
            score[region] += len(data["must_visit"]) * 2
        if travel_style == "Food & Wine":
            score[region] += len(data["where_to_eat"]) * 2
        if travel_style == "Balanced Mix":
            score[region] += 4

        for interest in interests:
            if interest.lower() in json.dumps(data).lower():
                score[region] += 2

    ranked = sorted(score, key=score.get, reverse=True)

    days_left = duration
    plan = []

    for region in ranked:
        if days_left <= 0:
            break
        stay = min(3, days_left)
        plan.append((region, stay))
        days_left -= stay

    return plan

# =========================================================
# HERO
# =========================================================
st.markdown("""
<div class="hero-section">
    <h1>Sicily</h1>
    <p style="font-size:1.3em;color:#5B8C85;">
        An insider’s journey through the island of contradictions
    </p>
</div>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:
    st.markdown("### Sicily Insider")
    st.markdown("Curated, local, intelligent travel")

# =========================================================
# TABS (NO DASHBOARD)
# =========================================================
tab1, tab2, tab3 = st.tabs([
    "EXPLORE REGIONS",
    "PLAN YOUR TRIP",
    "INSIDER TIPS"
])

# =========================================================
# TAB 1 — EXPLORE
# =========================================================
with tab1:
    st.markdown("<div class='section-header'><h2>Explore Regions</h2></div>", unsafe_allow_html=True)
    selected = st.selectbox("Select a region", list(destinations.keys()), index=0)
    region = destinations[selected]

    st.markdown(f"""
    <div class="content-card">
        <h3>{selected}</h3>
        <p><em>{region['tagline']}</em></p>
        <p><strong>Best time:</strong> {region['best_time']}</p>
        <p><strong>Stay:</strong> {region['days']}</p>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# TAB 2 — PLAN YOUR TRIP (AUTO)
# =========================================================
with tab2:
    st.markdown("<div class='section-header'><h2>Your Personalized Itinerary</h2></div>", unsafe_allow_html=True)

    with st.form("planner"):
        duration = st.number_input("Trip length (days)", 3, 21, 7)
        travel_style = st.selectbox("Travel style", [
            "Balanced Mix",
            "Beach & Relaxation",
            "Culture & History",
            "Food & Wine"
        ])

        interests = []
        if st.checkbox("Beaches"): interests.append("beach")
        if st.checkbox("Food"): interests.append("food")
        if st.checkbox("Culture"): interests.append("culture")

        submit = st.form_submit_button("Generate My Trip")

    if submit:
        itinerary = generate_itinerary(duration, travel_style, interests)

        for i, (region, days) in enumerate(itinerary, start=1):
            st.markdown(f"""
            <div class="feature-card">
                <span class="number-badge">{i}</span>
                <strong>{region}</strong><br>
                {days} days • {destinations[region]['tagline']}
            </div>
            """, unsafe_allow_html=True)

# =========================================================
# TAB 3 — INSIDER TIPS
# =========================================================
with tab3:
    st.markdown("<div class='section-header'><h2>Insider Tips</h2></div>", unsafe_allow_html=True)
    st.markdown("""
    - Rent a car for countryside travel  
    - Eat where locals eat (no menus in English)  
    - Visit baroque towns at golden hour  
    """)

# =========================================================
# MAP
# =========================================================
st.markdown("<div class='section-header'><h2>Sicily at a Glance</h2></div>", unsafe_allow_html=True)
st.map(pd.DataFrame([
    {"lat": d["lat"], "lon": d["lon"]} for d in destinations.values()
]))

# =========================================================
# FOOTER
# =========================================================
st.markdown("""
<hr>
<p style="text-align:center;font-size:0.9em;color:#6A6A6A;">
© 2026 Sicily Insider • Curated with local knowledge
</p>
""", unsafe_allow_html=True)
