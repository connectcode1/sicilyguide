import streamlit as st
import pandas as pd

st.set_page_config(page_title="Sicily Insider: Local Edition", page_icon="🍋", layout="wide")

# --- DATA: THE INSIDER KNOWLEDGE ---
destinations = {
    "Palermo & the West": {
        "highlights": ["Teatro Massimo", "Monreale Cathedral", "Erice"],
        "beaches": ["Mondello (Go early!)", "San Vito Lo Capo", "Riserva dello Zingaro (Hiking required)"],
        "food_spots": [
            "Nni Franco U'Vastiddaru (Street food icon)",
            "Trattoria Ai Cascinari (Traditional lunch)",
            "I Segreti del Chiostro (Best cannoli in a convent)"
        ],
        "image": "https://images.unsplash.com/photo-1541353210395-88c94676571a?w=800",
        "lat": 38.1157, "lon": 13.3615
    },
    "Catania & the East": {
        "highlights": ["Mount Etna South Crater", "Taormina Greek Theatre", "Aci Trezza"],
        "beaches": ["Isola Bella (Pebble beach)", "Fontane Bianche", "Cala Mosche"],
        "food_spots": [
            "Pasticceria Savia (Best Arancini in Catania)",
            "Osteria Antica Marina (Fresh fish near the market)",
            "Bam Bar in Taormina (The legendary Granita spot)"
        ],
        "image": "https://images.unsplash.com/photo-1508933454700-0e104e1837b7?w=800",
        "lat": 37.5027, "lon": 15.0873
    },
    "The Baroque Southeast": {
        "highlights": ["Noto Main Street", "Modica Old Town", "Ragusa Ibla"],
        "beaches": ["Spiaggia di Marianelli (Wild & quiet)", "Marzamemi", "Sampieri"],
        "food_spots": [
            "Caffè Sicilia in Noto (As seen on Chef's Table)",
            "Antica Dolceria Bonajuto (Oldest chocolate shop)",
            "Trattoria da la Rusticana (Classic Ragusa vibes)"
        ],
        "image": "https://images.unsplash.com/photo-1616432135048-52267675e01b?w=800",
        "lat": 36.8911, "lon": 14.8000
    }
}

# --- UI LAYOUT ---
st.title("🇮🇹 Sicily Insider Guide")
st.subheader("Curated for my international network 🌍")

tab1, tab2, tab3 = st.tabs(["📍 Local Itineraries", "🎒 Survival Guide", "📝 Trip Planner"])

with tab1:
    region = st.selectbox("Choose a region to explore like a local:", list(destinations.keys()))
    
    col_img, col_info = st.columns([1, 1])
    
    with col_img:
        st.image(destinations[region]["image"], use_container_width=True)
        st.map(pd.DataFrame({'lat': [destinations[region]["lat"]], 'lon': [destinations[region]["lon"]]}), zoom=8)

    with col_info:
        st.markdown(f"### 🏖️ Top Beaches")
        for beach in destinations[region]["beaches"]:
            st.markdown(f"- {beach}")
            
        st.markdown(f"### 🍝 Where to Eat")
        for spot in destinations[region]["food_spots"]:
            st.success(f"**{spot}**")
            
        st.markdown("### 🏛️ Must-See")
        st.write(", ".join(destinations[region]["highlights"]))

with tab2:
    st.header("The 'Unwritten Rules' of Sicily")
    c1, c2 = st.columns(2)
    
    with c1:
        st.info("### ☕ The Coffee Timeline")
        st.write("- **Morning:** Cappuccino & Cornetto.\n- **After 11am:** Caffè (Espresso) only.\n- **Pro Tip:** Drink it standing at the bar like a local.")
        
        st.warning("### 🚗 Driving & Parking")
        st.write("Blue lines = Paid parking. White lines = Free. Yellow = Residents only. Don't park on yellow!")

    with c2:
        st.success("### 🕒 The Riposo")
        st.write("Shops usually close 13:30 – 16:30. Restaurants serve lunch until 14:30 and reopen for dinner at 20:00.")

with tab3:
    st.header("Build Your Custom List")
    user_name = st.text_input("What's your name?")
    interest = st.multiselect("What are you looking for?", ["History", "Beaches", "Food", "Hiking", "Nightlife"])
    
    if st.button("Generate Advice"):
        st.write(f"Ciao {user_name}! Since you like {', '.join(interest)}, I suggest starting your journey in {region.split(' ')[0]}.")

st.divider()
st.caption("Updated with the best local insights for my international network.")
