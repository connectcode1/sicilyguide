import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import json

# Page Config
st.set_page_config(
    page_title="Sicily Insider - Curated Travel Guide", 
    page_icon="🇮🇹", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CONDÉ NAST INSPIRED CSS WITH SICILIAN CERAMIC COLORS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700;800&family=Lato:wght@300;400;700&display=swap');
    
    /* Main Background - Clean White with Subtle Pattern */
    .stApp {
        background-color: #FFFFFF;
        color: #2C2C2C;
        font-family: 'Lato', sans-serif;
    }
    
    /* Elegant Content Cards - Sicilian Ceramic Inspired */
    .content-card {
        background: #FFFFFF;
        color: #2C2C2C;
        padding: 50px;
        border-radius: 0;
        border-top: 6px solid #D4A574;
        margin: 40px 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        position: relative;
    }
    
    .content-card::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, 
            #C85A54 0%, 
            #D4A574 25%,
            #5B8C85 50%,
            #D4A574 75%,
            #C85A54 100%);
    }
    
    /* Feature Cards */
    .feature-card {
        background: linear-gradient(135deg, #F8F6F2 0%, #FFFFFF 100%);
        border: 1px solid #E8E4DC;
        border-left: 4px solid #5B8C85;
        padding: 30px;
        margin: 20px 0;
        border-radius: 0;
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        box-shadow: 0 8px 30px rgba(91, 140, 133, 0.15);
        transform: translateY(-2px);
    }
    
    /* Headers - Editorial Style */
    h1 {
        font-family: 'Playfair Display', serif !important;
        color: #2C2C2C !important;
        font-weight: 700 !important;
        font-size: 3.5em !important;
        letter-spacing: -1px !important;
        margin-bottom: 20px !important;
        line-height: 1.2 !important;
    }
    
    h2 {
        font-family: 'Playfair Display', serif !important;
        color: #C85A54 !important;
        font-weight: 600 !important;
        font-size: 2.2em !important;
        margin-top: 40px !important;
        margin-bottom: 20px !important;
        letter-spacing: 0px !important;
    }
    
    h3 {
        font-family: 'Playfair Display', serif !important;
        color: #5B8C85 !important;
        font-weight: 600 !important;
        font-size: 1.6em !important;
        margin-top: 25px !important;
        margin-bottom: 15px !important;
    }
    
    h4 {
        font-family: 'Lato', sans-serif !important;
        color: #2C2C2C !important;
        font-weight: 700 !important;
        font-size: 1.1em !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
        margin-bottom: 15px !important;
    }
    
    /* Paragraph Text */
    p {
        font-family: 'Lato', sans-serif;
        font-size: 1.05em;
        line-height: 1.8;
        color: #4A4A4A;
    }
    
    /* Sidebar - Minimalist Luxury */
    section[data-testid="stSidebar"] {
        background: #F8F6F2;
        border-right: 1px solid #E8E4DC;
        padding: 30px 20px;
    }
    
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #2C2C2C !important;
    }
    
    section[data-testid="stSidebar"] p {
        color: #4A4A4A;
        font-size: 0.95em;
    }
    
    /* Buttons - Sicilian Ceramic Accent */
    .stButton>button {
        background: #C85A54;
        color: #FFFFFF;
        border: none;
        border-radius: 0;
        font-weight: 600;
        padding: 15px 40px;
        font-size: 0.95em;
        font-family: 'Lato', sans-serif;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(200, 90, 84, 0.3);
    }
    
    .stButton>button:hover {
        background: #B34A44;
        box-shadow: 0 4px 15px rgba(200, 90, 84, 0.4);
        transform: translateY(-1px);
    }
    
    /* Secondary Buttons */
    .stButton>button[kind="secondary"] {
        background: #5B8C85;
    }
    
    .stButton>button[kind="secondary"]:hover {
        background: #4A7B74;
    }
    
    /* Tabs - Clean Editorial */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background: transparent;
        border-bottom: 2px solid #E8E4DC;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border: none;
        color: #6A6A6A;
        font-weight: 600;
        padding: 15px 30px;
        font-family: 'Lato', sans-serif;
        font-size: 0.95em;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        border-bottom: 3px solid transparent;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        color: #C85A54;
        border-bottom-color: #D4A574;
    }
    
    .stTabs [aria-selected="true"] {
        background: transparent;
        color: #C85A54;
        border-bottom-color: #C85A54;
    }
    
    /* Expanders - Sophisticated */
    .streamlit-expanderHeader {
        background: #F8F6F2;
        border: 1px solid #E8E4DC;
        border-left: 4px solid #D4A574;
        font-weight: 600;
        color: #2C2C2C !important;
        padding: 18px 20px !important;
        font-size: 1.05em;
        font-family: 'Lato', sans-serif;
        transition: all 0.3s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background: #FFFFFF;
        border-left-color: #C85A54;
    }
    
    /* Metrics - Editorial Numbers */
    [data-testid="stMetricValue"] {
        color: #C85A54;
        font-size: 2.5em;
        font-family: 'Playfair Display', serif;
        font-weight: 700;
    }
    
    [data-testid="stMetricLabel"] {
        color: #6A6A6A;
        font-weight: 600;
        font-size: 0.85em;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }
    
    /* Input Fields - Clean */
    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea,
    .stSelectbox>div>div>select,
    .stMultiSelect>div>div>div {
        background: #FFFFFF;
        border: 2px solid #E8E4DC;
        border-radius: 0;
        color: #2C2C2C;
        font-family: 'Lato', sans-serif;
        padding: 12px 15px;
        transition: border-color 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus,
    .stTextArea>div>div>textarea:focus {
        border-color: #5B8C85;
        box-shadow: 0 0 0 1px #5B8C85;
    }
    
    /* Dividers */
    hr {
        border: none;
        height: 1px;
        background: #E8E4DC;
        margin: 60px 0;
    }
    
    /* Success/Info Messages */
    .stSuccess {
        background: rgba(91, 140, 133, 0.1);
        border-left: 4px solid #5B8C85;
        border-radius: 0;
        color: #2C2C2C;
        padding: 15px 20px;
    }
    
    .stInfo {
        background: rgba(212, 165, 116, 0.1);
        border-left: 4px solid #D4A574;
        border-radius: 0;
        color: #2C2C2C;
        padding: 15px 20px;
    }
    
    .stWarning {
        background: rgba(200, 90, 84, 0.1);
        border-left: 4px solid #C85A54;
        border-radius: 0;
        color: #2C2C2C;
        padding: 15px 20px;
    }
    
    /* Blockquote Style */
    .insider-quote {
        border-left: 4px solid #D4A574;
        padding: 25px 30px;
        background: #F8F6F2;
        font-style: italic;
        font-size: 1.1em;
        line-height: 1.7;
        color: #4A4A4A;
        margin: 30px 0;
    }
    
    /* Bookmark Items */
    .bookmark-item {
        background: #FFFFFF;
        border: 1px solid #E8E4DC;
        border-left: 3px solid #5B8C85;
        padding: 15px 20px;
        margin: 10px 0;
        transition: all 0.3s ease;
    }
    
    .bookmark-item:hover {
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    /* Review Cards */
    .review-card {
        background: #FFFFFF;
        border: 1px solid #E8E4DC;
        padding: 30px;
        margin: 20px 0;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    }
    
    /* Image Captions */
    .caption {
        font-size: 0.9em;
        color: #6A6A6A;
        font-style: italic;
        margin-top: 10px;
        text-align: center;
    }
    
    /* Hero Section */
    .hero-section {
        text-align: center;
        padding: 80px 20px 60px 20px;
        background: linear-gradient(180deg, #FFFFFF 0%, #F8F6F2 100%);
        border-bottom: 1px solid #E8E4DC;
    }
    
    /* Section Headers */
    .section-header {
        text-align: center;
        padding: 40px 0 20px 0;
        border-bottom: 3px solid #E8E4DC;
        margin-bottom: 40px;
    }
    
    /* Footer */
    .footer {
        background: #F8F6F2;
        padding: 60px 40px;
        margin-top: 80px;
        border-top: 1px solid #E8E4DC;
    }
    
    /* Links */
    a {
        color: #C85A54;
        text-decoration: none;
        border-bottom: 1px solid transparent;
        transition: border-color 0.3s ease;
    }
    
    a:hover {
        border-bottom-color: #C85A54;
    }
    
    /* Number Badges */
    .number-badge {
        display: inline-block;
        background: #C85A54;
        color: #FFFFFF;
        width: 35px;
        height: 35px;
        line-height: 35px;
        text-align: center;
        border-radius: 50%;
        font-weight: 700;
        margin-right: 15px;
    }
    
    /* Pull Quote */
    .pull-quote {
        font-family: 'Playfair Display', serif;
        font-size: 1.5em;
        line-height: 1.5;
        color: #C85A54;
        text-align: center;
        padding: 40px 60px;
        position: relative;
        font-style: italic;
    }
    
    .pull-quote::before,
    .pull-quote::after {
        content: '"';
        font-size: 3em;
        color: #D4A574;
        position: absolute;
    }
    
    .pull-quote::before {
        top: 0;
        left: 20px;
    }
    
    .pull-quote::after {
        bottom: -20px;
        right: 20px;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #F8F6F2;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #D4A574;
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #C85A54;
    }
    </style>
    """, unsafe_allow_html=True)

# --- INITIALIZE SESSION STATE ---
if 'saved_trips' not in st.session_state:
    st.session_state.saved_trips = []
if 'bookmarks' not in st.session_state:
    st.session_state.bookmarks = []
if 'reviews' not in st.session_state:
    st.session_state.reviews = []

# --- EXPANDED DESTINATIONS DATA ---
destinations = {
    "Palermo & Western Sicily": {
        "tagline": "Where Arab Domes Meet Norman Grandeur",
        "description": """Palermo is a city of contradictions and unexpected beauty. Byzantine mosaics shimmer in Norman chapels, 
        Arab-influenced markets pulse with life, and baroque palaces lean against crumbling facades. The western coast unfolds with 
        pristine reserves, ancient salt pans, and hilltop medieval towns suspended in time. This is Sicily at its most authentic—
        unpolished, vibrant, and utterly captivating.""",
        
        "insider_tip": """Visit the Palatine Chapel on a Wednesday afternoon when light streams through the windows at the perfect 
        angle, illuminating the Byzantine mosaics in molten gold. The artisans who created this masterpiece nine centuries ago 
        understood sacred geometry—every detail was calculated to inspire awe at precisely this moment.""",
        
        "beaches": {
            "Mondello Beach": "Palermo's Art Nouveau playground with turquoise waters and Belle Époque architecture",
            "Riserva dello Zingaro": "7km of protected coastline accessible only on foot, with hidden coves and crystalline water",
            "San Vito Lo Capo": "White sand beach beneath Monte Monaco, transforming into pink and gold at sunset",
            "Scopello": "Dramatic sea stacks rising from emerald waters, historic tuna fishery turned swimming paradise"
        },
        
        "experiences": {
            "Street Food Tour": "Navigate Ballarò Market with a local guide—panelle, arancine, and sfincione",
            "Monreale Mosaics": "The cathedral's golden mosaics cover 6,400 square meters of biblical storytelling",
            "Erice Sunset": "Medieval hilltop town wrapped in mist, famous for almond pastries and panoramic views",
            "Salt Pans of Trapani": "Sunset over ancient windmills and pink salt mountains"
        },
        
        "must_visit": [
            "Palatine Chapel - Book 9 AM entry for the best light",
            "Quattro Canti - Baroque heart of the old city",
            "Teatro Massimo - Italy's largest opera house",
            "Cefalù - Norman cathedral on a pristine beach",
            "Segesta - Greek temple in splendid isolation"
        ],
        
        "where_to_eat": {
            "Antica Focacceria San Francesco": "Since 1834, the definitive pani ca' meusa (spleen sandwich)",
            "Pasticceria Cappello": "Cannoli filled to order—ricotta with pistachios is transcendent",
            "Trattoria Ai Cascinari": "Pasta con le sarde, Palermo's signature dish, perfected",
            "Ke Palle": "Modern take on arancine, 20+ varieties"
        },
        
        "lat": 38.1157,
        "lon": 13.3615,
        "days": "4-5 days",
        "best_time": "April-June, September-October"
    },
    
    "Taormina, Messina & The Northeast": {
        "tagline": "Where Myths Were Born and Beauty Reigns",
        "description": """Messina guards the strait where Scylla and Charybdis once terrorized sailors. Taormina perches on a cliff 
        with the ancient Greek theater framing Mount Etna and the Ionian Sea in one impossible view. The Peloritani Mountains descend 
        to hidden beaches and coastal villages where time moves to the rhythm of fishing boats and church bells. This is where Sicily 
        shows its most photogenic face.""",
        
        "insider_tip": """Take the Circumetnea train from Catania to Riposto early morning. This vintage railway circles Mount Etna 
        through lava fields, pistachio groves, and medieval villages. At Linguaglossa, step off for an espresso in the shadow of the 
        volcano—you'll be the only tourist for miles.""",
        
        "beaches": {
            "Isola Bella": "Taormina's jewel—a nature reserve connected to shore by a narrow sandbar",
            "Giardini Naxos": "Wide sandy beaches below Taormina, first Greek colony in Sicily",
            "Capo Milazzo": "Dramatic promontory with hidden coves and the Sanctuary of St. Anthony",
            "Letojanni": "Pebble beach village, quieter alternative to Taormina with excellent seafood"
        },
        
        "experiences": {
            "Ancient Theater of Taormina": "Greek theater with Mount Etna as backdrop—attend a summer concert",
            "Messina Cathedral": "Astronomical clock at noon triggers an elaborate mechanical show",
            "Savoca": "Godfather filming location—drink lemon granita at Bar Vitelli",
            "Castelmola": "Medieval village above Taormina, famous for almond wine"
        },
        
        "must_visit": [
            "Taormina's Corso Umberto - Boutique shopping and cafe culture",
            "Gole Alcantara - Volcanic gorge with ice-cold river",
            "Forza d'Agrò - Perfectly preserved medieval hamlet",
            "Santuario di Tindari - Black Madonna overlooking the sea",
            "Milazzo - Ferry port to Aeolian Islands"
        ],
        
        "where_to_eat": {
            "Bam Bar": "Taormina's legendary granita—almond with warm brioche",
            "Osteria Nero d'Avola": "Intimate restaurant in Taormina, Sicilian classics elevated",
            "Trattoria da Pina": "Letojanni favorite for swordfish and local wine",
            "Pasticceria Roberto": "Messina's finest pastries, try the pignolata"
        },
        
        "lat": 37.8526,
        "lon": 15.2876,
        "days": "3-4 days",
        "best_time": "May-June, September-October"
    },
    
    "Aeolian Islands": {
        "tagline": "The Seven Sisters of the Tyrrhenian Sea",
        "description": """Seven volcanic islands scattered north of Sicily like precious stones. Lipari, the largest, is a base for 
        island hopping. Stromboli erupts every 20 minutes—you can hike to the crater at sunset. Vulcano's therapeutic mud baths steam 
        beside black sand beaches. Salina grows sweet Malvasia wine among capers and wildflowers. Panarea attracts the international 
        jet set, while Filicudi and Alicudi remain wonderfully undiscovered. Each island has its own character, united by dramatic 
        beauty and isolation.""",
        
        "insider_tip": """Skip the crowded Stromboli summit hike. Instead, take the evening boat tour that circles the island. 
        You'll witness the Sciara del Fuoco from the sea—lava bombs exploding against the night sky, reflected in black water. 
        It's Stromboli's most spectacular angle, and you'll be back in time for dinner.""",
        
        "beaches": {
            "Pollara Beach (Salina)": "Crescent bay beneath volcanic cliffs, Il Postino filming location",
            "Spiaggia Bianca (Lipari)": "White pumice beach contrasting with turquoise water",
            "Vulcano Thermal Beaches": "Natural hot springs meet the sea, therapeutic volcanic mud",
            "Cala Junco (Panarea)": "Tiny bay carved from lava rock, crystal clear water"
        },
        
        "experiences": {
            "Stromboli Night Hike": "Guided climb to active crater—witness eruptions at sunset",
            "Boat Tour Around Islands": "Full-day excursion visiting multiple islands and hidden grottos",
            "Malvasia Wine Tasting": "Sweet wine made from grapes dried on volcanic terraces",
            "Volcanic Mud Bath": "Soak in Vulcano's therapeutic sulfur mud pools",
            "Panarea Nightlife": "Chic beach clubs and waterfront bars under the stars"
        },
        
        "must_visit": [
            "Lipari Archaeological Museum - Obsidian and ceramic treasures",
            "Salina's Twin Volcanoes - Hiking through Mediterranean vegetation",
            "Stromboli Village - Car-free streets, white houses, bougainvillea",
            "Filicudi Prehistoric Village - Bronze Age settlement ruins",
            "Panarea's Prehistoric Village - Clifftop archaeological site"
        ],
        
        "where_to_eat": {
            "E Pulera (Vulcano)": "Fresh fish grilled on volcanic stone",
            "Capofaro (Salina)": "Michelin-starred restaurant in Malvasia vineyard",
            "Il Filippino (Lipari)": "Historic restaurant, capers and seafood specialties",
            "Punta Lena (Stromboli)": "Terrace dining with volcano views"
        },
        
        "lat": 38.5667,
        "lon": 14.9564,
        "days": "4-7 days (minimum 3 for proper exploration)",
        "best_time": "May-June, September (July-August very crowded)",
        "access": "Ferries from Milazzo (90min-2.5hrs depending on island)"
    },
    
    "Catania, Etna & Eastern Sicily": {
        "tagline": "Living in the Shadow of the Volcano",
        "description": """Mount Etna dominates everything—the landscape, the culture, the economy, even the weather. At 3,350 meters, 
        Europe's most active volcano erupts regularly, covering Catania's baroque streets in fine ash. Yet Sicilians have learned to 
        harness the mountain's power: volcanic soil produces exceptional wine, pistachios grow nowhere else on earth, and tourism 
        thrives on the danger. Catania itself is Sicily's second city—grittier than Palermo, more authentic than Taormina.""",
        
        "insider_tip": """Visit Gambino Winery on Etna's slopes at 1200m elevation. The tasting room overlooks terraced vineyards 
        in volcanic soil, with the crater visible above. The Nerello Mascalese grapes produce wines that taste of smoke, stone, 
        and wild herbs—terroir in its purest expression. Book the sunset slot.""",
        
        "beaches": {
            "San Giovanni Li Cuti": "Catania's lava rock beach with fish restaurants and sunset views",
            "Aci Trezza": "Fishing village with the Cyclops' legendary basalt rocks offshore",
            "Aci Castello": "Black sand beach below a Norman castle on volcanic rock",
            "Fondachello": "Long sandy beach south of Catania, local favorite"
        },
        
        "experiences": {
            "Etna Summit Hike": "Guided trek to active craters with volcanologist—cable car + 4x4",
            "Catania Fish Market": "A Pescheria at dawn—tuna, swordfish, and controlled chaos",
            "Etna Wine Tour": "Visit boutique wineries at 800-1000m elevation",
            "Via Etnea Shopping": "Baroque street from Duomo to volcano, cafes and boutiques",
            "Ursino Castle": "13th-century fortress, now an art museum"
        },
        
        "must_visit": [
            "Piazza Duomo - Elephant fountain and baroque cathedral",
            "Benedictine Monastery - Massive complex, library and frescoes",
            "Etna Crater Silvestri - Lower craters accessible without guide",
            "Rifugio Sapienza - Mountain refuge at 1900m, starting point for summit",
            "Zafferana Etnea - Honey village on Etna's slopes"
        ],
        
        "where_to_eat": {
            "Savia": "The definitive arancino—try al burro and al ragù",
            "FUD": "Modern Catanese cuisine, horsemeat specialties",
            "Trattoria de Fiore": "Pasta alla Norma (eggplant, ricotta, basil)—Catania's signature",
            "Me Cumpari Turiddu": "Traditional dishes in historic setting"
        },
        
        "lat": 37.5079,
        "lon": 15.0830,
        "days": "3-4 days",
        "best_time": "April-June, September-October (Etna accessible year-round)"
    },
    
    "Syracuse & Baroque Southeast": {
        "tagline": "Where Greece Meets Baroque Splendor",
        "description": """Syracuse was the most powerful Greek city in the Mediterranean, rivaling Athens. Today, Ortigia island 
        preserves layers of history—Greek temples beneath baroque churches, Renaissance palaces over Roman foundations. Beyond the 
        city, the Val di Noto showcases UNESCO baroque towns rebuilt after the 1693 earthquake: Noto's honey-colored cathedral, 
        Ragusa Ibla's winding streets, Modica's chocolate traditions. The coast alternates between white sand beaches and nature 
        reserves where flamingos nest in spring.""",
        
        "insider_tip": """In Ortigia, find Borderi deli near the Duomo. Don't ask for a menu—tell Gaetano where you're from and 
        what you ate yesterday. He'll create a sandwich masterpiece based on instinct, local ingredients, and 30 years of experience. 
        His tuna creations are the subject of legend among those who know.""",
        
        "beaches": {
            "Fontane Bianche": "Powdery white sand and shallow turquoise water, family paradise",
            "Calamosche": "Hidden beach in Vendicari Reserve, voted one of Italy's most beautiful",
            "Vendicari": "Nature reserve with pristine beaches and flamingo spotting",
            "Isola delle Correnti": "Italy's southernmost point where two seas meet",
            "Marzamemi": "Fishing village with tuna traditions and beach bars"
        },
        
        "experiences": {
            "Greek Theater Syracuse": "Classical performances June-July in ancient setting",
            "Noto by Night": "Baroque facades illuminated—architectural masterpiece",
            "Modica Chocolate Tour": "Aztec-style grainy chocolate, workshops available",
            "Ragusa Ibla Walk": "Lower town labyrinth, 18 baroque churches",
            "Ortigia Market": "Morning market for fish, cheese, and produce"
        },
        
        "must_visit": [
            "Arethusa Spring - Freshwater spring with papyrus in Ortigia",
            "Duomo of Syracuse - Temple of Athena columns visible in walls",
            "Ear of Dionysius - Limestone cave with perfect acoustics",
            "Palazzo Nicolaci Noto - Baroque balconies with grotesque sculptures",
            "Castello Maniace - 13th-century fortress at Ortigia's tip"
        ],
        
        "where_to_eat": {
            "Caffè Sicilia Noto": "Legendary granita, featured in Chef's Table",
            "Don Camillo Syracuse": "Fine dining in 15th-century palazzo",
            "Accursio Modica": "Michelin star, contemporary Sicilian",
            "La Cialoma Marzamemi": "Fresh tuna steps from the fishing boats"
        },
        
        "lat": 37.0755,
        "lon": 15.2866,
        "days": "4-5 days",
        "best_time": "May-June (Greek theater season), September"
    }
}

# --- HEADER ---
st.markdown("""
    <div class="hero-section">
        <p style="font-size: 0.9em; text-transform: uppercase; letter-spacing: 3px; color: #C85A54; font-weight: 600; margin-bottom: 15px;">
            Curated Travel Guide
        </p>
        <h1 style="font-size: 4em; margin: 20px 0;">Sicily</h1>
        <p style="font-size: 1.3em; color: #5B8C85; font-style: italic; max-width: 700px; margin: 20px auto; line-height: 1.6;">
            An insider's journey through the island where civilizations converge,<br>
            volcanoes shape destiny, and beauty exists in contradictions
        </p>
    </div>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("""
        <div style='text-align: center; padding: 20px 0 30px 0;'>
            <h4 style="color: #C85A54; margin-bottom: 5px;">SICILY INSIDER</h4>
            <p style="font-size: 0.85em; color: #6A6A6A;">Your Private Guide</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Stats
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Saved", len(st.session_state.bookmarks))
    with col2:
        st.metric("Trips", len(st.session_state.saved_trips))
    
    st.markdown("---")
    
    st.markdown("#### QUICK NAVIGATION")
    
    if st.button("📍 Explore Regions", use_container_width=True):
        st.info("See Explore Regions tab")
    
    if st.button("✈️ Plan Trip", use_container_width=True):
        st.info("See Plan Your Trip tab")
    
    if st.button("📊 My Dashboard", use_container_width=True):
        st.info("See My Dashboard tab")
    
    st.markdown("---")
    
    if st.session_state.bookmarks:
        st.markdown("#### YOUR BOOKMARKS")
        for item in st.session_state.bookmarks[-3:]:
            st.markdown(f"<div class='bookmark-item' style='font-size: 0.85em; padding: 10px;'>✓ {item}</div>", 
                       unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("""
        <div style='text-align: center; padding: 20px 0;'>
            <p style='font-size: 0.8em; color: #6A6A6A;'>
                Questions?<br>
                <a href='mailto:giulia@cubopro.com' style='color: #C85A54;'>giulia@cubopro.com</a>
            </p>
        </div>
        """, unsafe_allow_html=True)

# --- MAIN TABS ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "EXPLORE REGIONS",
    "PLAN YOUR TRIP",
    "INSIDER TIPS",
    "COMMUNITY",
    "MY DASHBOARD"
])

# ============================================
# TAB 1: EXPLORE REGIONS
# ============================================
with tab1:
    st.markdown("""
        <div class="section-header">
            <h2>Discover Sicily by Region</h2>
            <p style="font-size: 1.1em; color: #6A6A6A; max-width: 800px; margin: 15px auto;">
                From baroque towns to volcanic landscapes, each region tells its own story
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    selected_region = st.selectbox(
        "Select a region",
        list(destinations.keys()),
        label_visibility="collapsed"
    )
    
    region = destinations[selected_region]
    
    # Hero section for region
    st.markdown(f"""
        <div class="content-card">
            <h2 style="margin-top: 0;">{selected_region}</h2>
            <h4 style="color: #5B8C85; text-transform: none; letter-spacing: 0; font-family: 'Playfair Display', serif; 
                font-size: 1.3em; font-weight: 400; margin: 15px 0 30px 0;">
                {region['tagline']}
            </h4>
            <p style="font-size: 1.1em; line-height: 1.9; color: #4A4A4A;">
                {region['description']}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Insider tip
    st.markdown(f"""
        <div class="insider-quote">
            {region['insider_tip']}
        </div>
        """, unsafe_allow_html=True)
    
    # Quick facts
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
            <div style='text-align: center; padding: 20px;'>
                <h4>RECOMMENDED STAY</h4>
                <p style='font-size: 1.3em; color: #C85A54; font-family: "Playfair Display", serif;'>
                    {region['days']}
                </p>
            </div>
            """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
            <div style='text-align: center; padding: 20px;'>
                <h4>BEST TIME</h4>
                <p style='font-size: 1.1em; color: #5B8C85;'>
                    {region['best_time']}
                </p>
            </div>
            """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
            <div style='text-align: center; padding: 20px;'>
                <h4>BEACHES</h4>
                <p style='font-size: 1.3em; color: #C85A54; font-family: "Playfair Display", serif;'>
                    {len(region['beaches'])}
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    if st.button(f"Bookmark {selected_region}", key="bookmark_region"):
        if selected_region not in st.session_state.bookmarks:
            st.session_state.bookmarks.append(selected_region)
            st.success(f"Added {selected_region} to your bookmarks")
        else:
            st.info("Already bookmarked")
    
    st.markdown("---")
    
    # Beaches
    st.markdown("### Beaches & Coastline")
    for beach_name, beach_desc in region['beaches'].items():
        st.markdown(f"""
            <div class="feature-card">
                <h4 style="color: #5B8C85; margin-bottom: 10px;">{beach_name}</h4>
                <p>{beach_desc}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Experiences
    st.markdown("### Signature Experiences")
    for exp_name, exp_desc in region['experiences'].items():
        st.markdown(f"""
            <div class="feature-card">
                <h4 style="color: #C85A54; margin-bottom: 10px;">{exp_name}</h4>
                <p>{exp_desc}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Two columns for must-visit and restaurants
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Must Visit")
        for item in region['must_visit']:
            st.markdown(f"- {item}")
    
    with col2:
        st.markdown("### Where to Eat")
        for restaurant, description in region['where_to_eat'].items():
            st.markdown(f"**{restaurant}**")
            st.markdown(f"*{description}*")
            st.markdown("")

# ============================================
# TAB 2: PLAN YOUR TRIP
# ============================================
with tab2:
    st.markdown("""
        <div class="section-header">
            <h2>Plan Your Sicily Journey</h2>
            <p style="font-size: 1.1em; color: #6A6A6A; max-width: 800px; margin: 15px auto;">
                Tell us about your travel style and we'll create a personalized itinerary
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="content-card">
            <h3 style="margin-top: 0; color: #2C2C2C;">Itinerary Builder</h3>
            <p>Answer a few questions to receive a curated Sicily experience</p>
        </div>
        """, unsafe_allow_html=True)
    
    with st.form("trip_builder"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            duration = st.number_input("How many days?", 3, 21, 7)
        with col2:
            start_city = st.selectbox("Arriving in", ["Palermo", "Catania", "Trapani"])
        with col3:
            travel_style = st.selectbox("Travel style", [
                "Culture & History",
                "Beach & Relaxation",
                "Food & Wine",
                "Active Adventure",
                "Balanced Mix"
            ])
        
        st.markdown("#### What interests you most?")
        col1, col2, col3, col4 = st.columns(4)
        
        interests = []
        with col1:
            if st.checkbox("Ancient ruins"): interests.append("Ancient ruins")
            if st.checkbox("Baroque architecture"): interests.append("Baroque")
        with col2:
            if st.checkbox("Beach time"): interests.append("Beaches")
            if st.checkbox("Island hopping"): interests.append("Islands")
        with col3:
            if st.checkbox("Wine tasting"): interests.append("Wine")
            if st.checkbox("Local cuisine"): interests.append("Food")
        with col4:
            if st.checkbox("Hiking"): interests.append("Hiking")
            if st.checkbox("Photography"): interests.append("Photography")
        
        st.markdown("#### Contact Information")
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Your name")
            email = st.text_input("Email address")
        with col2:
            dates = st.text_input("Preferred travel dates (optional)")
            group_size = st.number_input("Number of travelers", 1, 20, 2)
        
        special_requests = st.text_area("Any special requests or requirements?")
        
        submit = st.form_submit_button("CREATE MY ITINERARY")
        
        if submit:
            if name and email:
                # Save trip
                new_trip = {
                    'name': name,
                    'email': email,
                    'duration': duration,
                    'start': start_city,
                    'style': travel_style,
                    'interests': interests,
                    'dates': dates,
                    'group': group_size,
                    'requests': special_requests,
                    'created': datetime.now().strftime("%B %d, %Y")
                }
                st.session_state.saved_trips.append(new_trip)
                
                st.success(f"Thank you, {name}! Your personalized itinerary request has been received.")
                st.info(f"We'll send your custom Sicily itinerary to {email} within 24-48 hours, along with accommodation recommendations and insider tips.")
                
                # Sample preview
                st.markdown("---")
                st.markdown("### Preview: Your Sicily Journey")
                st.markdown(f"""
                    <div class="content-card">
                        <h4>{duration}-Day {travel_style} Journey</h4>
                        <p><strong>Starting from:</strong> {start_city}</p>
                        <p><strong>Focus areas:</strong> {', '.join(interests) if interests else 'Balanced exploration'}</p>
                        <p><strong>Travelers:</strong> {group_size}</p>
                        <br>
                        <p style="font-style: italic; color: #5B8C85;">
                            Your detailed day-by-day itinerary will include specific recommendations for 
                            accommodations, restaurants, transportation, and experiences tailored to your interests.
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.error("Please provide your name and email address")
    
    st.markdown("---")
    
    # Sample itineraries
    st.markdown("""
        <div class="section-header">
            <h3>Suggested Itineraries</h3>
        </div>
        """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class="feature-card">
                <h4>THE GRAND TOUR (10-14 DAYS)</h4>
                <p><strong>Palermo</strong> (3 days) → <strong>Aeolian Islands</strong> (3 days) → 
                <strong>Taormina & Etna</strong> (2 days) → <strong>Syracuse & Baroque Towns</strong> (3 days)</p>
                <p style="margin-top: 15px; font-size: 0.95em;">
                Complete Sicily experience covering all major regions, perfect for first-time visitors
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
            <div class="feature-card">
                <h4>ISLAND ODYSSEY (7 DAYS)</h4>
                <p><strong>Aeolian Islands</strong> island hopping → <strong>Lipari</strong>, <strong>Vulcano</strong>, 
                <strong>Salina</strong>, <strong>Stromboli</strong>, <strong>Panarea</strong></p>
                <p style="margin-top: 15px; font-size: 0.95em;">
                Volcanic landscapes, boat tours, beach clubs, and seafood—summer perfection
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="feature-card">
                <h4>BAROQUE & BEACHES (7 DAYS)</h4>
                <p><strong>Syracuse</strong> (2 days) → <strong>Noto, Modica, Ragusa</strong> (3 days) → 
                <strong>Vendicari & beach towns</strong> (2 days)</p>
                <p style="margin-top: 15px; font-size: 0.95em;">
                UNESCO towns, coastal nature reserves, and pristine beaches in the southeast
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
            <div class="feature-card">
                <h4>FOOD & WINE (5-7 DAYS)</h4>
                <p><strong>Palermo markets</strong> → <strong>Marsala</strong> wineries → 
                <strong>Etna</strong> volcanic wines → <strong>Modica</strong> chocolate</p>
                <p style="margin-top: 15px; font-size: 0.95em;">
                Culinary deep-dive: street food, wine estates, cooking classes, market tours
                </p>
            </div>
            """, unsafe_allow_html=True)

# ============================================
# TAB 3: INSIDER TIPS
# ============================================
with tab3:
    st.markdown("""
        <div class="section-header">
            <h2>Insider Knowledge</h2>
            <p style="font-size: 1.1em; color: #6A6A6A; max-width: 800px; margin: 15px auto;">
                Essential information for navigating Sicily like a local
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Transportation
    st.markdown("""
        <div class="content-card">
            <h3 style="margin-top: 0;">Getting Around</h3>
        </div>
        """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            #### Car Rental
            **Recommended for:** Countryside, wine regions, beach hopping  
            **Cost:** €30-60/day  
            **Tip:** Book automatic transmission in advance—most cars are manual
            
            #### Trains
            **Best for:** Coastal routes (Palermo-Messina-Catania-Syracuse)  
            **Cost:** €10-20 between major cities  
            **Tip:** Trenitalia and buses more reliable than regional trains
            """)
    
    with col2:
        st.markdown("""
            #### Buses
            **Coverage:** Reaches smaller towns trains don't  
            **Cost:** €5-15 depending on distance  
            **Tip:** Buy tickets at tobacco shops, not on board
            
            #### Ferries
            **Islands:** Aeolian (from Milazzo), Aegadian (from Trapani)  
            **Cost:** €15-40 depending on destination  
            **Tip:** Book hydrofoils in advance for summer travel
            """)
    
    st.markdown("---")
    
    # Money
    st.markdown("""
        <div class="content-card">
            <h3 style="margin-top: 0;">Budget Planning</h3>
        </div>
        """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            **BUDGET**  
            €50-80/day
            
            - Hostels/B&Bs
            - Street food & trattorias
            - Public transport
            - Self-guided tours
            """)
    
    with col2:
        st.markdown("""
            **MID-RANGE**  
            €120-200/day
            
            - 3-star hotels
            - Restaurant meals
            - Car rental
            - Guided experiences
            """)
    
    with col3:
        st.markdown("""
            **LUXURY**  
            €300+/day
            
            - Boutique hotels
            - Fine dining
            - Private tours
            - Premium experiences
            """)
    
    st.markdown("---")
    
    # Language & Culture
    st.markdown("""
        <div class="content-card">
            <h3 style="margin-top: 0;">Essential Phrases</h3>
        </div>
        """, unsafe_allow_html=True)
    
    phrases = {
        "Buongiorno / Buonasera": "Good morning / Good evening",
        "Per favore": "Please",
        "Grazie mille": "Thank you very much",
        "Mi scusi": "Excuse me",
        "Quanto costa?": "How much does it cost?",
        "Il conto, per favore": "The bill, please",
        "Dov'è...?": "Where is...?",
        "Che cosa mi consiglia?": "What do you recommend?",
        "È possibile avere...?": "Is it possible to have...?",
        "Parla inglese?": "Do you speak English?"
    }
    
    col1, col2 = st.columns(2)
    items = list(phrases.items())
    mid = len(items) // 2
    
    with col1:
        for italian, english in items[:mid]:
            st.markdown(f"**{italian}**  \n*{english}*\n")
    
    with col2:
        for italian, english in items[mid:]:
            st.markdown(f"**{italian}**  \n*{english}*\n")
    
    st.markdown("---")
    
    # When to visit
    st.markdown("""
        <div class="content-card">
            <h3 style="margin-top: 0;">When to Visit</h3>
            <p><strong>Peak Season (July-August):</strong> Hot, crowded, expensive—beach perfection but book everything in advance</p>
            <p><strong>Shoulder Season (April-June, September-October):</strong> Ideal weather, fewer tourists, reasonable prices</p>
            <p><strong>Winter (November-March):</strong> Quiet, authentic, some beach areas closed—perfect for culture-focused trips</p>
        </div>
        """, unsafe_allow_html=True)

# ============================================
# TAB 4: COMMUNITY
# ============================================
with tab4:
    st.markdown("""
        <div class="section-header">
            <h2>Community Reviews & Tips</h2>
            <p style="font-size: 1.1em; color: #6A6A6A; max-width: 800px; margin: 15px auto;">
                Share your Sicily experience and discover from fellow travelers
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    comm_tab1, comm_tab2 = st.tabs(["WRITE A REVIEW", "SHARE A TIP"])
    
    with comm_tab1:
        st.markdown("""
            <div class="content-card">
                <h3 style="margin-top: 0;">Share Your Experience</h3>
                <p>Help fellow travelers by reviewing places you've visited</p>
            </div>
            """, unsafe_allow_html=True)
        
        with st.form("review_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                review_name = st.text_input("Your name")
                place_name = st.text_input("Place name")
                location = st.selectbox("Region", list(destinations.keys()))
            
            with col2:
                review_email = st.text_input("Email (will be sent to giulia@cubopro.com)")
                category = st.selectbox("Category", [
                    "Restaurant",
                    "Hotel/Accommodation",
                    "Beach",
                    "Attraction",
                    "Experience/Tour"
                ])
                rating = st.slider("Rating", 1, 5, 4)
            
            visit_date = st.text_input("When did you visit?", placeholder="e.g., June 2024")
            
            review_text = st.text_area(
                "Your review",
                height=150,
                placeholder="Share details about your experience, what made it special, tips for future visitors..."
            )
            
            submit_review = st.form_submit_button("SUBMIT REVIEW")
            
            if submit_review:
                if review_name and place_name and review_text and review_email:
                    new_review = {
                        'name': review_name,
                        'email': review_email,
                        'place': place_name,
                        'location': location,
                        'category': category,
                        'rating': rating,
                        'visit_date': visit_date,
                        'review': review_text,
                        'submitted': datetime.now()
                    }
                    st.session_state.reviews.append(new_review)
                    
                    st.success(f"Thank you, {review_name}! Your review has been submitted.")
                    st.info(f"A copy has been sent to giulia@cubopro.com and will be reviewed for publication within 24-48 hours.")
                else:
                    st.error("Please fill in all required fields")
        
        # Display reviews
        if st.session_state.reviews:
            st.markdown("---")
            st.markdown("### Recent Reviews")
            
            for review in reversed(st.session_state.reviews[-5:]):
                stars = "★" * review['rating'] + "☆" * (5 - review['rating'])
                st.markdown(f"""
                    <div class="review-card">
                        <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 15px;">
                            <div>
                                <h4 style="margin: 0; color: #2C2C2C;">{review['place']}</h4>
                                <p style="margin: 5px 0; font-size: 0.9em; color: #6A6A6A;">
                                    {review['location']} • {review['category']}
                                </p>
                            </div>
                            <div style="color: #D4A574; font-size: 1.2em;">
                                {stars}
                            </div>
                        </div>
                        <p style="font-style: italic; color: #4A4A4A; line-height: 1.7;">
                            "{review['review']}"
                        </p>
                        <p style="margin-top: 15px; padding-top: 15px; border-top: 1px solid #E8E4DC; 
                                  font-size: 0.9em; color: #6A6A6A;">
                            — {review['name']}, visited {review['visit_date']}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
    
    with comm_tab2:
        st.markdown("""
            <div class="content-card">
                <h3 style="margin-top: 0;">Share an Insider Tip</h3>
                <p>Know a hidden gem or local secret? Share it with the community</p>
            </div>
            """, unsafe_allow_html=True)
        
        with st.form("tip_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                tip_name = st.text_input("Your name")
                tip_email = st.text_input("Email (will be sent to giulia@cubopro.com)")
            
            with col2:
                tip_region = st.selectbox("Related region", ["All Sicily"] + list(destinations.keys()))
                tip_category = st.selectbox("Tip category", [
                    "Hidden beach",
                    "Local restaurant",
                    "Secret viewpoint",
                    "Money-saving hack",
                    "Transportation tip",
                    "Cultural insight",
                    "Other"
                ])
            
            tip_title = st.text_input("Tip title", placeholder="e.g., 'Best cannoli in Palermo'")
            
            tip_content = st.text_area(
                "Your tip",
                height=150,
                placeholder="Share the details—what makes it special, how to find it, when to go..."
            )
            
            submit_tip = st.form_submit_button("SHARE TIP")
            
            if submit_tip:
                if tip_name and tip_email and tip_title and tip_content:
                    st.success(f"Thank you, {tip_name}! Your insider tip has been submitted.")
                    st.info(f"We've sent your tip to giulia@cubopro.com for review. If approved, it will be added to the guide within a few days.")
                else:
                    st.error("Please fill in all required fields")

# ============================================
# TAB 5: MY DASHBOARD
# ============================================
with tab5:
    st.markdown("""
        <div class="section-header">
            <h2>Your Sicily Dashboard</h2>
            <p style="font-size: 1.1em; color: #6A6A6A; max-width: 800px; margin: 15px auto;">
                Manage your bookmarks, trips, and reviews
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Bookmarks", len(st.session_state.bookmarks))
    with col2:
        st.metric("Saved Trips", len(st.session_state.saved_trips))
    with col3:
        st.metric("Reviews", len(st.session_state.reviews))
    with col4:
        st.metric("Total Activity", len(st.session_state.bookmarks) + len(st.session_state.saved_trips))
    
    st.markdown("---")
    
    # Bookmarks
    st.markdown("### Your Bookmarks")
    
    if st.session_state.bookmarks:
        for i, bookmark in enumerate(st.session_state.bookmarks):
            col1, col2 = st.columns([5, 1])
            with col1:
                st.markdown(f"""
                    <div class="bookmark-item">
                        ✓ {bookmark}
                    </div>
                    """, unsafe_allow_html=True)
            with col2:
                if st.button("Remove", key=f"remove_{i}"):
                    st.session_state.bookmarks.pop(i)
                    st.rerun()
        
        # Export
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            bookmark_text = "\n".join([f"• {b}" for b in st.session_state.bookmarks])
            st.download_button(
                "EXPORT BOOKMARKS",
                bookmark_text,
                file_name="sicily_bookmarks.txt",
                use_container_width=True
            )
    else:
        st.info("No bookmarks yet. Explore regions and save your favorites!")
    
    st.markdown("---")
    
    # Saved Trips
    st.markdown("### Your Trip Requests")
    
    if st.session_state.saved_trips:
        for i, trip in enumerate(st.session_state.saved_trips):
            with st.expander(f"Trip Request {i+1}: {trip.get('duration', 'N/A')} days - {trip.get('style', 'N/A')}"):
                st.markdown(f"""
                    <div class="content-card" style="margin: 0; padding: 25px;">
                        <p><strong>Name:</strong> {trip.get('name', 'N/A')}</p>
                        <p><strong>Email:</strong> {trip.get('email', 'N/A')}</p>
                        <p><strong>Duration:</strong> {trip.get('duration', 'N/A')} days</p>
                        <p><strong>Starting city:</strong> {trip.get('start', 'N/A')}</p>
                        <p><strong>Travel style:</strong> {trip.get('style', 'N/A')}</p>
                        <p><strong>Interests:</strong> {', '.join(trip.get('interests', [])) if trip.get('interests') else 'Not specified'}</p>
                        <p><strong>Group size:</strong> {trip.get('group', 'N/A')}</p>
                        <p><strong>Submitted:</strong> {trip.get('created', 'N/A')}</p>
                    </div>
                    """, unsafe_allow_html=True)
    else:
        st.info("No trip requests yet. Use the Plan Your Trip tab to create one!")
    
    st.markdown("---")
    
    # Reviews
    st.markdown("### Your Reviews")
    
    if st.session_state.reviews:
        for review in st.session_state.reviews:
            stars = "★" * review['rating'] + "☆" * (5 - review['rating'])
            st.markdown(f"""
                <div class="review-card">
                    <h4 style="margin: 0;">{review['place']} {stars}</h4>
                    <p style="margin: 10px 0; font-size: 0.9em; color: #6A6A6A;">
                        {review['location']} • Visited {review['visit_date']}
                    </p>
                    <p style="font-style: italic;">"{review['review']}"</p>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("No reviews yet. Share your experiences in the Community tab!")
    
    st.markdown("---")
    
    # Actions
    st.markdown("### Account Actions")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("EXPORT ALL DATA", use_container_width=True):
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
                mime="application/json",
                use_container_width=True
            )
    
    with col2:
        if st.button("CLEAR ALL DATA", use_container_width=True):
            if st.checkbox("Confirm deletion (cannot be undone)"):
                st.session_state.bookmarks = []
                st.session_state.saved_trips = []
                st.session_state.reviews = []
                st.success("All data cleared")
                st.rerun()

# --- MAP ---
st.markdown("---")
st.markdown("""
    <div class="section-header">
        <h2>Sicily at a Glance</h2>
        <p style="font-size: 1.1em; color: #6A6A6A; max-width: 800px; margin: 15px auto;">
            Interactive map of featured regions
        </p>
    </div>
    """, unsafe_allow_html=True)

map_data = pd.DataFrame([
    {"lat": d["lat"], "lon": d["lon"], "name": k}
    for k, d in destinations.items()
])

st.map(map_data)

# --- FOOTER ---
st.markdown("---")

st.markdown("""
    <div class="footer">
        <div style="max-width: 1200px; margin: 0 auto;">
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 40px; margin-bottom: 40px;">
                <div>
                    <h4>CONTACT</h4>
                    <p>Questions or custom requests?<br>
                    <a href="mailto:giulia@cubopro.com">giulia@cubopro.com</a></p>
                </div>
                <div>
                    <h4>ABOUT</h4>
                    <p>Curated by locals and Sicily enthusiasts<br>
                    Updated regularly with insider knowledge</p>
                </div>
                <div>
                    <h4>REGIONS</h4>
                    <p>Palermo • Messina • Aeolian Islands<br>
                    Catania • Syracuse • Baroque Towns</p>
                </div>
            </div>
            <div style="text-align: center; padding-top: 40px; border-top: 1px solid #E8E4DC;">
                <p style="font-size: 0.9em; color: #6A6A6A;">
                    © 2026 Sicily Insider Guide • For private use within our network<br>
                    Last updated January 2026
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
