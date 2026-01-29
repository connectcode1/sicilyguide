import streamlit as st
import pandas as pd
import json
from datetime import datetime

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Sicily Insider – Curated Travel Guide",
    page_icon="🇮🇹",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# STYLES (UNCHANGED, ONLY MICRO-WARMTH ADDED)
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Lato:wght@300;400;700&display=swap');

.stApp {
    background-color: #FAF9F6;
    color: #2C2C2C;
    font-family: 'Lato', sans-serif;
}

h1, h2, h3 {
    font-family: 'Playfair Display', serif !important;
}

.hero-section {
    text-align: center;
    padding: 80px 20px;
}

.section-header {
    text-align: center;
    margin: 60px 0 40px 0;
}

.content-card {
    background: white;
    padding: 50px;
    margin: 40px 0;
    border-top: 6px solid #D4A574;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
}

.feature-card {
    background: white;
    border: 1px solid #E8E4DC;
    padding: 30px;
    margin: 20px 0;
}

.number-badge {
    display: inline-block;
    background: #B34A44;
    color: white;
    width: 32px;
    height: 32px;
    line-height: 32px;
    text-align: center;
    border-radius: 50%;
    margin-right: 10px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# SESSION STATE (UNCHANGED)
# =========================================================
if "bookmarks" not in st.session_state:
    st.session_state.bookmarks = []

# =========================================================
# DESTINATIONS DATA (UNCHANGED STRUCTURE)
# =========================================================
destinations = {
    "Palermo & Western Sicily": {
        "tagline": "Where Arab domes meet Norman grandeur",
        "beaches": {"Mondello": "Art Nouveau beach"},
        "experiences": {"Street Food Tour": "Ballarò & Vucciria"},
        "must_visit": ["Palatine Chapel", "Monreale Cathedral"],
        "where_to_eat": {"Antica Focacceria": "Panelle"},
        "lat": 38.1157,
        "lon": 13.3615,
        "days": "4–5 days",
        "best_time": "April–June"
    },
    "Catania, Etna & Eastern Sicily": {
        "tagline": "Living in the shadow of the volcano",
        "beaches": {"Aci Trezza": "Cyclops coast"},
        "experiences": {"Etna Hike": "Volcanic landscapes"},
        "must_visit": ["Piazza Duomo"],
        "where_to_eat": {"Savia": "Arancini"},
        "lat": 37.5079,
        "lon": 15.0830,
        "days": "3–4 days",
        "best_time": "April–June"
    },
    "Syracuse & Baroque Southeast": {
        "tagline": "Where Greece meets Baroque",
        "beaches": {"Vendicari": "Nature reserve"},
        "experiences": {"Greek Theatre": "Classical drama"},
        "must_visit": ["Ortigia Island"],
        "where_to_eat": {"Caffè Sicilia": "Granita"},
        "lat": 37.0755,
        "lon": 15.2866,
        "days": "4–5 days",
        "best_time": "May–June"
    }
}

# =========================================================
# ITINERARY GENERATOR (NEW – SURGICAL ADDITION)
# =========================================================
def generate_itinerary(duration, start_city, travel_style, interests):
    scores = {}

    for region, data in destinations.items():
        score = 0

        if travel_style == "Beach & Relaxation":
            score += len(data["beaches"]) * 2
        elif travel_style == "Culture & History":
            score += len(data["must_visit"]) * 2
        elif travel_style == "Food & Wine":
            score += len(data["where_to_eat"]) * 2
        elif travel_style == "Active Adventure":
            score += len(data["experiences"]) * 2
        else:
            score += 4  # Balanced mix

        for interest in interests:
            if interest.lower() in json.dumps(data).lower():
                score += 3

        scores[region] = score

    ranked = sorted(scores, key=scores.get, reverse=True)

    days_left = duration
    itinerary = []

    for region in ranked:
        if days_left <= 0:
            break
        stay = min(3, days_left)
        itinerary.append((region, stay))
        days_left -= stay

    return itinerary

# =========================================================
# HERO
# =========================================================
st.markdown("""
<div class="hero-section">
    <h1>Sicily Insider</h1>
    <p style="font-size:1.3em;">
        A curated guide to the island of contrasts
    </p>
</div>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR (DASHBOARD REMOVED)
# =========================================================
with st.sidebar:
    st.markdown("### Sicily Insider")
    st.markdown("Local knowledge. Thoughtful travel.")

# =========================================================
# TABS (NO DASHBOARD)
# =========================================================
tab1, tab2, tab3, tab4 = st.tabs([
    "EXPLORE REGIONS",
    "PLAN YOUR TRIP",
    "INSIDER TIPS",
    "COMMUNITY"
])

# =========================================================
# TAB 1 — EXPLORE REGIONS (UNCHANGED)
# =========================================================
with tab1:
    st.markdown("<div class='section-header'><h2>Explore Regions</h2></div>", unsafe_allow_html=True)

    selected_region = st.selectbox(
        "Select a region",
        list(destinations.keys()),
        index=0
    )

    region = destinations[selected_region]

    st.markdown(f"""
    <div class="content-card">
        <h3>{selected_region}</h3>
        <p><em>{region['tagline']}</em></p>
        <p><strong>Best time:</strong> {region['best_time']}</p>
        <p><strong>Recommended stay:</strong> {region['days']}</p>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# TAB 2 — PLAN YOUR TRIP (SURGICAL UPGRADE)
# =========================================================
with tab2:
    st.markdown("<div class='section-header'><h2>Plan Your Trip</h2></div>", unsafe_allow_html=True)

    with st.form("trip_planner"):
        start_city = st.selectbox("Arrival city", ["Palermo", "Catania"])
        duration = st.number_input("Trip length (days)", 3, 21, 7)
        travel_style = st.selectbox(
            "Travel style",
            ["Balanced Mix", "Beach & Relaxation", "Culture & History", "Food & Wine", "Active Adventure"]
        )

        interests = []
        if st.checkbox("Beaches"):
            interests.append("beach")
        if st.checkbox("Food"):
            interests.append("food")
        if st.checkbox("Culture"):
            interests.append("culture")
        if st.checkbox("Nature"):
            interests.append("nature")

        submit = st.form_submit_button("Generate Itinerary")

    if submit:
        itinerary = generate_itinerary(duration, start_city, travel_style, interests)

        st.markdown("---")
        st.markdown("### Your Personalized Sicily
