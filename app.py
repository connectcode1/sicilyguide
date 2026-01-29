import streamlit as st
import pandas as pd

# Basic Page Configuration
st.set_page_config(page_title="Sicily Secrets", page_icon="🍋", layout="wide")

# --- DATA STRETCH (The "Database") ---
trips = {
    "The Classic East": {
        "cities": ["Catania", "Taormina", "Syracuse"],
        "description": "Perfect for first-timers. Focuses on history and the volcano.",
        "must_eat": "Pasta alla Norma & Granita",
        "map_lat": 37.5, "map_lon": 15.0
    },
    "Baroque Beauty": {
        "cities": ["Noto", "Modica", "Ragusa"],
        "description": "UNESCO heritage sites, chocolate, and stunning architecture.",
        "must_eat": "Modica Chocolate & Scacce",
        "map_lat": 36.8, "map_lon": 14.7
    },
    "The Wild West": {
        "cities": ["Palermo", "San Vito Lo Capo", "Marsala"],
        "description": "Street food, crystal clear beaches, and salt pans.",
        "must_eat": "Panelle & Fish Couscous",
        "map_lat": 38.1, "map_lon": 12.8
    }
}

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("🇮🇹 Sicily Travel Guide")
st.sidebar.info("A curated guide for my international colleagues.")
selection = st.sidebar.selectbox("Choose your vibe:", list(trips.keys()))
show_tips = st.sidebar.checkbox("Show Cultural Tips")

# --- MAIN CONTENT ---
st.title(f"Trip: {selection}")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📍 Itinerary Overview")
    st.write(trips[selection]["description"])
    
    st.markdown("**Key Stops:**")
    for city in trips[selection]["cities"]:
        st.markdown(f"- {city}")
    
    st.info(f"🍴 **Local Food Tip:** Try the {trips[selection]['must_eat']}!")

with col2:
    # Map integration
    map_data = pd.DataFrame({
        'lat': [trips[selection]["map_lat"]],
        'lon': [trips[selection]["map_lon"]]
    })
    st.map(map_data, zoom=8)

# --- CULTURAL TIPS SECTION ---
if show_tips:
    st.divider()
    st.subheader("💡 Tips for Travelers")
    t1, t2, t3 = st.columns(3)
    t1.metric("Coffee Rule", "No Milk", "After 11 AM")
    t2.metric("The 'Riposo'", "1:30 PM - 4:30 PM", "Shops Closed")
    t3.metric("Payment", "Cash is King", "In small villages")

# --- FEEDBACK FORM ---
with st.expander("Need a custom recommendation?"):
    name = st.text_input("Your Name")
    days = st.slider("How many days are you staying?", 1, 14, 7)
    if st.button("Get Advice"):
        st.write(f"Ciao {name}! For {days} days, I recommend staying in {trips[selection]['cities'][0]}.")