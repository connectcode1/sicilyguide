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

# --- CSS STYLING (Condé Nast Style) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700;800&family=Lato:wght@300;400;700&display=swap');
    
    .stApp { background-color: #FFFFFF; color: #2C2C2C; font-family: 'Lato', sans-serif; }
    
    /* Content Cards */
    .content-card {
        background: #FFFFFF; padding: 40px; border-top: 6px solid #D4A574;
        margin: 30px 0; box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    }
    
    /* Typography */
    h1 { font-family: 'Playfair Display', serif !important; color: #2C2C2C !important; font-size: 3.5em !important; }
    h2 { font-family: 'Playfair Display', serif !important; color: #C85A54 !important; font-size: 2.2em !important; margin-top: 40px !important; }
    h3 { font-family: 'Playfair Display', serif !important; color: #5B8C85 !important; }
    h4 { font-family: 'Lato', sans-serif !important; text-transform: uppercase !important; letter-spacing: 2px !important; font-weight: 700 !important; }
    
    /* Feature Cards for Lists */
    .list-card {
        background: #F8F6F2; padding: 20px; border-radius: 4px; margin-bottom: 15px;
        border-left: 3px solid #5B8C85;
    }
    
    /* Itinerary Stop */
    .itinerary-stop {
        background: #FFF; border: 1px solid #E8E4DC; border-left: 6px solid #C85A54;
        padding: 25px; margin-bottom: 20px;
    }
    
    /* Insider Quote */
    .insider-quote { 
        border-left: 4px solid #D4A574; padding: 25px; background: #F8F6F2; 
        font-style: italic; margin: 30px 0; font-family: 'Playfair Display', serif;
    }

    /* Buttons */
    .stButton>button { background: #C85A54; color: #FFFFFF; border: none; padding: 10px 25px; text-transform: uppercase; letter-spacing: 1px; }
    .stButton>button:hover { background: #B34A44; }
    
    /* Sidebar */
    section[data-testid="stSidebar"] { background: #F8F6F2; border-right: 1px solid #E8E4DC; }
    
    .hero-section { text-align: center; padding: 60px 20px; background: linear-gradient(180deg, #FFFFFF 0%, #F8F6F2 100%); border-bottom: 1px solid #E8E4DC; }
    </style>
    """, unsafe_allow_html=True)

# --- DATA: MERGED (Original Data + New Tags/Descriptions) ---
destinations = {
    "Palermo & Western Sicily": {
        "tagline": "Where Arab Domes Meet Norman Grandeur",
        "tags": ["Culture", "Street Food", "History", "Beaches"],
        "description": """Palermo is a city of contradictions and unexpected beauty, a place where the air hangs heavy with the scent of jasmine and fried chickpea fritters. To walk its streets is to read a history book written in stone: Byzantine mosaics shimmer inside Norman chapels, while red-domed Arab churches sit comfortably beside flamboyant Baroque palaces. 
        
        Head west, and the noise of the capital fades into the stillness of the salt pans of Trapani, where windmills silhouette against blazing sunsets. The medieval hilltop town of Erice floats above the clouds like a dream, offering almond pastries and ancient cobbled streets. This region is Sicily at its most authentic—unpolished, deeply historical, and fiercely proud.""",
        "insider_tip": "Visit the Palatine Chapel at 9 AM to see the mosaics light up, then head immediately to Ballarò Market for a panelle sandwich.",
        "must_visit": ["Palatine Chapel (Mosaic Masterpiece)", "Ballarò Market (Street Food)", "Erice (Medieval Hilltop)", "Segesta Temple (Greek Ruins)"],
        "beaches": {
            "Mondello Beach": "Palermo's Art Nouveau playground with turquoise waters.",
            "Riserva dello Zingaro": "7km of protected coastline accessible only on foot, with hidden coves.",
            "San Vito Lo Capo": "White sand beach beneath Monte Monaco, often called the 'Sicilian Caribbean'."
        },
        "where_to_eat": {
            "Antica Focacceria San Francesco": "Since 1834, the definitive pani ca' meusa (spleen sandwich).",
            "Pasticceria Cappello": "Cannoli filled to order—ricotta with pistachios is transcendent.",
            "Trattoria Ai Cascinari": "Pasta con le sarde, Palermo's signature dish, perfected."
        },
        "experiences": {
            "Street Food Tour": "Navigate Ballarò Market with a local guide.",
            "Monreale Mosaics": "Golden mosaics covering 6,400 square meters of biblical storytelling.",
            "Salt Pans of Trapani": "Sunset over ancient windmills and pink salt mountains."
        },
        "lat": 38.1157, "lon": 13.3615, "days": "4-5 days",
        "best_time": "April-June, Sept-Oct"
    },
    
    "Taormina, Messina & The Northeast": {
        "tagline": "The Dolce Vita Terrace Overlooking the Sea",
        "tags": ["Luxury", "Views", "Romance", "Beaches"],
        "description": """There is a reason writers and artists have flocked to Taormina for centuries. Perched precariously on a cliffside, it offers perhaps the most dramatic view in all of Italy: the crumbling columns of an ancient Greek theater framing the smoking cone of Mount Etna and the turquoise Ionian Sea below. The town itself is a manicured jewel box of high-end boutiques and hidden gardens.
        
        Just above lies the medieval village of Castelmola, famous for its almond wine. Down on the coast, the Isola Bella nature reserve offers snorkeling in crystal-clear water. This region blends the sophisticated 'Dolce Vita' lifestyle with breathtaking natural drama.""",
        "insider_tip": "Skip the main street of Taormina at midday. Instead, take the cable car down to Mazzarò and boat to the Blue Grotto before the crowds arrive.",
        "must_visit": ["Greek Theater (Views of Etna)", "Isola Bella (Nature Reserve)", "Castelmola (Panorama)", "Savoca (Godfather filming location)"],
        "beaches": {
            "Isola Bella": "Taormina's jewel—a pebble beach connected to an island by a sandbar.",
            "Giardini Naxos": "Wide sandy beaches below Taormina, the first Greek colony in Sicily.",
            "Letojanni": "Pebble beach village, a quieter alternative to Taormina."
        },
        "where_to_eat": {
            "Bam Bar": "Taormina's legendary granita—try almond with warm brioche.",
            "Osteria Nero d'Avola": "Intimate restaurant in Taormina, Sicilian classics elevated.",
            "Trattoria da Pina": "Letojanni favorite for swordfish and local wine."
        },
        "experiences": {
            "Ancient Theater Concert": "Attend a summer concert with Mount Etna as the backdrop.",
            "Messina Clock Tower": "Astronomical clock at noon triggers a mechanical show.",
            "Godfather Tour": "Visit Bar Vitelli in Savoca for a lemon granita."
        },
        "lat": 37.8526, "lon": 15.2876, "days": "3-4 days",
        "best_time": "May-June, Sept-Oct"
    },
    
    "Aeolian Islands": {
        "tagline": "Seven Volcanic Sisters in the Deep Blue",
        "tags": ["Islands", "Nature", "Volcanoes", "Boating", "Relaxation"],
        "description": """Rising from the cobalt Tyrrhenian Sea like dark pyramids, the Aeolian Islands feel like a world apart. UNESCO-protected and fiercely beautiful, each of the seven islands has a distinct soul. Stromboli is the wild child, a continuously active volcano where you can watch lava fireworks against the night sky. Panarea is the chic retreat, a whitewashed maze of bougainvillea and luxury villas.
        
        Salina, the greenest island, is a paradise of caper bushes and Malvasia vineyards. The magic here is elemental: black sand beaches, thermal mud baths, and the sensation of being small in the face of nature's power.""",
        "insider_tip": "Rent a private boat on Salina. It’s the only way to find the hidden cove of Pollara, made famous by the film 'Il Postino'.",
        "must_visit": ["Stromboli (Active Volcano)", "Pollara Beach (Salina)", "Vulcano Mud Baths", "Panarea Prehistoric Village"],
        "beaches": {
            "Pollara Beach (Salina)": "Crescent bay beneath volcanic cliffs.",
            "Spiaggia Bianca (Lipari)": "White pumice beach contrasting with turquoise water.",
            "Vulcano Thermal Beaches": "Natural hot springs meet the sea, therapeutic volcanic mud."
        },
        "where_to_eat": {
            "Capofaro (Salina)": "Michelin-starred restaurant in a Malvasia vineyard.",
            "Il Filippino (Lipari)": "Historic restaurant specializing in capers and seafood.",
            "Punta Lena (Stromboli)": "Terrace dining with direct volcano views."
        },
        "experiences": {
            "Stromboli Night Hike": "Guided climb to witness eruptions at sunset.",
            "Boat Tour": "Full-day excursion visiting multiple islands and hidden grottos.",
            "Malvasia Tasting": "Sweet wine made from grapes dried on volcanic terraces."
        },
        "lat": 38.5667, "lon": 14.9564, "days": "5-7 days",
        "best_time": "May-June, September"
    },
    
    "Catania, Etna & The East": {
        "tagline": "Fire, Lava Stone, and Barque Energy",
        "tags": ["Volcanoes", "Wine", "Food", "City"],
        "description": """Catania is the city of the volcano. Built from the very lava that has destroyed it multiple times, it is a city of black and white—buildings of dark volcanic stone framed by white limestone trim. It is grittier than Palermo but arguably more alive, with a fish market that screams with the energy of a Souk.
        
        Looming over everything is 'Mamma Etna.' Europe's highest active volcano is not just a backdrop; it is a presence. Its slopes are home to some of the world's most exciting wine production, where ancient vines struggle through mineral-rich ash to produce reds of incredible depth.""",
        "insider_tip": "Don't just look at Etna; drink it. Book a tasting at a winery in Passopisciaro to taste the 'Nerello Mascalese' grown on volcanic terraces.",
        "must_visit": ["Mount Etna Summit", "Catania Fish Market", "Benedictine Monastery", "Etna Wineries"],
        "beaches": {
            "San Giovanni Li Cuti": "Catania's black lava rock beach with sunset views.",
            "Aci Trezza": "Fishing village with the Cyclops' legendary basalt rocks offshore.",
            "Aci Castello": "Black sand beach below a Norman castle on volcanic rock."
        },
        "where_to_eat": {
            "Savia": "The definitive arancino—try al burro and al ragù.",
            "FUD": "Modern Catanese cuisine, horsemeat specialties.",
            "Trattoria de Fiore": "Pasta alla Norma (eggplant, ricotta, basil)—Catania's signature."
        },
        "experiences": {
            "Etna Summit Hike": "Guided trek to active craters with volcanologist.",
            "Catania Fish Market": "A Pescheria at dawn—tuna, swordfish, and controlled chaos.",
            "Etna Wine Tour": "Visit boutique wineries at 800-1000m elevation."
        },
        "lat": 37.5079, "lon": 15.0830, "days": "3-4 days",
        "best_time": "April-June, Oct-Nov"
    },
    
    "Syracuse & The Baroque Southeast": {
        "tagline": "Greek Myths and Golden Stone",
        "tags": ["History", "Architecture", "Baroque", "Culture"],
        "description": """If you want to understand the ancient world, come to Syracuse. Once the rival of Athens, its archaeological park holds vast Greek theaters and Roman amphitheaters. But the true heart is the island of Ortigia, a labyrinth of narrow streets that opens onto a cathedral built literally around an ancient Greek temple.
        
        Travel inland to the Val di Noto, and the scenery changes to rolling hills and deep gorges. Here, the towns of Noto, Modica, and Ragusa Ibla cling to the hillsides in a riot of Baroque splendor. Rebuilt after a massive earthquake in 1693, they glow with a honey-colored limestone that turns gold at sunset.""",
        "insider_tip": "In Ortigia, swim off the rocks at the Forte Vigliena at sunset, then walk to Piazza Duomo to see the cathedral lit up against the night sky.",
        "must_visit": ["Ortigia Island", "Neapolis Park (Greek Theater)", "Noto Cathedral", "Modica Chocolate Shop"],
        "beaches": {
            "Fontane Bianche": "Powdery white sand and shallow turquoise water, family paradise.",
            "Vendicari Reserve": "Nature reserve with pristine beaches and flamingo spotting.",
            "Marzamemi": "Fishing village with tuna traditions and beach bars."
        },
        "where_to_eat": {
            "Caffè Sicilia (Noto)": "Legendary granita, featured in Chef's Table.",
            "Don Camillo (Syracuse)": "Fine dining in a 15th-century palazzo.",
            "Accursio (Modica)": "Michelin star, contemporary Sicilian."
        },
        "experiences": {
            "Greek Theater Plays": "Classical performances June-July in the ancient setting.",
            "Noto by Night": "Baroque facades illuminated—architectural masterpiece.",
            "Modica Chocolate Tour": "Aztec-style grainy chocolate, workshops available."
        },
        "lat": 37.0755, "lon": 15.2866, "days": "4-5 days",
        "best_time": "May-June, Sept"
    }
}

# --- HEADER ---
st.markdown("""
    <div class="hero-section">
        <p style="font-size: 0.9em; text-transform: uppercase; letter-spacing: 3px; color: #C85A54; font-weight: 600;">Curated Travel Guide</p>
        <h1>Sicily</h1>
        <p style="font-size: 1.2em; color: #5B8C85; font-style: italic;">An insider's journey through the island of light and shadow</p>
    </div>
    """, unsafe_allow_html=True)

# --- CLEANED SIDEBAR (No Dashboard) ---
with st.sidebar:
    st.markdown("#### THE INSIDER")
    st.info("Explore the island through local eyes. Select a tab to begin your journey.")
    st.markdown("---")
    st.markdown("#### QUICK TIPS")
    st.write("• **Driving:** Essential for the coast.")
    st.write("• **Siesta:** Shops close 1:30 PM - 4:30 PM.")
    st.write("• **Dinner:** Locals eat after 8:30 PM.")
    st.markdown("---")
    st.caption("© 2026 Sicily Insider")

# --- MAIN TABS ---
tab1, tab2, tab3 = st.tabs(["EXPLORE REGIONS", "PLAN YOUR TRIP", "INSIDER TIPS"])

# ============================================
# TAB 1: EXPLORE REGIONS (Restored Lists)
# ============================================
with tab1:
    st.markdown("## Discover by Region")
    selected_region = st.selectbox("Select a region to explore", list(destinations.keys()))
    region = destinations[selected_region]
    
    # Hero Description
    st.markdown(f"""
        <div class="content-card">
            <h2 style="margin-top:0;">{selected_region}</h2>
            <h4 style="color:#5B8C85;">{region['tagline']}</h4>
            <p style="margin-top:20px;">{region['description']}</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Insider Tip & Stats
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(f"""
            <div class="insider-quote">
                <strong>Insider Tip:</strong> {region['insider_tip']}
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("### Quick Facts")
        st.write(f"**Stay:** {region['days']}")
        st.write(f"**Best Time:** {region['best_time']}")
        st.write("**Best For:** " + ", ".join(region['tags']))
    
    st.markdown("---")
    
    # RESTORED DETAILED SECTIONS
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown("### 🏛️ History & Experiences")
        for item, desc in region['experiences'].items():
            st.markdown(f"""
            <div class="list-card">
                <strong>{item}</strong><br>
                <span style="font-size:0.9em; color:#4A4A4A;">{desc}</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("### ⛱️ Beaches")
        for beach, desc in region['beaches'].items():
            st.markdown(f"- **{beach}**: {desc}")

    with col_b:
        st.markdown("### 🍝 Where to Eat")
        for place, desc in region['where_to_eat'].items():
            st.markdown(f"""
            <div class="list-card" style="border-left-color: #C85A54;">
                <strong>{place}</strong><br>
                <span style="font-size:0.9em; color:#4A4A4A;">{desc}</span>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("### 📍 Must Visit")
        for item in region['must_visit']:
            st.markdown(f"- {item}")

# ============================================
# TAB 2: INSTANT ITINERARY GENER
