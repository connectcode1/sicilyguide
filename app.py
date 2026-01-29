import streamlit as st
import pandas as pd

# Page Config
st.set_page_config(page_title="Sicily Insider", page_icon="🏺", layout="wide")

# --- CUSTOM CSS: MAJOLICA DARK THEME ---
st.markdown("""
    <style>
    /* Main Background: Deep Mediterranean Blue */
    .stApp {
        background-color: #002B5B;
        color: #FDF5E6;
    }
    
    /* High-Contrast Content Cards */
    .content-card {
        background-color: #FDF5E6; /* Noto Stone Cream */
        color: #1A1A1A;
        padding: 25px;
        border-radius: 15px;
        border-left: 10px solid #D32F2F; /* Lava Red */
        margin-bottom: 20px;
    }
    
    /* Headers with Sicilian Gold */
    h1, h2, h3 {
        color: #FFD700 !format;
        font-family: 'Serif';
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #001F3F;
    }
    
    /* Buttons */
    .stButton>button {
        background-color: #D32F2F;
        color: white;
        border-radius: 20px;
        border: 2px solid #FFD700;
    }
    </style>
    """, unsafe_allow_html=True)

# --- DATA ---
destinations = {
    "Palermo & The West": {
        "tagline": "The Arab-Norman Capital",
        "human_tip": "Look up at the ceilings of the Palatine Chapel. The golden mosaics aren't just art; they represent the light of three civilizations meeting.",
        "beaches": ["Mondello", "Riserva dello Zingaro", "San Vito Lo Capo"],
        "food": ["Panelle at Ballarò", "Cannoli at Santa Caterina"],
        "lat": 38.1157, "lon": 13.3615
    },
    "Siracusa & The Baroque": {
        "tagline": "The White Soul of the Sea",
        "human_tip": "When in Ortigia, buy a sandwich at Borderi. Don't look at the menu; let Gaetano build a masterpiece for you based on his mood.",
        "beaches": ["Fontane Bianche", "Calamosche", "Vendicari"],
        "food": ["Pistachio everything in Noto", "Fresh Tuna in Marzamemi"],
        "lat": 37.0755, "lon": 15.2866
    },
    "Etna & The East": {
        "tagline": "Fire and Volcanic Wines",
        "human_tip": "Visit a winery on the north slope of Etna. The 'Nerello Mascalese' grapes grow in volcanic ash, giving the wine a smoky taste of the earth.",
        "beaches": ["Isola Bella", "San Giovanni Li Cuti"],
        "food": ["Granita at Bam Bar", "Arancino at Savia"],
        "lat": 37.5027, "lon": 15.0873
    }
}

# --- HEADER SECTION ---
st.title("🏺 Sicilia: An Insider's Love Letter")
st.markdown("### A curated portal for my international network.")
st.divider()

# --- INTERACTIVE MAP ---
st.subheader("📍 Mapping the Magic")
map_data = pd.DataFrame([{"lat": d["lat"], "lon": d["lon"], "name": k} for k, d in destinations.items()])
st.map(map_data)

# --- MAIN NAVIGATION ---
tab1, tab2, tab3 = st.tabs(["🏛️ Deep Guide", "🧭 Itineraries", "💬 Your Feedback"])

with tab1:
    region = st.selectbox("Where are we heading?", list(destinations.keys()))
    res = destinations[region]
    
    # Using the Content Card for readability
    st.markdown(f"""
    <div class="content-card">
        <h2 style="color: #002B5B;">{region}</h2>
        <p><strong>{res['tagline']}</strong></p>
        <p style="font-style: italic; border-left: 3px solid #FFD700; padding-left: 10px;">"{res['human_tip']}"</p>
        <hr>
        <div style="display: flex; justify-content: space-between;">
            <div>
                <h4>🏖️ Beaches</h4>
                <ul>{" ".join([f"<li>{b}</li>" for b in res['beaches']])}</ul>
            </div>
            <div>
                <h4>🍴 Food Spots</h4>
                <ul>{" ".join([f"<li>{f}</li>" for f in res['food']])}</ul>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with tab2:
    st.subheader("📅 Curated Paths")
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("**The 5-Day East Coast Loop**\nCatania (Etna) -> Taormina -> Siracusa -> Noto.")
    with col2:
        st.info("**The 5-Day West Coast Charm**\nPalermo -> Cefalù -> Erice -> San Vito Lo Capo.")



with tab3:
    st.subheader("📮 Help me improve this guide!")
    with st.form("feedback_form"):
        name = st.text_input("Your Name")
        rating = st.slider("How helpful is this guide?", 1, 5, 5)
        comment = st.text_area("What city should I add next?")
        
        submitted = st.form_submit_button("Send Feedback")
        if submitted:
            st.success(f"Grazie, {name}! Your feedback makes this guide better.")
            # In a real app, you'd save this to a file or database
            st.balloons()

# --- FOOTER ---
st.divider()
st.markdown("<p style='text-align: center;'>Made with ❤️ in Sicily. For private use within our network.</p>", unsafe_allow_html=True)
