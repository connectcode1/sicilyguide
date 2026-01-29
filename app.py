import streamlit as st
import pandas as pd

# Page Config
st.set_page_config(page_title="Sicily: The Complete Insider", page_icon="🍋", layout="wide")

# Custom CSS for the "Noto Stone" & Majolica Aesthetic
st.markdown("""
    <style>
    /* Background set to Noto Stone / Cream */
    .stApp {
        background-color: #FDF5E6;
    }
    .main {
        background-color: #FDF5E6;
    }
    /* Sicilian Header with Gradient */
    .stHeader {
        background: linear-gradient(135deg, #005DAA 0%, #D32F2F 50%, #FFD700 100%);
        padding: 40px;
        border-radius: 15px;
        color: white;
        text-align: center;
        border-bottom: 10px solid #D32F2F;
        margin-bottom: 25px;
    }
    .tile-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 8px;
        border-top: 5px solid #005DAA;
        border-bottom: 5px solid #FFD700;
        box-shadow: 4px 4px 15px rgba(0,0,0,0.05);
    }
    .human-touch {
        font-style: italic;
        color: #D32F2F;
        font-weight: 500;
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- THE EXPANDED DATABASE ---
destinations = {
    "Palermo & The West": {
        "description": "A glorious chaos of Arab-Norman history and the best street food in Europe.",
        "human_tip": "If you go to the Ballarò market, don't just look—eat. Accept the small samples from vendors; it's how we welcome you.",
        "beaches": ["Mondello (Go early!)", "Riserva dello Zingaro (Hidden coves)", "San Vito Lo Capo"],
        "food_spots": "Nni Franco U'Vastiddaru (Street food), I Segreti del Chiostro (Cannoli)",
        "lat": 38.1157, "lon": 13.3615
    },
    "Catania & Mt. Etna": {
        "description": "Built from the very lava that once threatened it, Catania is gritty, baroque, and resilient.",
        "human_tip": "When visiting Etna, respect 'A Muntagna'. She isn't just a volcano to us; she is a living presence.",
        "beaches": ["San Giovanni Li Cuti (Black volcanic sand)", "Aci Trezza (The Cyclops Riviera)"],
        "food_spots": "Savia (Arancini), Osteria Antica Marina (Fish market dining)",
        "lat": 37.5027, "lon": 15.0873
    },
    "Siracusa & Ortigia": {
        "description": "White limestone buildings floating on the sea. The light here is different than anywhere else.",
        "human_tip": "Sit in Piazza Duomo at sunset. The stone turns a warm honey color. It’s the perfect time for a 'Caffè Shakerato'.",
        "beaches": ["Fontane Bianche", "Cala Mosche (Inside Vendicari)"],
        "food_spots": "Caseificio Borderi (Legendary sandwiches), Cortile di Bacco",
        "lat": 37.0755, "lon": 15.2866
    },
    "Agrigento & The South": {
        "description": "Home to the Valley of the Temples, where Ancient Greece still feels alive.",
        "human_tip": "Go to the temples at night. Seeing the Concordia Temple illuminated under the stars is a spiritual experience.",
        "beaches": ["Scala dei Turchi (White cliffs)", "Siculiana Marina"],
        "food_spots": "Terracotta (Local ingredients), La Terrazza degli Dei",
        "lat": 37.3107, "lon": 13.5765
    }
}

itineraries = {
    "3-Day Express": "Focus on either Palermo OR Catania. Don't try to do both, or you'll spend your whole trip in a car.",
    "7-Day Loop": "Palermo → Cefalù → Taormina → Catania/Etna. A classic 'Grand Tour' of the north and east.",
    "10-Day Deep Dive": "The full island. Start in Palermo, head west to Trapani, south to Agrigento, then east to Noto and Siracusa."
}

# --- UI DISPLAY ---
st.markdown('<div class="stHeader"><h1>Sicily Insider Guide</h1><p>Curated for my International Network</p></div>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["🗺️ Interactive Map", "📜 Suggested Itineraries", "🍋 Regional Secrets", "🏺 Cultural Rituals"])

with tab1:
    st.subheader("Explore the Island")
    # Mapping logic
    map_df = pd.DataFrame([{"lat": d["lat"], "lon": d["lon"], "name": k} for k, d in destinations.items()])
    st.map(map_df, zoom=7)
    st.caption("Click and scroll to see where the magic happens.")

with tab2:
    st.subheader("How long are you staying?")
    for duration, plan in itineraries.items():
        with st.expander(f"📅 {duration}"):
            st.write(plan)
            st.info("Pro Tip: Rent a small car. Our 'highways' are fine, but city streets are narrow!")

with tab3:
    region = st.selectbox("Choose a region:", list(destinations.keys()))
    res = destinations[region]
    
    col1, col2 = st.columns([1.5, 1])
    with col1:
        st.markdown(f"### {region}")
        st.write(res["description"])
        st.markdown(f'<p class="human-touch">"{res["human_tip"]}"</p>', unsafe_allow_html=True)
        
        st.markdown("#### 🍝 Local Food Spots")
        st.success(res["food_spots"])
        
    with col2:
        st.markdown("#### 🏖️ Top Beaches")
        for beach in res["beaches"]:
            st.write(f"🔹 {beach}")

with tab4:
    st.subheader("Living the Sicilian Life")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        **The Coffee Rules:**
        - No Cappuccino after 11:00 AM.
        - Drink your espresso standing up for the 'local price'.
        - 'Caffè Freddo' is your best friend in July.
        """)
    with c2:
        st.markdown("""
        **The Riposo:**
        - From 13:30 to 16:30, the island sleeps.
        - Don't expect to find shops open in small towns.
        - It's the perfect time for a long lunch or a nap.
        """)

st.divider()
st.caption("Designed with the colors of Noto and the spirit of the Mediterranean.")
