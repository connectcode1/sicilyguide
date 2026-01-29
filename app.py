import streamlit as st
import pandas as pd
from datetime import datetime

# Page Config
st.set_page_config(
    page_title="Sicily Insider - Curated Travel Guide", 
    page_icon="🇮🇹", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS REMAINS THE SAME AS YOUR BEAUTIFUL ORIGINAL DESIGN ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Lato:wght@300;400;700&display=swap');
    .stApp { background-color: #FFFFFF; color: #2C2C2C; font-family: 'Lato', sans-serif; }
    .content-card { background: #FFFFFF; padding: 50px; border-top: 6px solid #D4A574; margin: 40px 0; box-shadow: 0 4px 20px rgba(0,0,0,0.08); }
    .feature-card { background: #F8F6F2; border-left: 4px solid #5B8C85; padding: 30px; margin: 20px 0; }
    h1 { font-family: 'Playfair Display', serif !important; font-size: 3.5em !important; }
    h2 { font-family: 'Playfair Display', serif !important; color: #C85A54 !important; }
    .insider-quote { border-left: 4px solid #D4A574; padding: 25px; background: #F8F6F2; font-style: italic; }
    .hero-section { text-align: center; padding: 80px 20px; background: linear-gradient(180deg, #FFFFFF 0%, #F8F6F2 100%); }
    </style>
    """, unsafe_allow_html=True)

# --- EXPANDED DESTINATIONS DATA ---
destinations = {
    "Palermo & Western Sicily": {
        "tagline": "Where Arab Domes Meet Norman Grandeur",
        "description": """Palermo is a city of contradictions and unexpected beauty. Byzantine mosaics shimmer in Norman chapels, 
        Arab-influenced markets pulse with life, and baroque palaces lean against crumbling facades. The western coast unfolds with 
        pristine reserves, ancient salt pans, and hilltop medieval towns suspended in time. 
        
        To walk through the streets of Palermo is to walk through layers of history. You will find the influence of the Phoenicians, 
        the Romans, the Arabs, and the Normans all within a single city block. The architecture is a fever dream of styles—Arabic 
        geometric patterns sitting comfortably alongside Baroque flourishes. The air carries the scent of fried panelle and sea 
        salt, and the energy is infectious. It is a city that demands you pay attention, offering hidden courtyards and world-class 
        street food to those brave enough to wander off the main Corso.""",
        "interests": ["Ancient ruins", "Baroque", "Food", "Photography"],
        "beaches": {
            "Mondello Beach": "Palermo's Art Nouveau playground with turquoise waters and Belle Époque architecture",
            "Riserva dello Zingaro": "7km of protected coastline accessible only on foot, with hidden coves and crystalline water"
        },
        "must_visit": ["Palatine Chapel", "Monreale Cathedral", "Ballarò Market"],
        "lat": 38.1157, "lon": 13.3615, "days": "4-5 days"
    },
    "Aeolian Islands": {
        "tagline": "The Seven Sisters of the Tyrrhenian Sea",
        "description": """Seven volcanic islands scattered north of Sicily like precious stones. Lipari, the largest, is a base for 
        island hopping. Stromboli erupts every 20 minutes—you can hike to the crater at sunset. Vulcano's therapeutic mud baths steam 
        beside black sand beaches. Salina grows sweet Malvasia wine among capers and wildflowers. 
        
        The archipelago is a UNESCO World Heritage site for a reason. These islands were forged in fire and sculpted by the wind. 
        On Salina, you'll find a lush, green paradise where the pace of life slows to a crawl and the local Malvasia wine tastes 
        like liquid sunshine. On Panarea, the white-washed houses and bougainvillea create a Mediterranean chic atmosphere that 
        rivals the Greek Isles. Each island is a distinct world, connected only by the deep blue sea and the ferries that zip 
        between them.""",
        "interests": ["Islands", "Beaches", "Wine", "Active Adventure"],
        "beaches": {
            "Pollara Beach (Salina)": "Crescent bay beneath volcanic cliffs, Il Postino filming location",
            "Spiaggia Bianca (Lipari)": "White pumice beach contrasting with turquoise water"
        },
        "must_visit": ["Stromboli Crater", "Salina Vineyards", "Lipari Old Town"],
        "lat": 38.5667, "lon": 14.9564, "days": "5-7 days"
    },
    "Syracuse & Baroque Southeast": {
        "tagline": "Where Greece Meets Baroque Splendor",
        "description": """Syracuse was the most powerful Greek city in the Mediterranean, rivaling Athens. Today, Ortigia island 
        preserves layers of history—Greek temples beneath baroque churches. Beyond the city, the Val di Noto showcases UNESCO 
        baroque towns rebuilt after the 1693 earthquake.
        
        The light in the Southeast is different—it turns the local limestone a warm, honey hue that glows at sunset. The 'Baroque 
        Triangle' of Noto, Ragusa, and Modica offers some of the most stunning urban planning in the world. Imagine wide piazzas 
        designed for theater, grand staircases leading to towering cathedrals, and balconies supported by carved stone monsters. 
        This is a region of elegance and intellectual history, where the ancient world and the 17th century exist in a 
        harmonious, sun-drenched embrace.""",
        "interests": ["Baroque", "Ancient ruins", "Food", "Photography"],
        "beaches": {
            "Fontane Bianche": "Powdery white sand and shallow turquoise water",
            "Vendicari": "Nature reserve with pristine beaches and flamingo spotting"
        },
        "must_visit": ["Ortigia Island", "Greek Theater of Syracuse", "Noto Cathedral"],
        "lat": 37.0755, "lon": 15.2866, "days": "4-5 days"
    }
}

# --- HEADER ---
st.markdown("""
    <div class="hero-section">
        <p style="font-size: 0.9em; text-transform: uppercase; letter-spacing: 3px; color: #C85A54; font-weight: 600;">Curated Travel Guide</p>
        <h1>Sicily</h1>
    </div>
    """, unsafe_allow_html=True)

# --- SIDEBAR (Cleaned) ---
with st.sidebar:
    st.markdown("#### THE INSIDER")
    st.info("Explore the island through local eyes. Select a tab to begin your journey.")
    st.markdown("---")
    st.markdown("#### QUICK TIPS")
    st.write("• Rent a car for the coast.")
    st.write("• April-June is peak beauty.")

# --- MAIN TABS ---
tab1, tab2, tab3 = st.tabs(["EXPLORE REGIONS", "PLAN YOUR TRIP", "INSIDER TIPS"])

with tab1:
    selected_region = st.selectbox("Select a region", list(destinations.keys()))
    region = destinations[selected_region]
    
    st.markdown(f"""
        <div class="content-card">
            <h2>{selected_region}</h2>
            <p style="font-size: 1.2em; line-height: 1.8;">{region['description']}</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Signature Sites")
        for item in region['must_visit']:
            st.markdown(f"- **{item}**")
    with col2:
        st.markdown("### The Coast")
        for b, d in region['beaches'].items():
            st.markdown(f"**{b}**: {d}")

with tab2:
    st.markdown("## Instant Itinerary Generator")
    st.write("Select your interests and we will build your route immediately.")
    
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            days = st.slider("Duration (Days)", 3, 14, 7)
        with col2:
            style = st.multiselect("Your Interests", ["Ancient ruins", "Baroque", "Food", "Islands", "Beaches", "Wine", "Active Adventure"])
            
    if style:
        st.markdown("---")
        st.markdown(f"### Your Custom {days}-Day Route")
        
        # Suggestion Logic
        suggested_regions = []
        for name, data in destinations.items():
            if any(interest in data['interests'] for interest in style):
                suggested_regions.append(name)
        
        if suggested_regions:
            for i, r_name in enumerate(suggested_regions):
                st.markdown(f"""
                    <div class="feature-card">
                        <h4 style="color:#C85A54;">Stop {i+1}: {r_name}</h4>
                        <p>{destinations[r_name]['tagline']}</p>
                        <p><strong>Top Experience:</strong> {destinations[r_name]['must_visit'][0]}</p>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("Try selecting a few more interests to see matching regions!")
    else:
        st.info("Please select at least one interest to generate suggestions.")

with tab3:
    st.markdown("### Travel Wisdom")
    st.markdown("""
    <div class="insider-quote">
        "Sicily is more than an island; it is a continent of the mind. Don't try to see it all. Pick a corner and let it speak to you."
    </div>
    """, unsafe_allow_html=True)
    
    st.write("#### Getting Around")
    st.write("Driving in Sicily is an art form. The Autostrada is efficient, but the real magic happens on the SS (Strada Statale) roads that wind through olive groves.")

# Map at the bottom
st.markdown("---")
map_data = pd.DataFrame([{"lat": d["lat"], "lon": d["lon"], "name": k} for k, d in destinations.items()])
st.map(map_data)
