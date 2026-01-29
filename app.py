import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import json

# Page Config
st.set_page_config(
    page_title="Sicilia Autentica - Your Insider's Journey", 
    page_icon="🌅", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- SICILIAN DREAMY CSS THEME ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;600;700&family=Montserrat:wght@300;400;500&display=swap');
    
    /* Main Background - Mediterranean Sunset Gradient */
    .stApp {
        background: linear-gradient(180deg, 
            #0a1828 0%,
            #1e3a5f 20%,
            #2d5f8d 40%,
            #f4a261 80%,
            #e76f51 100%);
        background-attachment: fixed;
        color: #fefae0;
        font-family: 'Montserrat', sans-serif;
    }
    
    /* Elegant Content Cards with Sicilian Ceramic Pattern */
    .content-card {
        background: linear-gradient(135deg, #fefae0 0%, #faf3dd 100%);
        color: #1a1a1a;
        padding: 40px;
        border-radius: 25px;
        border: 3px solid #e9c46a;
        margin: 25px 0;
        box-shadow: 
            0 20px 60px rgba(0,0,0,0.3),
            inset 0 1px 0 rgba(255,255,255,0.8);
        position: relative;
        overflow: hidden;
    }
    
    .content-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 8px;
        background: repeating-linear-gradient(
            90deg,
            #e76f51 0px,
            #e76f51 20px,
            #f4a261 20px,
            #f4a261 40px,
            #2a9d8f 40px,
            #2a9d8f 60px
        );
    }
    
    /* Dreamy Info Cards */
    .info-card {
        background: rgba(42, 157, 143, 0.15);
        backdrop-filter: blur(10px);
        border: 2px solid #2a9d8f;
        border-radius: 20px;
        padding: 25px;
        margin: 20px 0;
        box-shadow: 0 8px 32px rgba(42, 157, 143, 0.2);
    }
    
    /* Headers - Elegant Serif */
    h1 {
        font-family: 'Cormorant Garamond', serif !important;
        color: #fefae0 !important;
        font-weight: 700 !important;
        font-size: 4em !important;
        text-shadow: 
            2px 2px 4px rgba(0,0,0,0.6),
            0 0 20px rgba(233, 196, 106, 0.4);
        margin-bottom: 10px !important;
        letter-spacing: 2px;
    }
    
    h2 {
        font-family: 'Cormorant Garamond', serif !important;
        color: #e9c46a !important;
        font-weight: 600 !important;
        font-size: 2.5em !important;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.5);
        margin-top: 30px !important;
    }
    
    h3 {
        font-family: 'Cormorant Garamond', serif !important;
        color: #f4a261 !important;
        font-weight: 600 !important;
        font-size: 1.8em !important;
    }
    
    /* Sidebar - Terracotta Elegance */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e3a5f 0%, #264653 100%);
        border-right: 5px solid #e9c46a;
        padding: 20px;
    }
    
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #e9c46a !important;
    }
    
    section[data-testid="stSidebar"] p {
        color: #fefae0;
    }
    
    /* Elegant Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #e76f51 0%, #f4a261 100%);
        color: #fefae0;
        border-radius: 30px;
        border: 3px solid #e9c46a;
        font-weight: 600;
        padding: 15px 35px;
        font-size: 1.1em;
        font-family: 'Montserrat', sans-serif;
        letter-spacing: 1px;
        transition: all 0.4s ease;
        box-shadow: 0 5px 15px rgba(231, 111, 81, 0.4);
    }
    
    .stButton>button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 8px 25px rgba(231, 111, 81, 0.6);
        background: linear-gradient(135deg, #f4a261 0%, #e9c46a 100%);
        border-color: #fefae0;
    }
    
    /* Tabs - Mediterranean Wave Design */
    .stTabs [data-baseweb="tab-list"] {
        gap: 15px;
        background: rgba(42, 157, 143, 0.1);
        padding: 15px;
        border-radius: 20px;
        backdrop-filter: blur(5px);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(254, 250, 224, 0.1);
        border-radius: 15px;
        color: #fefae0;
        font-weight: 600;
        padding: 15px 30px;
        font-family: 'Montserrat', sans-serif;
        border: 2px solid transparent;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(233, 196, 106, 0.2);
        border-color: #e9c46a;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #e9c46a 0%, #f4a261 100%);
        color: #1a1a1a;
        border-color: #fefae0;
        box-shadow: 0 5px 20px rgba(233, 196, 106, 0.4);
    }
    
    /* Expanders - Ceramic Tile Inspired */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, rgba(42, 157, 143, 0.3) 0%, rgba(42, 157, 143, 0.1) 100%);
        border-radius: 15px;
        font-weight: 600;
        border: 2px solid #2a9d8f;
        color: #fefae0 !important;
        padding: 15px !important;
        font-size: 1.1em;
    }
    
    .streamlit-expanderHeader:hover {
        background: rgba(42, 157, 143, 0.4);
        border-color: #e9c46a;
    }
    
    /* Metrics - Elegant Display */
    [data-testid="stMetricValue"] {
        color: #e9c46a;
        font-size: 2.5em;
        font-family: 'Cormorant Garamond', serif;
        font-weight: 700;
    }
    
    [data-testid="stMetricLabel"] {
        color: #fefae0;
        font-weight: 500;
        font-size: 1.1em;
    }
    
    /* Input Fields */
    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea,
    .stSelectbox>div>div>select {
        background: rgba(254, 250, 224, 0.9);
        border: 2px solid #e9c46a;
        border-radius: 15px;
        color: #1a1a1a;
        font-family: 'Montserrat', sans-serif;
        padding: 12px;
    }
    
    /* Form Submit Button Special */
    .stForm button[type="submit"] {
        background: linear-gradient(135deg, #2a9d8f 0%, #264653 100%);
        border-color: #e9c46a;
    }
    
    .stForm button[type="submit"]:hover {
        background: linear-gradient(135deg, #e76f51 0%, #f4a261 100%);
    }
    
    /* Dividers */
    hr {
        border: none;
        height: 3px;
        background: linear-gradient(90deg, 
            transparent 0%, 
            #e9c46a 20%, 
            #f4a261 50%, 
            #e9c46a 80%, 
            transparent 100%);
        margin: 40px 0;
    }
    
    /* Success/Info/Warning Messages */
    .stSuccess {
        background: rgba(42, 157, 143, 0.2);
        border: 2px solid #2a9d8f;
        border-radius: 15px;
        color: #fefae0;
    }
    
    .stInfo {
        background: rgba(233, 196, 106, 0.2);
        border: 2px solid #e9c46a;
        border-radius: 15px;
        color: #fefae0;
    }
    
    .stWarning {
        background: rgba(244, 162, 97, 0.2);
        border: 2px solid #f4a261;
        border-radius: 15px;
        color: #fefae0;
    }
    
    /* Bookmarks Style */
    .bookmark-item {
        background: rgba(42, 157, 143, 0.15);
        border-left: 5px solid #e9c46a;
        padding: 15px;
        margin: 10px 0;
        border-radius: 10px;
        backdrop-filter: blur(5px);
    }
    
    /* Review Card */
    .review-card {
        background: linear-gradient(135deg, rgba(254, 250, 224, 0.1) 0%, rgba(233, 196, 106, 0.1) 100%);
        border: 2px solid #e9c46a;
        border-radius: 20px;
        padding: 25px;
        margin: 15px 0;
        backdrop-filter: blur(10px);
    }
    
    /* Footer */
    .footer-link {
        color: #e9c46a;
        text-decoration: none;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .footer-link:hover {
        color: #fefae0;
        text-shadow: 0 0 10px rgba(233, 196, 106, 0.6);
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(26, 58, 95, 0.5);
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #e9c46a 0%, #f4a261 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #f4a261 0%, #e76f51 100%);
    }
    
    /* Rating Stars */
    .star-rating {
        color: #e9c46a;
        font-size: 1.5em;
        letter-spacing: 3px;
    }
    
    /* Decorative Elements */
    .decorative-icon {
        font-size: 3em;
        color: #e9c46a;
        text-shadow: 0 0 20px rgba(233, 196, 106, 0.4);
    }
    </style>
    """, unsafe_allow_html=True)

# --- INITIALIZE SESSION STATE ---
if 'saved_trips' not in st.session_state:
    st.session_state.saved_trips = []
if 'feedback_data' not in st.session_state:
    st.session_state.feedback_data = []
if 'bookmarks' not in st.session_state:
    st.session_state.bookmarks = []
if 'reviews' not in st.session_state:
    st.session_state.reviews = []
if 'user_name' not in st.session_state:
    st.session_state.user_name = "Traveler"

# --- COMPREHENSIVE DATA ---
destinations = {
    "Palermo & The West": {
        "tagline": "The Arab-Norman Capital - Where Three Worlds Meet",
        "description": """Palermo is a vibrant, chaotic masterpiece where Byzantine mosaics gleam alongside Arab domes 
        and Norman fortifications. The city's soul lives in its markets—Ballarò, Vucciria, and Capo—where vendors 
        shout in dialect and the air smells of saffron, fresh fish, and ancient stone. This is Sicily at its most 
        authentic: unpolished, passionate, and utterly unforgettable.""",
        
        "human_tip": """🎨 **Insider Secret**: Visit the Palatine Chapel at 3 PM on a sunny day. The light hits the 
        golden mosaics at an angle that makes them appear to move. The craftsmen who created this knew exactly what 
        they were doing—they built a physical manifestation of divine light.""",
        
        "beaches": {
            "Mondello": {
                "description": "Palermo's beach paradise with turquoise waters and Art Nouveau bathhouses",
                "best_for": "Families, swimming, sunset aperitivo",
                "how_to_get": "15 min bus from Palermo center (Line 806)",
                "insider_tip": "Avoid August weekends. Go on weekday mornings for a local experience."
            },
            "Riserva dello Zingaro": {
                "description": "7km of pristine, protected coastline with hidden coves accessible only on foot",
                "best_for": "Hiking, snorkeling, nature photography",
                "how_to_get": "Bus to Scopello, then 20 min walk to entrance",
                "insider_tip": "Start from the northern entrance at San Vito and walk south—easier terrain."
            },
            "San Vito Lo Capo": {
                "description": "Caribbean-like white sand beach beneath Monte Monaco",
                "best_for": "Beach lounging, couscous festival (September)",
                "how_to_get": "Bus from Palermo (2 hours) or Trapani (1 hour)",
                "insider_tip": "Stay until sunset—the mountain turns pink and gold."
            }
        },
        
        "food": {
            "Panelle at Ballarò Market": {
                "what": "Chickpea fritters on sesame bread",
                "where": "Antica Friggitoria Ballarò",
                "price": "€3-4",
                "insider": "Add crocchè (potato croquettes) and ask for extra lemon"
            },
            "Cannoli at Pasticceria Cappello": {
                "what": "The city's best cannoli, filled only when you order",
                "where": "Via Colonna Rotta (near Quattro Canti)",
                "price": "€2.50 each",
                "insider": "Try ricotta with pistachio cream—it's life-changing"
            },
            "Pasta con le Sarde": {
                "what": "Traditional pasta with sardines, wild fennel, pine nuts, raisins",
                "where": "Trattoria Ai Cascinari",
                "price": "€12-15",
                "insider": "This is Palermo's signature dish—you must try it"
            }
        },
        
        "must_see": [
            "🏛️ Palatine Chapel - Book tickets in advance",
            "🕌 Cathedral of Palermo - Free entry, rooftop tour €7",
            "💀 Capuchin Catacombs - Not for the faint-hearted",
            "🎭 Teatro Massimo - Take the guided tour",
            "🏖️ Mondello Beach - Best reached by morning"
        ],
        
        "hidden_gems": [
            "📚 Biblioteca Comunale - Stunning reading rooms, free entry",
            "🌳 Orto Botanico - Peaceful gardens from 1795",
            "🎨 Palazzo Abatellis - Medieval art in a renaissance palace",
            "🍷 Enoteca Picone - Wine shop with 4,000+ Sicilian labels"
        ],
        
        "lat": 38.1157, 
        "lon": 13.3615,
        "best_months": "April-June, September-October",
        "days_needed": "3-4 days",
        "emoji": "🏛️"
    },
    
    "Siracusa & The Baroque Southeast": {
        "tagline": "The White Soul of the Sea - Baroque Perfection",
        "description": """Syracuse was once the most powerful Greek city in the Mediterranean, rivaling Athens itself. 
        Today, its island quarter Ortigia is a labyrinth of honey-colored baroque buildings, hidden courtyards, and 
        piazzas that feel like outdoor living rooms. The surrounding towns—Noto, Modica, Ragusa—form the Baroque Valley, 
        a UNESCO treasure built after the 1693 earthquake in a unified vision of architectural magnificence.""",
        
        "human_tip": """🥪 **The Borderi Experience**: This isn't just a sandwich shop in Ortigia—it's a philosophy. 
        Gaetano doesn't ask what you want; he asks where you're from, what you've eaten today, and how you're feeling. 
        Then he creates. Trust the process. I've seen grown men cry over his tuna creations.""",
        
        "beaches": {
            "Fontane Bianche": {
                "description": "Fine white sand and shallow crystal waters",
                "best_for": "Families with kids, beach clubs",
                "how_to_get": "20 min bus from Syracuse center",
                "insider_tip": "The free public beach is at the southern end—just as beautiful"
            },
            "Calamosche": {
                "description": "Secluded beach in Vendicari Reserve, surrounded by cliffs",
                "best_for": "Couples, nature lovers, photography",
                "how_to_get": "Car recommended, 30 min from Noto + 20 min walk",
                "insider_tip": "Arrive before 10 AM or after 4 PM to avoid crowds"
            },
            "Vendicari": {
                "description": "Nature reserve with multiple beaches and flamingo spotting",
                "best_for": "Birdwatching, hiking, wild beaches",
                "how_to_get": "Bus to Noto, then taxi to entrances",
                "insider_tip": "San Lorenzo beach is quieter than Calamosche"
            }
        },
        
        "food": {
            "Pistachio Everything in Noto": {
                "what": "Gelato, granita, pasta, pesto—all with Bronte pistachios",
                "where": "Caffè Sicilia (famous from Chef's Table)",
                "price": "€4-6 for granita",
                "insider": "The almond granita with brioche is equally legendary"
            },
            "Fresh Tuna in Marzamemi": {
                "what": "Tuna tartare, spaghetti, grilled steaks",
                "where": "La Cialoma or Campisi",
                "price": "€15-25",
                "insider": "Visit during the Tuna Festival in May"
            },
            "Modica Chocolate": {
                "what": "Ancient Aztec-style grainy chocolate",
                "where": "Antica Dolceria Bonajuto",
                "price": "€5-8 per bar",
                "insider": "Try the chili pepper variety—it's traditional"
            }
        },
        
        "must_see": [
            "🏛️ Ortigia Island - Get lost in the alleys",
            "⛲ Arethusa Spring - Legend of the nymph",
            "🎭 Greek Theater - Summer performances are magical",
            "⛪ Noto Cathedral - Recently restored baroque jewel",
            "🏰 Ragusa Ibla - The other Baroque capital"
        ],
        
        "hidden_gems": [
            "🎨 Palazzo Nicolaci balconies in Noto - Baroque grotesque art",
            "🍷 Wine tasting in Pachino - Nero d'Avola territory",
            "🏖️ Isola delle Correnti - Italy's southernmost point",
            "📖 Libreria Arcadia in Ortigia - Charming bookshop café"
        ],
        
        "lat": 37.0755, 
        "lon": 15.2866,
        "best_months": "May-June, September",
        "days_needed": "4-5 days",
        "emoji": "⛪"
    },
    
    "Etna & The East Coast": {
        "tagline": "Fire and Wine - Living with the Volcano",
        "description": """Mount Etna isn't just a volcano—it's Sicily's defining force. Europe's most active volcano 
        shapes everything: the soil (volcanic ash perfect for wine), the weather (sudden changes as clouds hit the peak), 
        the culture (a mix of respect and defiance). The east coast from Catania to Taormina offers urban energy, 
        resort elegance, and the raw power of nature all within 50km.""",
        
        "human_tip": """🍷 **Volcanic Wine Secret**: Visit Passopisciaro or Terre Nere wineries on Etna's north slope. 
        The 'Nerello Mascalese' vines grow in ash and lava stones at 800m altitude. The wine tastes like the mountain 
        itself—smoky, mineral, powerful yet elegant. This is terroir in its purest form.""",
        
        "beaches": {
            "Isola Bella": {
                "description": "Tiny island connected to shore, nature reserve",
                "best_for": "Snorkeling, photos, iconic views",
                "how_to_get": "Below Taormina, cable car or walking path",
                "insider_tip": "Visit early morning before tour groups arrive"
            },
            "San Giovanni Li Cuti": {
                "description": "Catania's black lava stone beach, local scene",
                "best_for": "Sunset, local atmosphere, seafood",
                "how_to_get": "Walking distance from Catania center",
                "insider_tip": "Have aperitivo at the beach bars at 7 PM"
            }
        },
        
        "food": {
            "Granita at Bam Bar": {
                "what": "Legendary almond granita with warm brioche",
                "where": "Via di Giovanni, Taormina",
                "price": "€6-8",
                "insider": "Arrive before 11 AM for best brioche"
            },
            "Arancino at Savia": {
                "what": "Catania's iconic rice balls, best in the city",
                "where": "Via Etnea, Catania",
                "price": "€2.50-3",
                "insider": "Try 'al burro' (butter/ham) and 'al ragù' (meat)"
            },
            "Pasta alla Norma": {
                "what": "Catania's pride—pasta with eggplant, ricotta salata, tomato",
                "where": "Trattoria de Fiore, Catania",
                "price": "€10-12",
                "insider": "Named after Bellini's opera—both are Catanese masterpieces"
            }
        },
        
        "must_see": [
            "🌋 Mount Etna - Guided tour to summit craters (€65)",
            "🎭 Taormina Ancient Theater - Greek theater with Etna backdrop",
            "🐘 Catania Fish Market - Sensory overload, arrive early",
            "🏛️ Catania Baroque Center - UNESCO site, rebuilt after 1693"
        ],
        
        "hidden_gems": [
            "🍷 Etna Wine Route - Dozens of wineries to visit",
            "🏰 Castello di Aci - Norman castle over the sea",
            "🎵 Bellini Museum in Catania - Opera composer's birthplace",
            "🌳 Gole Alcantara - Lava gorge with river"
        ],
        
        "lat": 37.5027, 
        "lon": 15.0873,
        "best_months": "April-June, September-October",
        "days_needed": "3-4 days",
        "emoji": "🌋"
    }
}

# --- ELEGANT HEADER ---
st.markdown("""
    <div style='text-align: center; padding: 60px 20px 40px 20px;'>
        <div class='decorative-icon'>🌅</div>
        <h1 style='margin: 20px 0 10px 0;'>SICILIA AUTENTICA</h1>
        <p style='font-size: 1.5em; color: #e9c46a; font-family: "Cormorant Garamond", serif; font-style: italic; margin: 10px 0;'>
            Un Viaggio nell'Anima dell'Isola
        </p>
        <p style='font-size: 1.1em; color: #fefae0; font-weight: 300; margin: 10px 0;'>
            Your Personal Insider's Guide to the Heart of the Mediterranean
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# --- ELEGANT SIDEBAR ---
with st.sidebar:
    st.markdown("""
        <div style='text-align: center; padding: 20px 0;'>
            <div class='decorative-icon' style='font-size: 2.5em;'>🏺</div>
            <h2 style='margin: 15px 0;'>Navigation</h2>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<hr style='margin: 20px 0;'>", unsafe_allow_html=True)
    
    # User Greeting
    user_greeting = st.text_input("👤 Your name", value=st.session_state.user_name, key="user_name_input")
    if user_greeting != st.session_state.user_name:
        st.session_state.user_name = user_greeting
        st.rerun()
    
    st.markdown(f"""
        <p style='text-align: center; font-size: 1.2em; color: #e9c46a; margin: 15px 0;'>
            Benvenuto, <strong>{st.session_state.user_name}</strong>! 🌊
        </p>
        """, unsafe_allow_html=True)
    
    st.markdown("<hr style='margin: 20px 0;'>", unsafe_allow_html=True)
    
    # Quick Stats
    st.markdown("### 📊 Your Journey Stats")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("📌 Saved", len(st.session_state.bookmarks))
    with col2:
        st.metric("🗺️ Trips", len(st.session_state.saved_trips))
    
    st.metric("⭐ Reviews", len(st.session_state.reviews))
    
    st.markdown("<hr style='margin: 20px 0;'>", unsafe_allow_html=True)
    
    # Quick Actions
    st.markdown("### ⚡ Quick Actions")
    
    if st.button("🗺️ Jump to Map", use_container_width=True):
        st.info("Scroll down to see the interactive map!")
    
    if st.button("💾 My Dashboard", use_container_width=True):
        st.info("Navigate to 'My Dashboard' tab above!")
    
    st.markdown("<hr style='margin: 20px 0;'>", unsafe_allow_html=True)
    
    # Recent Bookmarks
    st.markdown("### 📌 Recent Bookmarks")
    if st.session_state.bookmarks:
        recent = list(st.session_state.bookmarks)[-3:]
        for item in recent:
            st.markdown(f"<div class='bookmark-item'>✓ {item}</div>", unsafe_allow_html=True)
    else:
        st.markdown("<p style='color: #e9c46a; font-style: italic;'>No bookmarks yet</p>", unsafe_allow_html=True)

# --- MAIN CONTENT TABS ---
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🏛️ Explore Regions",
    "🧳 Plan Your Trip",
    "💬 Community & Reviews",
    "📋 Practical Guide",
    "❓ Ask & Discover",
    "📊 My Dashboard"
])

# ============================================
# TAB 1: EXPLORE REGIONS
# ============================================
with tab1:
    st.markdown("""
        <div style='text-align: center; padding: 30px 0;'>
            <h2>Discover Sicily's Magic</h2>
            <p style='font-size: 1.2em; color: #e9c46a;'>Choose a region to begin your journey</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Region selector with emojis
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        selected_region = st.selectbox(
            "🗺️ Select Your Destination",
            list(destinations.keys()),
            format_func=lambda x: f"{destinations[x]['emoji']} {x}",
            key="region_selector"
        )
    
    region_data = destinations[selected_region]
    
    # Hero Section
    st.markdown(f"""
    <div class="content-card">
        <div style='text-align: center;'>
            <div class='decorative-icon'>{region_data['emoji']}</div>
            <h1 style="color: #e76f51; margin: 20px 0; font-size: 2.5em;">{selected_region}</h1>
            <h3 style="color: #264653; font-style: italic; margin-bottom: 25px;">"{region_data['tagline']}"</h3>
        </div>
        <p style="font-size: 1.15em; line-height: 1.8; color: #264653; text-align: justify;">
            {region_data['description']}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Bookmark button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button(f"🔖 Bookmark {selected_region}", use_container_width=True, key="bookmark_region"):
            if selected_region not in st.session_state.bookmarks:
                st.session_state.bookmarks.append(selected_region)
                st.success(f"✨ Added to your collection!")
                st.balloons()
            else:
                st.info("Already in your bookmarks!")
    
    # Insider Tip
    st.markdown(f"""
    <div class="info-card">
        <div style='text-align: center;'>
            <h3 style="color: #e9c46a;">💡 Insider's Secret</h3>
        </div>
        <p style="font-size: 1.1em; line-height: 1.7; color: #fefae0; padding: 15px;">
            {region_data['human_tip']}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick Info Metrics
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🗓️ Recommended Stay", region_data['days_needed'])
    with col2:
        st.metric("🌞 Best Season", region_data['best_months'])
    with col3:
        st.metric("🏖️ Featured Beaches", len(region_data['beaches']))
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Beaches Section
    st.markdown("""
        <div style='text-align: center; padding: 20px 0;'>
            <h2>🏖️ Coastal Treasures</h2>
            <p style='color: #e9c46a; font-size: 1.1em;'>Discover the most beautiful beaches and coves</p>
        </div>
        """, unsafe_allow_html=True)
    
    for beach_name, beach_info in region_data['beaches'].items():
        with st.expander(f"🌊 {beach_name}", expanded=False):
            st.markdown(f"""
            <div class="content-card" style="padding: 25px;">
                <h3 style="color: #2a9d8f; margin-bottom: 15px;">{beach_name}</h3>
                <p style="font-size: 1.05em; color: #264653; line-height: 1.6;">
                    📍 <strong>{beach_info['description']}</strong>
                </p>
                <br>
                <div style="background: rgba(42, 157, 143, 0.1); padding: 15px; border-radius: 10px; margin: 10px 0;">
                    <p style="color: #264653;"><strong>🎯 Best for:</strong> {beach_info['best_for']}</p>
                    <p style="color: #264653;"><strong>🚗 How to get there:</strong> {beach_info['how_to_get']}</p>
                </div>
                <div style="background: rgba(233, 196, 106, 0.15); padding: 15px; border-radius: 10px; margin: 15px 0; border-left: 4px solid #e9c46a;">
                    <p style="color: #264653;"><strong>💎 Insider Tip:</strong> {beach_info['insider_tip']}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"📍 Get Directions", key=f"dir_{beach_name}"):
                    st.success(f"Opening maps for {beach_name}...")
            with col2:
                if st.button(f"💾 Save Beach", key=f"save_beach_{beach_name}"):
                    bookmark_text = f"{beach_name} - {selected_region}"
                    if bookmark_text not in st.session_state.bookmarks:
                        st.session_state.bookmarks.append(bookmark_text)
                        st.success("Saved!")
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Food Section
    st.markdown("""
        <div style='text-align: center; padding: 20px 0;'>
            <h2>🍴 Culinary Delights</h2>
            <p style='color: #e9c46a; font-size: 1.1em;'>Must-try dishes and where to find them</p>
        </div>
        """, unsafe_allow_html=True)
    
    for food_name, food_info in region_data['food'].items():
        with st.expander(f"🍽️ {food_name}", expanded=False):
            st.markdown(f"""
            <div class="content-card" style="padding: 25px;">
                <h3 style="color: #e76f51; margin-bottom: 15px;">{food_name}</h3>
                <p style="font-size: 1.05em; color: #264653;"><strong>What it is:</strong> {food_info['what']}</p>
                <p style="font-size: 1.05em; color: #264653;"><strong>📍 Where:</strong> {food_info['where']}</p>
                <p style="font-size: 1.05em; color: #264653;"><strong>💰 Price:</strong> {food_info['price']}</p>
                <div style="background: rgba(244, 162, 97, 0.15); padding: 15px; border-radius: 10px; margin: 15px 0; border-left: 4px solid #f4a261;">
                    <p style="color: #264653;"><strong>✨ Insider Tip:</strong> {food_info['insider']}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"🔖 Save this spot", key=f"save_food_{food_name}"):
                bookmark_text = f"{food_name} - {selected_region}"
                if bookmark_text not in st.session_state.bookmarks:
                    st.session_state.bookmarks.append(bookmark_text)
                    st.success("Added to bookmarks!")
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Attractions
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class="info-card">
                <h3 style="text-align: center; color: #e9c46a;">⭐ Must-See Attractions</h3>
            </div>
            """, unsafe_allow_html=True)
        for item in region_data['must_see']:
            st.markdown(f"<p style='font-size: 1.05em; padding: 5px 0;'>{item}</p>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="info-card">
                <h3 style="text-align: center; color: #e9c46a;">💎 Hidden Gems</h3>
            </div>
            """, unsafe_allow_html=True)
        for item in region_data['hidden_gems']:
            st.markdown(f"<p style='font-size: 1.05em; padding: 5px 0;'>{item}</p>", unsafe_allow_html=True)

# ============================================
# TAB 2: PLAN YOUR TRIP
# ============================================
with tab2:
    st.markdown("""
        <div style='text-align: center; padding: 30px 0;'>
            <h2>✨ Craft Your Perfect Journey</h2>
            <p style='font-size: 1.2em; color: #e9c46a;'>Let us help you create an unforgettable experience</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="content-card">
        <h3 style="color: #2a9d8f; text-align: center;">🎯 Trip Builder</h3>
        <p style="text-align: center; color: #264653;">Tell us about your dream Sicily trip</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Trip Planning Form
    with st.form("trip_planner", clear_on_submit=False):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            trip_duration = st.number_input("📅 How many days?", min_value=2, max_value=30, value=7)
        
        with col2:
            travel_style = st.selectbox("🎨 Travel Style", [
                "🏖️ Beach & Relaxation",
                "🏛️ Culture & History",
                "🍷 Food & Wine",
                "🥾 Adventure & Nature",
                "✨ Balanced Mix"
            ])
        
        with col3:
            start_point = st.selectbox("🛬 Starting City", [
                "Palermo", 
                "Catania", 
                "Syracuse"
            ])
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("#### 🎯 Select Your Interests")
        col1, col2, col3, col4 = st.columns(4)
        
        interests = []
        with col1:
            if st.checkbox("🏖️ Beaches"): interests.append("Beaches")
            if st.checkbox("🏛️ Ancient Sites"): interests.append("Ancient Sites")
        with col2:
            if st.checkbox("🍷 Food & Wine"): interests.append("Food & Wine")
            if st.checkbox("🌳 Nature"): interests.append("Nature")
        with col3:
            if st.checkbox("⛪ Baroque Towns"): interests.append("Baroque Towns")
            if st.checkbox("⛵ Islands"): interests.append("Islands")
        with col4:
            if st.checkbox("🛒 Markets"): interests.append("Markets")
            if st.checkbox("🎭 Nightlife"): interests.append("Nightlife")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        trip_name = st.text_input("🏷️ Name your trip (optional)", placeholder="e.g., 'Summer Sicily 2026'")
        
        submit_trip = st.form_submit_button("✨ Create My Itinerary", use_container_width=True)
        
        if submit_trip:
            # Save trip
            new_trip = {
                'name': trip_name if trip_name else f"{travel_style} - {trip_duration} days",
                'duration': trip_duration,
                'style': travel_style,
                'start': start_point,
                'interests': interests,
                'date_created': datetime.now().strftime("%B %d, %Y")
            }
            st.session_state.saved_trips.append(new_trip)
            
            st.success("🎉 Your personalized itinerary is ready!")
            st.balloons()
            
            st.markdown(f"""
            <div class="content-card">
                <h2 style="color: #2a9d8f; text-align: center;">🗺️ Your {trip_duration}-Day Sicily Journey</h2>
                <h3 style="text-align: center; color: #264653; font-style: italic;">"{new_trip['name']}"</h3>
                <br>
                <div style="background: rgba(42, 157, 143, 0.1); padding: 20px; border-radius: 15px;">
                    <h3 style="color: #e76f51;">Days 1-2: {start_point}</h3>
                    <p style="color: #264653; font-size: 1.05em;">
                        🏨 Arrive and settle in<br>
                        🏛️ Explore the historic center and main attractions<br>
                        🍴 Experience local street food and markets<br>
                        🌅 Sunset walk and aperitivo
                    </p>
                </div>
                <br>
                <div style="background: rgba(233, 196, 106, 0.1); padding: 20px; border-radius: 15px;">
                    <h3 style="color: #e76f51;">Days 3-{min(5, trip_duration)}: Coastal Exploration</h3>
                    <p style="color: #264653; font-size: 1.05em;">
                        🏖️ Beach hopping and swimming<br>
                        🍷 Wine tasting in countryside<br>
                        📸 Hidden gems and local villages<br>
                        🌊 Boat trips or water activities
                    </p>
                </div>
                <br>
                <div style="background: rgba(244, 162, 97, 0.1); padding: 20px; border-radius: 15px;">
                    <h3 style="color: #e76f51;">Final Days: Baroque & Culture</h3>
                    <p style="color: #264653; font-size: 1.05em;">
                        ⛪ UNESCO Baroque towns<br>
                        🏛️ Archaeological sites<br>
                        🛍️ Souvenir shopping<br>
                        🍝 Final feast and arrivederci
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.info("💾 Itinerary saved to 'My Dashboard' for future reference!")

# ============================================
# TAB 3: COMMUNITY & REVIEWS
# ============================================
with tab3:
    st.markdown("""
        <div style='text-align: center; padding: 30px 0;'>
            <h2>💬 Join Our Community</h2>
            <p style='font-size: 1.2em; color: #e9c46a;'>Share your experiences and discover from fellow travelers</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Sub-tabs for community
    comm_tab1, comm_tab2, comm_tab3 = st.tabs([
        "⭐ Reviews & Ratings",
        "💡 Share Your Tips",
        "📮 Feedback"
    ])
    
    with comm_tab1:
        st.markdown("""
            <div class="content-card">
                <h3 style="color: #2a9d8f; text-align: center;">⭐ Rate Your Experience</h3>
                <p style="text-align: center; color: #264653;">Help fellow travelers with your insights</p>
            </div>
            """, unsafe_allow_html=True)
        
        with st.form("review_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                review_type = st.selectbox("📍 What are you reviewing?", [
                    "Restaurant",
                    "Beach",
                    "Hotel/Accommodation",
                    "Attraction",
                    "Tour/Experience"
                ])
                place_name = st.text_input("🏷️ Name of place")
            
            with col2:
                location = st.selectbox("📍 Location", list(destinations.keys()))
                rating = st.slider("⭐ Your rating", 1, 5, 4)
            
            visit_date = st.date_input("📅 When did you visit?", value=datetime.now() - timedelta(days=30))
            
            would_recommend = st.radio("👍 Would you recommend this?", 
                ["✅ Absolutely!", "👌 Yes, with reservations", "❌ Not really"], 
                horizontal=True)
            
            review_text = st.text_area(
                "✍️ Share your experience",
                height=150,
                placeholder="What made it special? Any tips for future visitors? What should people know?"
            )
            
            reviewer_name = st.text_input("👤 Your name (optional)", value=st.session_state.user_name)
            
            submit_review = st.form_submit_button("🌟 Submit Review", use_container_width=True)
            
            if submit_review and place_name and review_text:
                new_review = {
                    'type': review_type,
                    'place': place_name,
                    'location': location,
                    'rating': rating,
                    'recommend': would_recommend,
                    'review': review_text,
                    'reviewer': reviewer_name,
                    'date': visit_date.strftime("%B %d, %Y"),
                    'timestamp': datetime.now()
                }
                st.session_state.reviews.append(new_review)
                
                st.success("🎉 Thank you for sharing your experience!")
                st.balloons()
                st.info("Your review has been added to the community!")
        
        # Display recent reviews
        if st.session_state.reviews:
            st.markdown("<br><hr><br>", unsafe_allow_html=True)
            st.markdown("""
                <div style='text-align: center;'>
                    <h3 style="color: #e9c46a;">📜 Recent Community Reviews</h3>
                </div>
                """, unsafe_allow_html=True)
            
            for review in reversed(st.session_state.reviews[-5:]):  # Show last 5 reviews
                stars = "⭐" * review['rating']
                st.markdown(f"""
                <div class="review-card">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                        <div>
                            <h3 style="color: #e9c46a; margin: 0;">{review['place']}</h3>
                            <p style="color: #fefae0; margin: 5px 0; font-size: 0.9em;">{review['location']} • {review['type']}</p>
                        </div>
                        <div class="star-rating">{stars}</div>
                    </div>
                    <p style="color: #fefae0; line-height: 1.6; font-size: 1.05em;">"{review['review']}"</p>
                    <div style="margin-top: 15px; padding-top: 15px; border-top: 1px solid rgba(233, 196, 106, 0.3);">
                        <p style="color: #e9c46a; font-size: 0.9em;">
                            👤 {review['reviewer']} • 📅 Visited {review['date']} • {review['recommend']}
                        </p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("🌟 Be the first to share a review!")
    
    with comm_tab2:
        st.markdown("""
            <div class="content-card">
                <h3 style="color: #2a9d8f; text-align: center;">💡 Share Your Insider Tips</h3>
                <p style="text-align: center; color: #264653;">Know a hidden gem? Share it with the community!</p>
            </div>
            """, unsafe_allow_html=True)
        
        with st.form("tips_form", clear_on_submit=True):
            tip_category = st.selectbox("🏷️ Category", [
                "Hidden Beach",
                "Local Restaurant",
                "Secret Viewpoint",
                "Cultural Tip",
                "Money-Saving Hack",
                "Transportation Advice",
                "Other"
            ])
            
            tip_title = st.text_input("📝 Tip Title", placeholder="e.g., 'Best sunset spot in Palermo'")
            
            tip_location = st.selectbox("📍 Related to", ["Sicily (General)"] + list(destinations.keys()))
            
            tip_content = st.text_area(
                "✍️ Share your tip",
                height=150,
                placeholder="Share the details, how to get there, what makes it special..."
            )
            
            submit_tip = st.form_submit_button("✨ Share Tip", use_container_width=True)
            
            if submit_tip and tip_title and tip_content:
                st.success("🙏 Grazie! Your tip will help many travelers!")
                st.balloons()
                st.info("Tip submitted for review. It will appear in the community section within 24-48 hours.")
    
    with comm_tab3:
        st.markdown("""
            <div class="content-card">
                <h3 style="color: #2a9d8f; text-align: center;">📮 Send Us Feedback</h3>
                <p style="text-align: center; color: #264653;">Help us improve this guide for everyone</p>
            </div>
            """, unsafe_allow_html=True)
        
        with st.form("feedback_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                feedback_name = st.text_input("👤 Your Name", value=st.session_state.user_name)
                feedback_email = st.text_input("📧 Email (optional)")
            
            with col2:
                visited = st.radio("🗺️ Have you been to Sicily?", [
                    "Planning my first trip",
                    "Currently traveling!",
                    "Been there before"
                ])
                helpfulness = st.slider("⭐ How helpful is this guide?", 1, 5, 5)
            
            feedback_category = st.multiselect("What would you like to tell us about?", [
                "Missing information",
                "Incorrect details",
                "Suggestion for improvement",
                "New feature request",
                "General praise 😊",
                "Other"
            ])
            
            feedback_text = st.text_area(
                "💭 Your feedback",
                height=150,
                placeholder="What can we improve? What's missing? What do you love?"
            )
            
            submit_feedback = st.form_submit_button("📤 Send Feedback", use_container_width=True)
            
            if submit_feedback and feedback_text:
                feedback_entry = {
                    'name': feedback_name,
                    'email': feedback_email,
                    'visited': visited,
                    'rating': helpfulness,
                    'category': feedback_category,
                    'feedback': feedback_text,
                    'timestamp': datetime.now()
                }
                st.session_state.feedback_data.append(feedback_entry)
                
                st.success(f"Grazie mille, {feedback_name}! 🙏")
                st.balloons()
                st.info("Your feedback helps make this guide better for everyone!")
        
        # Community stats
        st.markdown("<br><hr><br>", unsafe_allow_html=True)
        st.markdown("""
            <div style='text-align: center;'>
                <h3 style="color: #e9c46a;">📊 Community Impact</h3>
            </div>
            """, unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("👥 Active Users", "2,847")
        with col2:
            st.metric("⭐ Reviews", len(st.session_state.reviews))
        with col3:
            st.metric("💬 Feedback", len(st.session_state.feedback_data))
        with col4:
            st.metric("🌍 Countries", "23")

# ============================================
# TAB 4: PRACTICAL GUIDE
# ============================================
with tab4:
    st.markdown("""
        <div style='text-align: center; padding: 30px 0;'>
            <h2>📋 Essential Travel Information</h2>
            <p style='font-size: 1.2em; color: #e9c46a;'>Everything you need to know before you go</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Practical information sections
    prac_tab1, prac_tab2, prac_tab3 = st.tabs([
        "🚗 Getting Around",
        "💰 Money & Budget",
        "🗣️ Language & Culture"
    ])
    
    with prac_tab1:
        st.markdown("""
        <div class="content-card">
            <h3 style="color: #2a9d8f;">🚗 Transportation Guide</h3>
        </div>
        """, unsafe_allow_html=True)
        
        transport_options = {
            "🚗 Car Rental": {
                "pros": "Freedom to explore, reach remote beaches, wine regions",
                "cons": "City traffic, narrow streets, parking challenges",
                "cost": "€30-50/day",
                "tip": "Book automatic transmission in advance—manuals are standard"
            },
            "🚂 Trains": {
                "pros": "Scenic coastal routes, connects major cities",
                "cons": "Limited inland, slower on some routes",
                "cost": "€8-15 between cities",
                "tip": "Circumetnea train around Etna is a day trip itself"
            },
            "🚌 Buses": {
                "pros": "Reaches everywhere, affordable",
                "cons": "Schedules can be unreliable, crowded in summer",
                "cost": "€5-20 depending on distance",
                "tip": "Buy tickets at tobacco shops (tabacchi), not on board"
            },
            "🛵 Scooter": {
                "pros": "Perfect for towns and islands, park anywhere",
                "cons": "Hot in summer, limited range",
                "cost": "€20-35/day",
                "tip": "Always wear helmet—police are strict now"
            }
        }
        
        for transport, details in transport_options.items():
            with st.expander(transport):
                st.markdown(f"""
                <div class="content-card" style="padding: 20px;">
                    <p><strong>✅ Pros:</strong> {details['pros']}</p>
                    <p><strong>❌ Cons:</strong> {details['cons']}</p>
                    <p><strong>💰 Cost:</strong> {details['cost']}</p>
                    <div style="background: rgba(233, 196, 106, 0.15); padding: 15px; border-radius: 10px; margin-top: 10px;">
                        <p><strong>💡 Insider Tip:</strong> {details['tip']}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    with prac_tab2:
        st.markdown("""
        <div class="content-card">
            <h3 style="color: #2a9d8f;">💰 Money Matters</h3>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="info-card">
                <h4 style="color: #e9c46a;">💵 Daily Budget</h4>
                <p><strong>Budget:</strong> €50-70/day<br>
                <em>(Hostels, street food, public transport)</em></p>
                <p><strong>Mid-range:</strong> €100-150/day<br>
                <em>(B&Bs, trattorias, some car rental)</em></p>
                <p><strong>Luxury:</strong> €250+/day<br>
                <em>(Hotels, fine dining, private tours)</em></p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="info-card">
                <h4 style="color: #e9c46a;">💳 Tipping Guide</h4>
                <p><strong>Restaurants:</strong> Round up or €5-10<br>
                <em>(Service often included)</em></p>
                <p><strong>Bars:</strong> €1 for table service<br>
                <em>(Not expected for coffee)</em></p>
                <p><strong>Taxis:</strong> Round to nearest €5</p>
                <p><em>Note: Coperto (cover charge) €1-3 is normal</em></p>
            </div>
            """, unsafe_allow_html=True)
    
    with prac_tab3:
        st.markdown("""
        <div class="content-card">
            <h3 style="color: #2a9d8f;">🗣️ Language & Culture</h3>
            <p style="color: #264653;">English is spoken in tourist areas, but learning a few Italian phrases goes a long way!</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-card">
            <h4 style="color: #e9c46a;">🗨️ Essential Phrases</h4>
        </div>
        """, unsafe_allow_html=True)
        
        phrases = {
            "Buongiorno": "Good morning",
            "Per favore": "Please",
            "Grazie": "Thank you",
            "Scusi": "Excuse me",
            "Quanto costa?": "How much?",
            "Dov'è...?": "Where is...?",
            "Il conto, per favore": "The bill, please",
            "Che cosa consiglia?": "What do you recommend?",
            "Senza glutine": "Gluten-free",
            "Delizioso!": "Delicious!"
        }
        
        col1, col2 = st.columns(2)
        for i, (italian, english) in enumerate(phrases.items()):
            with (col1 if i % 2 == 0 else col2):
                st.markdown(f"**{italian}** → *{english}*")

# ============================================
# TAB 5: ASK & DISCOVER
# ============================================
with tab5:
    st.markdown("""
        <div style='text-align: center; padding: 30px 0;'>
            <h2>❓ Your Personal Concierge</h2>
            <p style='font-size: 1.2em; color: #e9c46a;'>Get personalized recommendations and answers</p>
        </div>
        """, unsafe_allow_html=True)
    
    question_type = st.selectbox(
        "What can we help you with?",
        [
            "🍴 Restaurant Recommendation",
            "🏨 Where to Stay",
            "🏖️ Beach Suggestion",
            "🗺️ Day Trip Ideas",
            "🚗 Transportation Help",
            "💭 General Question"
        ]
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if "Restaurant" in question_type:
        st.markdown("""
        <div class="content-card">
            <h3 style="color: #2a9d8f; text-align: center;">🍴 Find Your Perfect Restaurant</h3>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("restaurant_finder"):
            col1, col2 = st.columns(2)
            
            with col1:
                rest_location = st.selectbox("📍 Where are you?", 
                    ["Palermo", "Catania", "Syracuse", "Taormina", "Other"])
                cuisine = st.multiselect("🍽️ Cuisine Type", [
                    "Traditional Sicilian",
                    "Seafood",
                    "Pizza",
                    "Fine Dining",
                    "Vegetarian/Vegan"
                ])
            
            with col2:
                budget = st.select_slider("💰 Budget per person", [
                    "€10-20",
                    "€20-40",
                    "€40-70",
                    "€70+"
                ])
                occasion = st.radio("🎭 Occasion", [
                    "Casual meal",
                    "Romantic dinner",
                    "Family gathering"
                ])
            
            special = st.text_area("Any special requests?", placeholder="Allergies, celebrations, etc.")
            
            if st.form_submit_button("🔍 Find Restaurants", use_container_width=True):
                st.success("✨ Perfect matches found!")
                st.markdown(f"""
                <div class="content-card">
                    <h3 style="color: #e76f51;">Top Picks in {rest_location}</h3>
                    <br>
                    <div style="background: rgba(42, 157, 143, 0.1); padding: 20px; border-radius: 15px; margin: 15px 0;">
                        <h4 style="color: #2a9d8f;">🌟 Trattoria del Mare</h4>
                        <p>Perfect for: {occasion}</p>
                        <p>Budget: {budget}</p>
                        <p><em>"Authentic Sicilian seafood, family-run for 3 generations"</em></p>
                    </div>
                    <div style="background: rgba(233, 196, 106, 0.1); padding: 20px; border-radius: 15px; margin: 15px 0;">
                        <h4 style="color: #e9c46a;">💎 Osteria Antica</h4>
                        <p>Specialty: Traditional dishes</p>
                        <p><em>"Hidden gem in the old town, incredible wine selection"</em></p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    elif "Beach" in question_type:
        st.markdown("""
        <div class="content-card">
            <h3 style="color: #2a9d8f; text-align: center;">🏖️ Discover Your Perfect Beach</h3>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("beach_finder"):
            col1, col2 = st.columns(2)
            
            with col1:
                beach_area = st.selectbox("📍 Preferred area", [
                    "Any - show me the best",
                    "Near Palermo",
                    "Near Catania",
                    "Near Syracuse",
                    "Islands"
                ])
                beach_features = st.multiselect("What you're looking for", [
                    "White sand",
                    "Snorkeling",
                    "Family-friendly",
                    "Secluded",
                    "Beach clubs"
                ])
            
            with col2:
                access = st.radio("Accessibility", [
                    "Easy access",
                    "Short walk OK",
                    "Hidden gems (hiking)"
                ])
            
            if st.form_submit_button("🌊 Find My Beach", use_container_width=True):
                st.success("🏖️ Found your perfect match!")
                st.info("Cala Rossa in Favignana matches your preferences perfectly!")
    
    else:
        st.markdown("""
        <div class="content-card">
            <h3 style="color: #2a9d8f; text-align: center;">💭 Ask Us Anything</h3>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("general_question"):
            your_question = st.text_area(
                "What would you like to know?",
                height=150,
                placeholder="e.g., Is Sicily safe for solo travelers? Best time for wine harvest? Can I drink tap water?"
            )
            
            contact_email = st.text_input("📧 Your email (for response)")
            
            urgency = st.radio("⏱️ How urgent?", [
                "Just curious",
                "Planning soon",
                "Already in Sicily!"
            ])
            
            if st.form_submit_button("📤 Submit Question", use_container_width=True):
                if your_question and contact_email:
                    st.success("✅ Question received!")
                    st.info(f"""
                    We'll respond to **{contact_email}** within:
                    - 🚨 Already there: 2-4 hours
                    - 📅 Planning soon: 24 hours
                    - 💭 Just curious: 48 hours
                    """)

# ============================================
# TAB 6: MY DASHBOARD
# ============================================
with tab6:
    st.markdown(f"""
        <div style='text-align: center; padding: 30px 0;'>
            <h2>📊 Welcome Back, {st.session_state.user_name}!</h2>
            <p style='font-size: 1.2em; color: #e9c46a;'>Your personal Sicily travel hub</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Stats Overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📌 Bookmarks", len(st.session_state.bookmarks))
    with col2:
        st.metric("🗺️ Saved Trips", len(st.session_state.saved_trips))
    with col3:
        st.metric("⭐ Reviews Written", len(st.session_state.reviews))
    with col4:
        st.metric("💬 Feedback Given", len(st.session_state.feedback_data))
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Bookmarks Section
    st.markdown("""
        <div style='text-align: center; padding: 20px 0;'>
            <h3 style="color: #e9c46a;">📌 Your Bookmarks</h3>
        </div>
        """, unsafe_allow_html=True)
    
    if st.session_state.bookmarks:
        # Create columns for better layout
        for i, bookmark in enumerate(st.session_state.bookmarks):
            col1, col2 = st.columns([5, 1])
            
            with col1:
                st.markdown(f"""
                <div class="bookmark-item">
                    <p style="margin: 0; font-size: 1.05em;">✓ {bookmark}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                if st.button("🗑️", key=f"remove_bookmark_{i}"):
                    st.session_state.bookmarks.pop(i)
                    st.rerun()
        
        # Export bookmarks
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            bookmarks_text = "\n".join([f"• {b}" for b in st.session_state.bookmarks])
            st.download_button(
                "📥 Export Bookmarks",
                bookmarks_text,
                file_name="sicily_bookmarks.txt",
                use_container_width=True
            )
    else:
        st.markdown("""
        <div class="info-card">
            <p style='text-align: center; font-size: 1.1em;'>
                No bookmarks yet! 🌟<br>
                <em>Explore the regions and save your favorite places</em>
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Saved Trips Section
    st.markdown("""
        <div style='text-align: center; padding: 20px 0;'>
            <h3 style="color: #e9c46a;">🗺️ Your Saved Itineraries</h3>
        </div>
        """, unsafe_allow_html=True)
    
    if st.session_state.saved_trips:
        for i, trip in enumerate(st.session_state.saved_trips):
            with st.expander(f"✈️ {trip['name']}", expanded=False):
                st.markdown(f"""
                <div class="content-card">
                    <h3 style="color: #2a9d8f;">{trip['name']}</h3>
                    <p><strong>📅 Duration:</strong> {trip['duration']} days</p>
                    <p><strong>🎨 Style:</strong> {trip['style']}</p>
                    <p><strong>🛬 Starting from:</strong> {trip['start']}</p>
                    <p><strong>🎯 Interests:</strong> {', '.join(trip.get('interests', [])) if trip.get('interests') else 'Not specified'}</p>
                    <p><strong>📅 Created:</strong> {trip['date_created']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("📧 Email Details", key=f"email_{i}"):
                        st.success("📧 Itinerary sent to your email!")
                with col2:
                    if st.button("📄 View Full Plan", key=f"view_{i}"):
                        st.info("Full itinerary displayed above!")
                with col3:
                    if st.button("🗑️ Delete", key=f"delete_{i}"):
                        st.session_state.saved_trips.pop(i)
                        st.success("Trip deleted")
                        st.rerun()
    else:
        st.markdown("""
        <div class="info-card">
            <p style='text-align: center; font-size: 1.1em;'>
                No saved trips yet! ✈️<br>
                <em>Use the Trip Builder to create your perfect itinerary</em>
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Reviews Section
    st.markdown("""
        <div style='text-align: center; padding: 20px 0;'>
            <h3 style="color: #e9c46a;">⭐ Your Reviews</h3>
        </div>
        """, unsafe_allow_html=True)
    
    if st.session_state.reviews:
        for review in st.session_state.reviews:
            stars = "⭐" * review['rating']
            st.markdown(f"""
            <div class="review-card">
                <h4 style="color: #e9c46a;">{review['place']} {stars}</h4>
                <p style="color: #fefae0;"><em>"{review['review']}"</em></p>
                <p style="color: #e9c46a; font-size: 0.9em;">Posted on {review['date']}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="info-card">
            <p style='text-align: center; font-size: 1.1em;'>
                No reviews yet! 🌟<br>
                <em>Share your experiences in the Community tab</em>
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Account Actions
    st.markdown("""
        <div style='text-align: center; padding: 20px 0;'>
            <h3 style="color: #e9c46a;">⚙️ Account Actions</h3>
        </div>
        """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📥 Export All Data", use_container_width=True):
            all_data = {
                'bookmarks': st.session_state.bookmarks,
                'trips': st.session_state.saved_trips,
                'reviews': [r for r in st.session_state.reviews],
                'export_date': datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            st.download_button(
                "Download JSON",
                json.dumps(all_data, indent=2, default=str),
                file_name=f"sicily_data_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json"
            )
    
    with col2:
        if st.button("🔄 Refresh Dashboard", use_container_width=True):
            st.rerun()
    
    with col3:
        if st.button("🗑️ Clear All Data", use_container_width=True, type="secondary"):
            if st.checkbox("⚠️ Are you sure? This cannot be undone"):
                st.session_state.bookmarks = []
                st.session_state.saved_trips = []
                st.session_state.reviews = []
                st.session_state.feedback_data = []
                st.success("All data cleared!")
                st.rerun()

# --- INTERACTIVE MAP ---
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("""
    <div style='text-align: center; padding: 30px 0;'>
        <h2>🗺️ Interactive Sicily Map</h2>
        <p style='font-size: 1.2em; color: #e9c46a;'>Explore all regions at a glance</p>
    </div>
    """, unsafe_allow_html=True)

map_data = pd.DataFrame([
    {
        "lat": d["lat"], 
        "lon": d["lon"], 
        "name": k,
        "size": 200
    } 
    for k, d in destinations.items()
])

st.map(map_data, size='size')

st.markdown("""
<div class="info-card">
    <p style='text-align: center;'>
        🔵 <strong>Blue markers</strong> represent major regions covered in this guide<br>
        Click markers for more details • Best viewed on desktop
    </p>
</div>
""", unsafe_allow_html=True)

# --- ELEGANT FOOTER ---
st.markdown("<hr>", unsafe_allow_html=True)

st.markdown("""
    <div style='text-align: center; padding: 40px 20px;'>
        <div class='decorative-icon'>🏺</div>
        <h2 style='color: #e9c46a; margin: 20px 0;'>Sicilia Autentica</h2>
        <p style='font-size: 1.1em; color: #fefae0; margin: 15px 0;'>
            Made with ❤️ and passion for Sicily<br>
            <em>Benvenuti in Sicilia — Where every stone tells a story</em>
        </p>
        <br>
        <p style='color: #e9c46a; font-size: 0.9em;'>
            Last Updated: January 2026 • Version 2.0 • Premium Edition
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div style='text-align: center; padding: 20px;'>
    <p style='color: rgba(254, 250, 224, 0.6); font-size: 0.85em;'>
        © 2026 Sicilia Autentica • For private use within our network<br>
        Contact: info@siciliaautentica.com
    </p>
</div>
""", unsafe_allow_html=True)
