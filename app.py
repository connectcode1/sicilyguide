import streamlit as st
import pandas as pd

# Page Config
st.set_page_config(page_title="Sicily: A Love Letter", page_icon="🏺", layout="wide")

# Custom CSS for Sicilian Patterns & Deep Colors
st.markdown("""
    <style>
    .main { background-color: #FDF5E6; }
    .stHeader {
        background: linear-gradient(135deg, #005DAA 0%, #D32F2F 50%, #FFD700 100%);
        padding: 30px;
        border-radius: 15px;
        color: white;
        text-align: center;
        border-bottom: 8px solid #D32F2F;
    }
    .city-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        border: 2px solid #005DAA;
        margin-bottom: 25px;
    }
    .human-touch {
        font-style: italic;
        color: #D32F2F;
        border-left: 3px solid #FFD700;
        padding-left: 10px;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# --- THE DEEP DATA ---
destinations = {
    "Palermo: The Glorious Chaos": {
        "description": "Palermo doesn't ask to be liked; it demands to be lived. It’s a city of crumbling palazzos and golden mosaics.",
        "human_tip": "Walk through the Ballarò market at 10 AM. The 'abbanniata' (the vendors' shouting) is a centuries-old opera. If a vendor offers you a piece of cheese, take it with a smile—it's a gesture of hospitality, not a sales pitch.",
        "beaches": ["Mondello (Go to the 'Stabilimenti' for a vintage vibe)", "Capo Gallo (Where the locals hide)"],
        "food_spots": {"I Segreti del Chiostro": "Inside a cloister. Buy the 'Sospiri di Monaca' (Nun's Sighs). They taste like a quiet Sunday afternoon."},
        "activity": "Puppet Theater (Opera dei Pupi). It sounds touristy, but seeing the passion of the puppeteers will make you realize how much we love our legends.",
        "lat": 38.1157, "lon": 13.3615
    },
    "Siracusa: The White Marble Dream": {
        "description": "Ortigia (the old town) feels like an island floating in time. The light here hits the limestone and turns everything honey-colored at sunset.",
        "human_tip": "Sit on the steps of the Cathedral (which was once a Greek temple) around 7 PM. Watch the 'Passeggiata'—grandparents in their Sunday best and teenagers flirting. It’s the heartbeat of our social life.",
        "beaches": ["Fontane Bianche (Caribbean blue)", "Calamosche (A 20-min trek, but the silence is worth it)"],
        "food_spots": {"Caseificio Borderi": "Go to the market and find Gaetano. He doesn't just make sandwiches; he creates edible poetry. Let him choose the ingredients for you."},
        "activity": "The Greek Theater at sunset. Even if there isn't a play, sit on those ancient stones and realize people have been sitting exactly where you are for 2,500 years.",
        "lat": 37.0755, "lon": 15.2866
    },
    "Agrigento: The Valley of Eternity": {
        "description": "Here, the Greek temples stand guard over the sea. It’s a place that makes you feel small in the best way possible.",
        "human_tip": "Visit the Valley of the Temples at *night*. The crowds are gone, the air is cool, and the illuminated columns against the dark sky feel like ghosts of a great civilization.",
        "beaches": ["Scala dei Turchi (White marl cliffs—looks like a giant staircase to the sea)"],
        "food_spots": {"Local Farmhouses": "Look for an 'Agriturismo' nearby. Order anything with 'Pistacchio di Raffadali'—it’s the green gold of this province."},
        "activity": "Garden of Kolymbethra. It’s an ancient irrigation garden. Smell the orange blossoms; that is the true scent of Sicily.",
        "lat": 37.3107, "lon": 13.5765
    },
    "Cefalù: The Norman Jewel": {
        "description": "A postcard-perfect fishing village tucked under a massive rock. It’s where the mountains literally touch the Tyrrhenian sea.",
        "human_tip": "Climb 'La Rocca' early in the morning. You’ll be sweating by the time you reach the Temple of Diana, but looking down at the red-tiled roofs and the crescent beach is the best therapy money can't buy.",
        "beaches": ["Lungomare Cefalù (Easy access)", "Mazforno (More rugged and local)"],
        "food_spots": {"Le Chat Noir": "Tucked in the narrow alleys. Try the Pasta a Taianu—it’s the soul of Cefalù on a plate."},
        "activity": "A sunset swim at the old harbor (Porto Vecchio). The water is calm, and the view of the lit-up houses from the sea is magical.",
        "lat": 38.0369, "lon": 14.0223
    }
}

# --- UI DISPLAY ---
st.markdown('<div class="stHeader"><h1>Benvenuti in Sicilia</h1><p>A guide for my international network, from a local heart.</p></div>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🏛️ The Deep Journey", "🥘 The Rituals", "🧭 Logistics of the Soul"])

with tab1:
    city = st.selectbox("Where does your heart want to go?", list(destinations.keys()))
    data = destinations[city]
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader(city)
        st.write(data["description"])
        st.markdown(f'<div class="human-touch">"{data["human_tip"]}"</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown("### 🏺 Must-Do Activity")
        st.success(data["activity"])
        
    st.divider()
    
    c_beach, c_food = st.columns(2)
    with c_beach:
        st.markdown("### 🏖️ My Favorite Beaches")
        for b in data["beaches"]: st.write(f"• {b}")
    with c_food:
        st.markdown("### 🍽️ The Local Table")
        for spot, desc in data["food_spots"].items():
            st.write(f"**{spot}**: {desc}")

with tab2:
    st.header("How to 'Be' Sicilian")
    st.write("To enjoy Sicily, you must surrender to its rhythm. We don't live to work; we work to live.")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("The Art of Small Talk")
        st.write("Don't be surprised if a shopkeeper asks where you are from and how long you are staying. This isn't an interrogation; it's curiosity. In Sicily, a stranger is just a friend we haven't fed yet.")
    with col_b:
        st.subheader("The 'Granita' Ritual")
        st.write("In summer, breakfast is a lemon or almond granita with a warm brioche. Use the brioche 'tuppo' (the little hat on top) to scoop the ice. If you eat it with a spoon first, we’ll know you're a tourist!")

with tab3:
    st.header("Logistics with Love")
    st.info("### 🚂 The Train vs. The Bus\nOur trains are scenic but slow. For long distances (like Palermo to Agrigento), take the 'Cuffaro' or 'SAIS' buses. They are faster, have AC, and the drivers often treat the bus like their second home.")
    st.warning("### 💧 Water & Sun\nThe 'Scirocco' wind is a hot breath from Africa. If it blows, stay indoors between 1 PM and 4 PM. Drink more water than you think you need—and no, wine doesn't count as water (though we wish it did).")

st.divider()
st.caption("Designed with Sicilian patterns and a touch of salt and sun.")
