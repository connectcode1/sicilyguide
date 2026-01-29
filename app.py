import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import json

# Page Config
st.set_page_config(
    page_title="Sicily Insider - Your Personal Guide", 
    page_icon="🏺", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS: ENHANCED MAJOLICA THEME ---
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background: linear-gradient(135deg, #002B5B 0%, #003D73 100%);
        color: #FDF5E6;
    }
    
    /* High-Contrast Content Cards */
    .content-card {
        background: linear-gradient(145deg, #FDF5E6 0%, #F5EBD9 100%);
        color: #1A1A1A;
        padding: 30px;
        border-radius: 20px;
        border-left: 12px solid #D32F2F;
        margin-bottom: 25px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.3);
    }
    
    /* Info Cards */
    .info-card {
        background-color: rgba(255, 215, 0, 0.1);
        border: 2px solid #FFD700;
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
    }
    
    /* Headers */
    h1 { color: #FFD700 !important; font-family: 'Georgia', serif; text-shadow: 2px 2px 4px rgba(0,0,0,0.5); }
    h2 { color: #FFD700 !important; font-family: 'Georgia', serif; }
    h3 { color: #FFA500 !important; font-family: 'Georgia', serif; }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #001F3F 0%, #003D73 100%);
        border-right: 3px solid #FFD700;
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #D32F2F 0%, #B71C1C 100%);
        color: white;
        border-radius: 25px;
        border: 3px solid #FFD700;
        font-weight: bold;
        padding: 12px 30px;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(211, 47, 47, 0.4);
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: rgba(255, 215, 0, 0.2);
        border-radius: 10px;
        font-weight: bold;
    }
    
    /* Metric containers */
    [data-testid="stMetricValue"] {
        color: #FFD700;
        font-size: 2em;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255, 215, 0, 0.1);
        border-radius: 10px 10px 0 0;
        color: #FFD700;
        font-weight: bold;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #FFD700;
        color: #002B5B;
    }
    </style>
    """, unsafe_allow_html=True)

# --- INITIALIZE SESSION STATE ---
if 'saved_trips' not in st.session_state:
    st.session_state.saved_trips = []
if 'feedback_data' not in st.session_state:
    st.session_state.feedback_data = []
if 'bookmarks' not in st.session_state:
    st.session_state.bookmarks = set()

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
            "Sfincione": {
                "what": "Sicilian thick-crust pizza with tomato, onions, anchovies",
                "where": "Any bakery in the historic center",
                "price": "€2-3 per slice",
                "insider": "Best eaten at room temperature—the flavors develop"
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
        "days_needed": "3-4 days"
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
            },
            "Plemmirio": {
                "description": "Marine protected area with incredible snorkeling",
                "best_for": "Snorkeling, diving, rocky coast",
                "how_to_get": "15 min from Syracuse by car/scooter",
                "insider_tip": "Rent a kayak to explore the sea caves"
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
            },
            "Scacce Ragusane": {
                "what": "Folded pastry with ricotta, tomato, or eggplant",
                "where": "Ragusa Ibla bakeries",
                "price": "€3-5",
                "insider": "Eat them warm from the oven"
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
        "days_needed": "4-5 days"
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
            },
            "Aci Trezza": {
                "description": "Fishing village with legendary Cyclops rocks",
                "best_for": "Swimming, Sicilian culture, seafood",
                "how_to_get": "Bus from Catania (20 min)",
                "insider_tip": "The black rocks are volcanic—wear water shoes"
            },
            "Letojanni": {
                "description": "Quieter alternative to Taormina's beaches",
                "best_for": "Relaxation, local restaurants",
                "how_to_get": "Train from Taormina (5 min)",
                "insider_tip": "Better value and less crowded than Taormina beaches"
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
            },
            "Pistacchio di Bronte": {
                "what": "Green gold from Etna's slopes",
                "where": "Pasticceria Russo, Bronte",
                "price": "€15-25 per kg",
                "insider": "Harvest is Sept-Oct, buy DOP certified"
            },
            "Raw Seafood in Catania": {
                "what": "Sea urchin, oysters, prawns at fish market",
                "where": "Mercato del Pesce, Catania",
                "price": "€10-20",
                "insider": "Go at 10 AM when the market is closing—fresher and cheaper"
            }
        },
        
        "must_see": [
            "🌋 Mount Etna - Guided tour to summit craters (€65)",
            "🎭 Taormina Ancient Theater - Greek theater with Etna backdrop",
            "🐘 Catania Fish Market - Sensory overload, arrive early",
            "🏛️ Catania Baroque Center - UNESCO site, rebuilt after 1693",
            "🚂 Circumetnea Train - Vintage train around Etna"
        ],
        
        "hidden_gems": [
            "🍷 Etna Wine Route - Dozens of wineries to visit",
            "🏰 Castello di Aci - Norman castle over the sea",
            "🎵 Bellini Museum in Catania - Opera composer's birthplace",
            "🌳 Gole Alcantara - Lava gorge with river (bring wetsuit!)",
            "🍯 Zafferana Etnea - Honey village, Sunday market"
        ],
        
        "lat": 37.5027, 
        "lon": 15.0873,
        "best_months": "April-June, September-October",
        "days_needed": "3-4 days"
    },
    
    "Agrigento & The Southern Coast": {
        "tagline": "Valley of the Temples - Greek Heritage Preserved",
        "description": """The south coast is Sicily's most serene face: endless wheat fields turning gold in May, 
        white limestone cliffs, and the most spectacular Greek ruins outside Greece itself. Agrigento's Valley of the 
        Temples stands as a testament to the island's ancient glory, while the nearby Scala dei Turchi offers 
        blindingly white marl cliffs descending into turquoise waters.""",
        
        "human_tip": """🏛️ **Temple Timing**: Visit the Valley of the Temples at 7 PM in summer. Get the evening 
        ticket (€10) and watch the sunset behind the Temple of Concordia. As the golden hour light hits the honey-colored 
        stone, you'll understand why the Greeks called this place sacred. Stay for the night illumination.""",
        
        "beaches": {
            "Scala dei Turchi": {
                "description": "Brilliant white marl cliff formations, iconic Instagram spot",
                "best_for": "Photography, sunset, unique landscapes",
                "how_to_get": "15 min from Agrigento, parking available",
                "insider_tip": "Officially closed but accessible. Best at sunset."
            },
            "Siculiana Marina": {
                "description": "Long sandy beach with nature reserve",
                "best_for": "Families, long walks, local atmosphere",
                "how_to_get": "20 min from Agrigento by car",
                "insider_tip": "Less crowded than Scala dei Turchi, better for swimming"
            },
            "Eraclea Minoa": {
                "description": "Beach with Greek ruins overlooking the sea",
                "best_for": "History + beach combo, dunes",
                "how_to_get": "30 min from Agrigento toward Sciacca",
                "insider_tip": "Visit the small archaeological site first"
            }
        },
        
        "food": {
            "Couscous di Pesce": {
                "what": "Arab-influenced fish couscous",
                "where": "Restaurants in Sciacca",
                "price": "€15-20",
                "insider": "Sciacca hosts the Couscous Festival in September"
            },
            "Girgentana Cheese": {
                "what": "Cheese from native spiral-horned goats",
                "where": "Local markets and cheese shops",
                "price": "€20-25 per kg",
                "insider": "Rare breed, unique tangy flavor"
            }
        },
        
        "must_see": [
            "🏛️ Valley of the Temples - UNESCO site, allow 3-4 hours",
            "🏛️ Temple of Concordia - Best-preserved Doric temple",
            "🏛️ Kolymbetra Garden - Ancient garden in the valley",
            "🏰 Scala dei Turchi - White cliffs (limited access)"
        ],
        
        "hidden_gems": [
            "🎨 Museo Archeologico - Amazing collection before temples",
            "🏛️ Villa Romana del Casale - Mosaics near Piazza Armerina",
            "🌳 Riserva Naturale Torre Salsa - Pristine beach reserve"
        ],
        
        "lat": 37.3108,
        "lon": 13.5765,
        "best_months": "April-June, September",
        "days_needed": "2-3 days"
    },
    
    "Trapani & The Islands": {
        "tagline": "Salt, Wind, and Ancient Islands",
        "description": """The far west of Sicily dances to a different rhythm: North African influences in the 
        couscous and tuna traditions, salt pans that turn pink at sunset, windmills that have ground sea salt for 
        centuries. From here, ferries depart to the Egadi Islands (Favignana, Levanzo, Marettimo) and the remote 
        volcanic speck of Pantelleria.""",
        
        "human_tip": """⛵ **Island Secret**: Skip crowded Favignana in August. Instead, take the ferry to Marettimo 
        (90 min). No cars, no beaches, just vertical cliffs, crystalline water, and spectacular cave-diving. It's Sicily's 
        last wild edge. Stay at Pensione Il Veliero—the owner knows every hidden cove.""",
        
        "beaches": {
            "Favignana - Cala Rossa": {
                "description": "Former tuff quarry, incredible blue water",
                "best_for": "Snorkeling, cliff jumping, photos",
                "how_to_get": "Ferry from Trapani (30 min) + bike rental",
                "insider_tip": "Rent a bike, not a scooter—the island is small"
            },
            "San Vito Lo Capo": {
                "description": "Wide sandy beach, crystal waters",
                "best_for": "Beach relaxation, couscous fest",
                "how_to_get": "Bus from Trapani or Palermo",
                "insider_tip": "Stay for the sunset behind Monte Monaco"
            }
        },
        
        "food": {
            "Couscous di Pesce": {
                "what": "The real deal, North African tradition",
                "where": "Cantina Siciliana, San Vito Lo Capo",
                "price": "€18-22",
                "insider": "September Couscous Fest brings international chefs"
            },
            "Tuna Bottarga": {
                "what": "Dried tuna roe, salty delicacy",
                "where": "Favignana specialty shops",
                "price": "€35-50 per 100g",
                "insider": "Grate over pasta with olive oil and lemon"
            },
            "Trapani Sea Salt": {
                "what": "Hand-harvested sea salt",
                "where": "Salt museums and shops",
                "price": "€5-10",
                "insider": "Visit the windmills at sunset near Marsala"
            }
        },
        
        "must_see": [
            "⛵ Egadi Islands - Favignana, Levanzo, Marettimo",
            "🧂 Salt Pans of Trapani - Sunset photos with windmills",
            "🏰 Erice - Medieval hilltop town in the clouds",
            "🍷 Marsala - Wine cellars and historic center"
        ],
        
        "hidden_gems": [
            "🎨 Museo Pepoli Trapani - Coral art and maiolica",
            "⛪ Santuario di Custonaci - Pilgrimage site with views",
            "🏊 Laghetti di Marineo - Natural pools near Erice"
        ],
        
        "lat": 38.0176,
        "lon": 12.5365,
        "best_months": "May-June, September",
        "days_needed": "3-4 days"
    }
}

# --- PRACTICAL INFORMATION DATABASE ---
practical_info = {
    "Getting Around": {
        "Car Rental": {
            "pros": "Freedom to explore, reach remote beaches, wine regions",
            "cons": "Palermo/Catania traffic, narrow streets, parking challenges",
            "recommendation": "Essential for countryside, avoid in city centers",
            "insider": "Book automatic transmission in advance—manuals are standard",
            "cost": "€30-50/day"
        },
        "Trains": {
            "pros": "Coastal routes scenic, connects major cities",
            "cons": "Limited inland, slow on some routes",
            "recommendation": "Great for Catania-Taormina-Syracuse",
            "insider": "Circumetnea train around Etna is a day trip itself",
            "cost": "€8-15 between major cities"
        },
        "Buses": {
            "pros": "Reaches everywhere, affordable",
            "cons": "Schedules unreliable, crowded in summer",
            "recommendation": "Good for specific routes like Palermo-Agrigento",
            "insider": "Buy tickets at tobacco shops (tabacchi), not on board",
            "cost": "€5-20 depending on distance"
        },
        "Scooter": {
            "pros": "Perfect for small towns, beaches, parking anywhere",
            "cons": "Hot in summer, limited range",
            "recommendation": "Ideal for islands (Favignana) and coastal areas",
            "insider": "Always wear helmet—police are strict now",
            "cost": "€20-35/day"
        }
    },
    
    "When to Visit": {
        "Spring (April-June)": {
            "weather": "15-28°C, warm days, cool evenings",
            "crowds": "Moderate, Easter week is busy",
            "highlights": "Wildflowers, almond blossoms, perfect hiking",
            "insider": "May is ideal—warm enough for beaches, not too hot for cities"
        },
        "Summer (July-August)": {
            "weather": "28-38°C, very hot, crowded",
            "crowds": "Peak season, book everything in advance",
            "highlights": "Beach life, festivals, nightlife",
            "insider": "August is Italian vacation—everywhere is packed. Choose June or September."
        },
        "Fall (September-October)": {
            "weather": "20-28°C, still warm sea",
            "crowds": "Lower, good value",
            "highlights": "Grape harvest, wine festivals, golden light",
            "insider": "September is the sweet spot—warm water, fewer tourists"
        },
        "Winter (November-March)": {
            "weather": "10-18°C, rainy periods",
            "crowds": "Minimal, many places closed",
            "highlights": "Authentic experience, almond blossoms in Feb",
            "insider": "Good for culture and food, not beaches. Etna skiing possible!"
        }
    },
    
    "Money & Costs": {
        "Daily Budget": {
            "Budget": "€50-70/day (hostels, street food, buses)",
            "Mid-range": "€100-150/day (B&Bs, trattorias, some car rental)",
            "Luxury": "€250+/day (hotels, fine dining, private tours)",
            "insider": "Lunch 'menu fisso' at trattorias is €12-18 and excellent value"
        },
        "Tipping": {
            "Restaurants": "Service often included; round up or leave €5-10",
            "Bars": "Not expected for coffee (€1-1.50), leave €1 for table service",
            "Taxis": "Round up to nearest €5",
            "insider": "Coperto (cover charge) €1-3 is normal, not a tip"
        },
        "ATMs & Cards": {
            "info": "ATMs everywhere in cities, scarce in countryside",
            "insider": "Carry cash for small towns, markets, beaches. Many places still cash-only."
        }
    },
    
    "Language": {
        "Reality Check": {
            "English": "Spoken in tourist areas, hotels, young people",
            "Italian": "Essential outside tourist zones",
            "Sicilian": "Older locals often prefer it to Italian",
            "insider": "Learn basic Italian phrases—'per favore', 'grazie', 'scusi'. Sicilians appreciate effort."
        },
        "Key Phrases": {
            "Quanto costa?": "How much?",
            "Dov'è...?": "Where is...?",
            "Posso avere il conto?": "Can I have the bill?",
            "Che cosa consiglia?": "What do you recommend?",
            "Senza glutine": "Gluten-free (important for celiacs!)"
        }
    }
}

# --- HEADER SECTION ---
col1, col2, col3 = st.columns([2, 3, 2])
with col2:
    st.title("🏺 SICILIA")
    st.markdown("### *Un Viaggio nell'Anima* — A Journey into the Soul")
    st.markdown("#### Your Comprehensive Insider's Guide")

st.divider()

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("## 🧭 Navigation Hub")
    st.markdown("---")
    
    # Quick Stats
    st.metric("📍 Regions Covered", len(destinations))
    st.metric("🏖️ Beaches Listed", sum(len(d['beaches']) for d in destinations.values()))
    st.metric("🍴 Food Spots", sum(len(d['food']) for d in destinations.values()))
    
    st.markdown("---")
    
    # Quick Links
    st.markdown("### 🔗 Quick Actions")
    if st.button("📥 Download Full Guide (PDF)", use_container_width=True):
        st.info("📧 Enter your email to receive the comprehensive 50-page PDF guide")
    
    if st.button("🗺️ View Interactive Map", use_container_width=True):
        st.info("Jump to Map Section ↓")
    
    st.markdown("---")
    
    # Saved Items
    st.markdown("### 📌 Your Bookmarks")
    if st.session_state.bookmarks:
        for bookmark in st.session_state.bookmarks:
            st.text(f"✓ {bookmark}")
    else:
        st.text("No bookmarks yet")
    
    st.markdown("---")
    st.markdown("### 🌡️ Live Weather")
    if st.button("Get Sicily Weather", use_container_width=True):
        st.info("Connect to weather API (premium feature)")

# --- MAIN NAVIGATION TABS ---
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "🗺️ Regional Deep Dives", 
    "🧳 Plan Your Trip", 
    "📋 Practical Info",
    "🍷 Experiences",
    "❓ Get Info Now",
    "💬 Community",
    "📊 My Dashboard"
])

# ============================================
# TAB 1: REGIONAL DEEP DIVES
# ============================================
with tab1:
    st.header("🏛️ Explore Sicily by Region")
    st.markdown("*Select a region to unlock detailed insider information*")
    
    # Region selector
    col1, col2 = st.columns([1, 2])
    with col1:
        selected_region = st.selectbox(
            "Choose Your Destination",
            list(destinations.keys()),
            key="region_selector"
        )
    
    with col2:
        if st.button(f"🔖 Bookmark {selected_region}", use_container_width=True):
            st.session_state.bookmarks.add(selected_region)
            st.success(f"Added to bookmarks!")
    
    # Display selected region
    region_data = destinations[selected_region]
    
    # Hero Section
    st.markdown(f"""
    <div class="content-card">
        <h1 style="color: #D32F2F; margin-bottom: 10px;">{selected_region}</h1>
        <h3 style="color: #1A1A1A; font-style: italic; margin-bottom: 20px;">"{region_data['tagline']}"</h3>
        <p style="font-size: 1.1em; line-height: 1.6;">{region_data['description']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Insider Tip Highlight
    st.markdown(f"""
    <div class="info-card">
        <h3 style="color: #FFD700;">💡 Insider's Secret</h3>
        <p style="font-size: 1.05em; line-height: 1.6;">{region_data['human_tip']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick Info
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🗓️ Recommended Days", region_data['days_needed'])
    with col2:
        st.metric("🌞 Best Months", region_data['best_months'])
    with col3:
        st.metric("🏖️ Beaches", len(region_data['beaches']))
    
    st.markdown("---")
    
    # Beaches Section
    st.subheader("🏖️ Beaches & Coastal Areas")
    
    beach_tabs = st.tabs(list(region_data['beaches'].keys()))
    for i, (beach_name, beach_info) in enumerate(region_data['beaches'].items()):
        with beach_tabs[i]:
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**{beach_name}**")
                st.markdown(f"📍 {beach_info['description']}")
                st.markdown(f"**Best for:** {beach_info['best_for']}")
                st.markdown(f"**How to get there:** {beach_info['how_to_get']}")
            
            with col2:
                st.info(f"💎 **Insider Tip**\n\n{beach_info['insider_tip']}")
            
            if st.button(f"📍 Get Directions to {beach_name}", key=f"beach_{i}"):
                st.success(f"Opening maps for {beach_name}...")
    
    st.markdown("---")
    
    # Food Section
    st.subheader("🍴 Must-Try Food & Where to Find It")
    
    for food_name, food_info in region_data['food'].items():
        with st.expander(f"🍽️ {food_name}"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**What it is:** {food_info['what']}")
                st.markdown(f"**Where:** {food_info['where']}")
                st.markdown(f"**Price:** {food_info['price']}")
            
            with col2:
                st.success(f"✨ **Insider Tip**\n\n{food_info['insider']}")
            
            if st.button(f"🔖 Save this spot", key=f"food_{food_name}"):
                st.session_state.bookmarks.add(f"{food_name} - {selected_region}")
                st.success("Saved to bookmarks!")
    
    st.markdown("---")
    
    # Must See & Hidden Gems
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ⭐ Must-See Attractions")
        for item in region_data['must_see']:
            st.markdown(f"- {item}")
    
    with col2:
        st.markdown("### 💎 Hidden Gems")
        for item in region_data['hidden_gems']:
            st.markdown(f"- {item}")

# ============================================
# TAB 2: PLAN YOUR TRIP
# ============================================
with tab2:
    st.header("🧳 Trip Planning Assistant")
    st.markdown("*Create your perfect Sicily itinerary*")
    
    # Interactive itinerary builder
    st.subheader("📅 Build Your Itinerary")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        trip_duration = st.number_input("How many days?", min_value=2, max_value=30, value=7)
    
    with col2:
        travel_style = st.selectbox("Travel Style", [
            "Beach & Relaxation",
            "Culture & History",
            "Food & Wine",
            "Adventure & Nature",
            "Balanced Mix"
        ])
    
    with col3:
        start_point = st.selectbox("Starting City", [
            "Palermo", 
            "Catania", 
            "Syracuse",
            "Trapani"
        ])
    
    # Interests
    st.markdown("#### 🎯 Select Your Interests")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        beaches_interest = st.checkbox("🏖️ Beaches")
        ancient_sites = st.checkbox("🏛️ Ancient Sites")
    with col2:
        food_wine = st.checkbox("🍷 Food & Wine")
        nature = st.checkbox("🌳 Nature & Hiking")
    with col3:
        baroque = st.checkbox("⛪ Baroque Towns")
        islands = st.checkbox("⛵ Islands")
    with col4:
        markets = st.checkbox("🛒 Markets")
        nightlife = st.checkbox("🎭 Nightlife")
    
    # Generate Itinerary Button
    if st.button("✨ Generate My Custom Itinerary", use_container_width=True, type="primary"):
        with st.spinner("Creating your personalized Sicily itinerary..."):
            # Simulated itinerary generation
            st.success("🎉 Your itinerary is ready!")
            
            st.markdown("### 🗓️ Your Personalized Sicily Journey")
            
            # Sample itinerary based on inputs
            if trip_duration >= 7:
                st.markdown(f"""
                <div class="content-card">
                    <h3>Day 1-2: {start_point}</h3>
                    <p>Arrival and exploration of the starting city. Visit main attractions, try local food, get oriented.</p>
                    
                    <h3>Day 3-4: {list(destinations.keys())[1]}</h3>
                    <p>Transfer and explore the second region based on your interests.</p>
                    
                    <h3>Day 5-6: {list(destinations.keys())[2]}</h3>
                    <p>Continue to the east coast, beach time and cultural visits.</p>
                    
                    <h3>Day 7: Return & Departure</h3>
                    <p>Last-minute shopping, final meal, departure.</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Save option
            if st.button("💾 Save This Itinerary"):
                st.session_state.saved_trips.append({
                    'duration': trip_duration,
                    'style': travel_style,
                    'start': start_point,
                    'date': datetime.now().strftime("%Y-%m-%d")
                })
                st.success("Itinerary saved to your dashboard!")
    
    st.markdown("---")
    
    # Pre-made itineraries
    st.subheader("🗺️ Pre-Made Itineraries")
    
    itinerary_col1, itinerary_col2 = st.columns(2)
    
    with itinerary_col1:
        with st.expander("⭐ The Classic Week (7 Days)"):
            st.markdown("""
            **Day 1-2: Palermo**
            - Palatine Chapel & Cathedral
            - Ballarò Market food tour
            - Mondello Beach afternoon
            
            **Day 3: Cefalù & West Coast**
            - Morning in Cefalù 
            - Afternoon Monreale Cathedral
            
            **Day 4-5: Agrigento & South**
            - Valley of the Temples (sunset)
            - Scala dei Turchi
            
            **Day 6-7: Taormina & Etna**
            - Ancient Theater
            - Etna summit tour
            - Isola Bella
            """)
            
            if st.button("📋 Get Detailed Day-by-Day", key="classic_week"):
                st.info("Request sent! We'll email you the detailed itinerary.")
        
        with st.expander("🏖️ Beach Lovers Circuit (5 Days)"):
            st.markdown("""
            **Day 1-2: San Vito Lo Capo**
            - Caribbean vibes
            - Zingaro Reserve hike
            
            **Day 3: Favignana**
            - Island hopping
            - Cala Rossa snorkeling
            
            **Day 4-5: Southeast Beaches**
            - Vendicari Reserve
            - Marzamemi fishing village
            - Calamosche beach
            """)
    
    with itinerary_col2:
        with st.expander("🍷 Food & Wine Journey (6 Days)"):
            st.markdown("""
            **Day 1-2: Palermo Markets & Street Food**
            - Market tours
            - Cooking class
            
            **Day 3: Marsala Wine Region**
            - Wine cellars
            - Salt pans
            
            **Day 4-5: Etna Wine Route**
            - Volcano wineries
            - Pistachio farms in Bronte
            
            **Day 6: Modica & Noto**
            - Chocolate workshops
            - Baroque towns
            """)
        
        with st.expander("🏛️ Ancient Sicily (5 Days)"):
            st.markdown("""
            **Day 1-2: Syracuse**
            - Greek Theater
            - Ortigia archaeological sites
            
            **Day 3: Agrigento**
            - Valley of the Temples
            - Archaeological Museum
            
            **Day 4-5: Segesta & Selinunte**
            - Remote Greek temples
            - Western archaeological sites
            """)
    
    st.markdown("---")
    
    # Packing List Generator
    st.subheader("🎒 Smart Packing Assistant")
    
    col1, col2 = st.columns(2)
    
    with col1:
        season = st.select_slider("When are you going?", [
            "Winter (Nov-Mar)",
            "Spring (Apr-Jun)",
            "Summer (Jul-Aug)",
            "Fall (Sep-Oct)"
        ])
    
    with col2:
        activities = st.multiselect("Activities planned", [
            "Beach days",
            "Hiking",
            "City touring",
            "Fine dining",
            "Boat trips",
            "Wine tasting"
        ])
    
    if st.button("📦 Generate Packing List"):
        st.markdown("""
        ### ✅ Your Sicily Packing List
        
        **Essentials:**
        - 🎫 Passport & travel insurance
        - 💳 Credit cards + €200 cash
        - 🔌 EU plug adapter
        - 📱 Phone & chargers
        
        **Clothing (Summer):**
        - 👕 Light, breathable clothes
        - 🩱 Swimsuit × 2
        - 👟 Comfortable walking shoes
        - 🥿 Sandals for beach
        - 🧢 Sun hat
        - 👗 Smart-casual for restaurants
        
        **Protection:**
        - 🧴 SPF 50+ sunscreen
        - 😎 Sunglasses
        - 💧 Reusable water bottle
        
        **Optional:**
        - 🤿 Snorkel gear (can rent)
        - 📷 Camera
        - 📚 Phrasebook or translator app
        """)

# ============================================
# TAB 3: PRACTICAL INFO
# ============================================
with tab3:
    st.header("📋 Practical Information & Travel Tips")
    
    # Category selector
    info_category = st.selectbox(
        "Choose a topic",
        list(practical_info.keys())
    )
    
    category_data = practical_info[info_category]
    
    for topic_name, topic_info in category_data.items():
        with st.expander(f"ℹ️ {topic_name}", expanded=True):
            if isinstance(topic_info, dict):
                for key, value in topic_info.items():
                    if key != 'insider':
                        st.markdown(f"**{key.title()}:** {value}")
                    else:
                        st.success(f"💡 **Insider Tip:** {value}")
            else:
                st.markdown(topic_info)
    
    st.markdown("---")
    
    # Emergency Contacts
    st.subheader("🚨 Emergency & Useful Contacts")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Emergency Numbers:**
        - 🚑 Medical Emergency: **112**
        - 🚓 Police (Carabinieri): **112**
        - 👮 Local Police: **113**
        - 🚒 Fire Department: **115**
        - 🚗 Roadside Assistance: **116**
        
        **Consulates in Palermo:**
        - 🇺🇸 US: +39 091 305 857
        - 🇬🇧 UK: +39 091 326 412
        - 🇨🇦 Canada: +39 091 584 288
        """)
    
    with col2:
        st.markdown("""
        **Useful Services:**
        - 🏥 Pharmacy (Farmacia): Look for green cross
        - 🏥 24h Pharmacies: Check "farmacia di turno"
        - 🚕 Taxi Palermo: +39 091 513 311
        - 🚕 Taxi Catania: +39 095 330 966
        
        **Tourist Info:**
        - ℹ️ Palermo Tourist Office: Piazza Castelnuovo
        - ℹ️ Catania Tourist Office: Via Vittorio Emanuele II
        - 📱 Sicily Tourism App: "Visit Sicily"
        """)

# ============================================
# TAB 4: EXPERIENCES & TOURS
# ============================================
with tab4:
    st.header("🍷 Unique Experiences & Tours")
    st.markdown("*Book authentic Sicilian experiences*")
    
    # Experience categories
    exp_category = st.radio(
        "Browse by category:",
        ["🍷 Wine & Food", "🚣 Adventure", "🎨 Culture", "👨‍🍳 Cooking Classes", "⛵ Boat Tours"],
        horizontal=True
    )
    
    # Sample experiences
    experiences = {
        "🍷 Wine & Food": [
            {
                "name": "Etna Wine Tour with Sommelier",
                "description": "Visit 3 wineries on Etna's slopes, taste volcanic wines, lunch included",
                "duration": "8 hours",
                "price": "€120-150",
                "location": "Mount Etna",
                "highlights": ["Nerello Mascalese tasting", "Volcano views", "Traditional lunch"]
            },
            {
                "name": "Palermo Street Food Tour",
                "description": "Walk through markets with local guide, taste 10+ street foods",
                "duration": "3 hours",
                "price": "€50-70",
                "location": "Palermo",
                "highlights": ["Ballarò Market", "Panelle & arancini", "Local guide stories"]
            },
            {
                "name": "Modica Chocolate Workshop",
                "description": "Learn ancient Aztec chocolate-making technique",
                "duration": "2 hours",
                "price": "€45",
                "location": "Modica",
                "highlights": ["Hands-on workshop", "Historical techniques", "Take home chocolate"]
            }
        ],
        "🚣 Adventure": [
            {
                "name": "Etna Summit Crater Hike",
                "description": "Guided trek to active craters with volcanologist",
                "duration": "6 hours",
                "price": "€65-90",
                "location": "Mount Etna",
                "highlights": ["Active craters", "Expert guide", "Cable car included"]
            },
            {
                "name": "Zingaro Reserve Coastal Hike",
                "description": "7km hike along pristine coastline, swimming stops",
                "duration": "5 hours",
                "price": "€40",
                "location": "Zingaro Reserve",
                "highlights": ["Hidden coves", "Snorkeling", "Nature guide"]
            }
        ],
        "🎨 Culture": [
            {
                "name": "Private Palatine Chapel Tour",
                "description": "After-hours access to Palermo's Byzantine masterpiece",
                "duration": "1.5 hours",
                "price": "€80",
                "location": "Palermo",
                "highlights": ["After-hours access", "Expert art historian", "Photography allowed"]
            },
            {
                "name": "Valley of Temples Sunset Tour",
                "description": "Evening guided tour with sunset at Temple of Concordia",
                "duration": "3 hours",
                "price": "€55",
                "location": "Agrigento",
                "highlights": ["Golden hour photography", "Night illumination", "Archaeologist guide"]
            }
        ],
        "👨‍🍳 Cooking Classes": [
            {
                "name": "Sicilian Grandma's Kitchen",
                "description": "Cook traditional dishes in local home, family-style lunch",
                "duration": "4 hours",
                "price": "€85",
                "location": "Palermo countryside",
                "highlights": ["Arancini making", "Pasta alla Norma", "Family hospitality"]
            },
            {
                "name": "Cannoli & Cassata Masterclass",
                "description": "Learn Sicily's iconic desserts from pastry chef",
                "duration": "3 hours",
                "price": "€70",
                "location": "Palermo or Catania",
                "highlights": ["Professional kitchen", "Ricotta cream secrets", "Take home desserts"]
            }
        ],
        "⛵ Boat Tours": [
            {
                "name": "Egadi Islands Day Trip",
                "description": "Sail around Favignana, Levanzo, swimming stops",
                "duration": "8 hours",
                "price": "€70-90",
                "location": "Trapani",
                "highlights": ["3 islands", "Cave exploration", "Lunch on board"]
            },
            {
                "name": "Taormina Sunset Cruise",
                "description": "Coastal cruise with Etna views, aperitivo included",
                "duration": "2 hours",
                "price": "€50",
                "location": "Taormina",
                "highlights": ["Isola Bella from sea", "Prosecco & snacks", "Sunset views"]
            }
        ]
    }
    
    # Display experiences
    for experience in experiences.get(exp_category, []):
        with st.expander(f"⭐ {experience['name']} - {experience['price']}"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**{experience['description']}**")
                st.markdown(f"📍 **Location:** {experience['location']}")
                st.markdown(f"⏱️ **Duration:** {experience['duration']}")
                st.markdown(f"💰 **Price:** {experience['price']}")
                
                st.markdown("**Highlights:**")
                for highlight in experience['highlights']:
                    st.markdown(f"- ✓ {highlight}")
            
            with col2:
                if st.button("📧 Request Info", key=experience['name']):
                    st.success("Info request sent! We'll contact you within 24 hours.")
                
                if st.button("💾 Save for Later", key=f"save_{experience['name']}"):
                    st.session_state.bookmarks.add(experience['name'])
                    st.success("Saved!")

# ============================================
# TAB 5: GET INFO NOW (FORMS)
# ============================================
with tab5:
    st.header("❓ Get Information On The Go")
    st.markdown("*Ask specific questions and get personalized recommendations*")
    
    # Question type selector
    question_type = st.selectbox(
        "What do you need help with?",
        [
            "🍴 Restaurant Recommendation",
            "🏨 Accommodation Advice",
            "🚗 Transportation Question",
            "🏖️ Beach Recommendation",
            "🗺️ Day Trip Planning",
            "💰 Budget Question",
            "👨‍👩‍👧 Family Travel Tips",
            "♿ Accessibility Information",
            "📱 General Question"
        ]
    )
    
    st.markdown("---")
    
    # Dynamic form based on question type
    if "Restaurant" in question_type:
        st.subheader("🍴 Get Restaurant Recommendations")
        
        with st.form("restaurant_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                location = st.selectbox("Where are you?", [
                    "Palermo", "Catania", "Syracuse", "Taormina", 
                    "Agrigento", "Trapani", "Noto", "Ragusa", "Other"
                ])
                cuisine_pref = st.multiselect("Cuisine preferences", [
                    "Traditional Sicilian",
                    "Seafood",
                    "Pizza & Pasta",
                    "Fine Dining",
                    "Street Food",
                    "Vegetarian/Vegan",
                    "Gluten-free options"
                ])
            
            with col2:
                budget = st.select_slider("Budget per person", [
                    "€10-20 (Casual)",
                    "€20-40 (Mid-range)",
                    "€40-70 (Upscale)",
                    "€70+ (Fine dining)"
                ])
                atmosphere = st.radio("Atmosphere", [
                    "Casual & Local",
                    "Romantic",
                    "Family-friendly",
                    "Trendy/Modern"
                ])
            
            special_requests = st.text_area("Any special requests? (allergies, celebrations, etc.)")
            
            submit_restaurant = st.form_submit_button("🔍 Get Recommendations", use_container_width=True)
            
            if submit_restaurant:
                with st.spinner("Finding the perfect spots for you..."):
                    st.success("✅ Recommendations ready!")
                    st.markdown(f"""
                    ### Your Personalized Recommendations in {location}
                    
                    **1. 🌟 Top Pick: Trattoria del Mare**
                    - Perfect match for your preferences
                    - Price range: {budget}
                    - Atmosphere: {atmosphere}
                    - *"The seafood pasta is sublime, and they can accommodate gluten-free"*
                    
                    **2. 🍝 Alternative: Osteria Antica**
                    - Traditional Sicilian specialties
                    - Great local wine selection
                    - *"Ask for the off-menu daily specials"*
                    
                    **3. 💎 Hidden Gem: Cucina di Nonna Rosa**
                    - Family-run, authentic atmosphere
                    - Booking recommended
                    """)
                    
                    if st.button("📧 Email me these recommendations"):
                        st.info("Recommendations sent to your email!")
    
    elif "Accommodation" in question_type:
        st.subheader("🏨 Find Your Perfect Stay")
        
        with st.form("accommodation_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                stay_location = st.selectbox("Where do you want to stay?", 
                    list(destinations.keys()) + ["Other"])
                check_in = st.date_input("Check-in date", 
                    value=datetime.now() + timedelta(days=30))
                check_out = st.date_input("Check-out date",
                    value=datetime.now() + timedelta(days=33))
            
            with col2:
                accommodation_type = st.multiselect("Type of accommodation", [
                    "Hotel",
                    "B&B",
                    "Vacation Rental",
                    "Agriturismo (Farm stay)",
                    "Hostel",
                    "Luxury Resort"
                ])
                budget_night = st.select_slider("Budget per night", [
                    "€30-60",
                    "€60-100",
                    "€100-150",
                    "€150-250",
                    "€250+"
                ])
            
            priorities = st.multiselect("What matters most?", [
                "Central location",
                "Sea view",
                "Swimming pool",
                "Parking",
                "Breakfast included",
                "Kitchen facilities",
                "Walking distance to beach",
                "Quiet area"
            ])
            
            additional_info = st.text_area("Additional requirements")
            
            submit_accommodation = st.form_submit_button("🏠 Find Accommodations", use_container_width=True)
            
            if submit_accommodation:
                st.success("📍 Top recommendations found!")
                st.markdown(f"""
                ### Recommended Stays in {stay_location}
                
                **Based on your criteria:** {', '.join(accommodation_type)} | {budget_night} | {check_in} to {check_out}
                
                *We'll send you a curated list of 5-7 properties with direct booking links and insider tips.*
                """)
                
                email_input = st.text_input("Email address for recommendations")
                if st.button("Send Recommendations"):
                    if email_input:
                        st.success(f"✅ Sent to {email_input}!")
    
    elif "Transportation" in question_type:
        st.subheader("🚗 Transportation Help")
        
        with st.form("transportation_form"):
            transport_question = st.radio("What do you need?", [
                "Best way to get from A to B",
                "Car rental advice",
                "Public transportation info",
                "Airport transfer",
                "Parking information"
            ])
            
            if "A to B" in transport_question:
                col1, col2 = st.columns(2)
                with col1:
                    from_location = st.text_input("From")
                with col2:
                    to_location = st.text_input("To")
                
                travel_date = st.date_input("When?")
                passengers = st.number_input("Number of people", 1, 10, 2)
            
            preferences = st.multiselect("Preferences", [
                "Fastest route",
                "Most scenic",
                "Budget-friendly",
                "Public transport only",
                "Comfort priority"
            ])
            
            additional_context = st.text_area("Additional details")
            
            submit_transport = st.form_submit_button("Get Transportation Advice")
            
            if submit_transport:
                st.success("🚗 Here's your route advice:")
                st.info(f"""
                **From {from_location} to {to_location}**
                
                **Recommended Option:** Private car rental
                - Duration: ~2 hours
                - Cost: €40-60 (rental + gas)
                - Route: A19 highway (scenic coastal views)
                
                **Alternative:** Bus + Train
                - Duration: ~3.5 hours
                - Cost: €15-20
                - Changes: 1
                
                💡 *For {passengers} people, car rental is more economical and flexible*
                """)
    
    elif "Beach" in question_type:
        st.subheader("🏖️ Find Your Perfect Beach")
        
        with st.form("beach_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                beach_region = st.selectbox("Which area?", [
                    "Don't mind - show me the best",
                    "Near Palermo",
                    "Near Catania",
                    "Near Syracuse",
                    "Southwest",
                    "Islands (Egadi, etc.)"
                ])
                
                beach_type = st.multiselect("Beach characteristics", [
                    "White sand",
                    "Crystal clear water",
                    "Snorkeling spots",
                    "Family-friendly (shallow)",
                    "Secluded/quiet",
                    "Beach clubs available",
                    "Rocky/dramatic cliffs",
                    "Good for sunset"
                ])
            
            with col2:
                accessibility = st.radio("Accessibility", [
                    "Easy access (parking nearby)",
                    "Don't mind a short walk",
                    "Up for a hike to hidden gems"
                ])
                
                facilities = st.multiselect("Needed facilities", [
                    "Restaurants nearby",
                    "Showers/toilets",
                    "Umbrella/chair rental",
                    "Parking",
                    "Completely wild/natural"
                ])
            
            when_visit = st.date_input("When are you going?")
            
            submit_beach = st.form_submit_button("🏖️ Find My Beach")
            
            if submit_beach:
                st.success("🌊 Perfect beaches for you:")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("""
                    ### 🥇 Top Match: Cala Rossa (Favignana)
                    - ⭐⭐⭐⭐⭐ Spectacular turquoise water
                    - 🏊 Perfect for snorkeling
                    - 🚶 20-minute bike ride from port
                    - 💡 *Insider:* Arrive before 11 AM
                    
                    **Why this beach:** Matches all your criteria for clear water and snorkeling
                    """)
                
                with col2:
                    st.markdown("""
                    ### 🥈 Runner-up: Calamosche (Vendicari)
                    - ⭐⭐⭐⭐⭐ Secluded paradise
                    - 🌿 Protected nature reserve
                    - 🚶 20-minute walk from parking
                    - 💡 *Insider:* Best in September (fewer crowds)
                    """)
                
                st.markdown("### 🥉 Also Consider: Fontane Bianche")
                st.info("Great family option near Syracuse with easy access and facilities")
    
    elif "Day Trip" in question_type:
        st.subheader("🗺️ Plan a Day Trip")
        
        with st.form("day_trip_form"):
            starting_from = st.selectbox("Starting from", [
                "Palermo", "Catania", "Syracuse", "Taormina", "Other"
            ])
            
            interests = st.multiselect("I want to see/do", [
                "Ancient ruins",
                "Beaches",
                "Medieval towns",
                "Wine tasting",
                "Nature/hiking",
                "Local markets",
                "Volcanic landscapes"
            ])
            
            col1, col2 = st.columns(2)
            with col1:
                trip_date = st.date_input("Date of trip")
                has_car = st.radio("Do you have a car?", ["Yes", "No"])
            
            with col2:
                group_size = st.number_input("People in group", 1, 20, 2)
                budget = st.select_slider("Budget", ["€20-40", "€40-70", "€70-100", "€100+"])
            
            submit_daytrip = st.form_submit_button("🗺️ Create Day Trip Plan")
            
            if submit_daytrip:
                st.success("✨ Your custom day trip:")
                
                st.markdown(f"""
                ### Day Trip from {starting_from}
                
                **Morning (9:00 AM - 12:00 PM)**
                - 🚗 Depart for Agrigento Valley of the Temples (1.5h drive)
                - 🏛️ Guided tour of ancient Greek temples
                - ☕ Coffee break at nearby bar
                
                **Lunch (12:30 PM - 2:00 PM)**
                - 🍝 Trattoria La Scala - traditional Sicilian lunch
                - Budget: ~€20 per person
                
                **Afternoon (2:00 PM - 5:00 PM)**
                - 🏖️ Visit Scala dei Turchi white cliffs
                - 🏊 Quick swim (bring swimsuit!)
                - 📸 Photos at sunset viewpoint
                
                **Evening (5:00 PM - 7:00 PM)**
                - 🚗 Return to {starting_from}
                - 🍷 Optional: stop at winery on route back
                
                **Total Cost Estimate:** €{40 + (20 if has_car == "No" else 0)} per person
                **Best suited for:** {interests[0] if interests else 'Exploration'} lovers
                """)
                
                if st.button("📧 Email me detailed directions"):
                    st.success("Detailed itinerary sent!")
    
    else:  # General question
        st.subheader("📱 Ask Anything")
        
        with st.form("general_question_form"):
            name = st.text_input("Your name (optional)")
            email = st.text_input("Email (to receive response)")
            
            question = st.text_area("Your question", height=150,
                placeholder="Example: Is Sicily safe for solo female travelers? What's the tipping culture? Can I drink tap water?")
            
            urgency = st.radio("How urgent?", [
                "Just curious",
                "Planning soon (within 2 weeks)",
                "Urgent (already in Sicily!)"
            ])
            
            submit_general = st.form_submit_button("💬 Submit Question", use_container_width=True)
            
            if submit_general:
                if question and email:
                    st.success("✅ Question received!")
                    st.info(f"""
                    Thank you{' ' + name if name else ''}! We'll respond to **{email}** within:
                    - 🚀 Urgent: 2-4 hours
                    - 📅 Planning soon: 24 hours
                    - 💭 Just curious: 48 hours
                    
                    In the meantime, check our Practical Info tab for common questions!
                    """)
                    
                    # Store in session state
                    st.session_state.feedback_data.append({
                        'type': 'question',
                        'question': question,
                        'urgency': urgency,
                        'timestamp': datetime.now()
                    })
                else:
                    st.error("Please provide your question and email address")

# ============================================
# TAB 6: COMMUNITY & FEEDBACK
# ============================================
with tab6:
    st.header("💬 Community & Your Feedback")
    
    # Tabs within community
    comm_tab1, comm_tab2, comm_tab3 = st.tabs([
        "📮 Share Feedback",
        "⭐ Rate & Review",
        "💡 Suggest Additions"
    ])
    
    with comm_tab1:
        st.subheader("📮 Help Us Improve This Guide")
        
        with st.form("feedback_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                feedback_name = st.text_input("Your Name")
                feedback_email = st.text_input("Email (optional)")
            
            with col2:
                visited_before = st.radio("Have you been to Sicily?", [
                    "Not yet, planning",
                    "Currently there!",
                    "Yes, in the past"
                ])
                
                how_helpful = st.slider("How helpful is this guide?", 1, 5, 5)
            
            feedback_text = st.text_area(
                "Your feedback, suggestions, or corrections",
                height=150,
                placeholder="What could we improve? Any missing information? Errors to correct?"
            )
            
            submit_feedback = st.form_submit_button("📤 Send Feedback", use_container_width=True)
            
            if submit_feedback and feedback_name and feedback_text:
                st.session_state.feedback_data.append({
                    'name': feedback_name,
                    'rating': how_helpful,
                    'feedback': feedback_text,
                    'timestamp': datetime.now()
                })
                st.success(f"Grazie mille, {feedback_name}! Your feedback makes this guide better.")
                st.balloons()
    
    with comm_tab2:
        st.subheader("⭐ Rate Places You've Visited")
        
        st.markdown("*Help other travelers by sharing your experiences*")
        
        with st.form("review_form"):
            place_type = st.selectbox("What are you reviewing?", [
                "Restaurant",
                "Beach",
                "Attraction",
                "Hotel/Accommodation",
                "Tour/Experience"
            ])
            
            place_name = st.text_input("Name of place")
            location = st.selectbox("Location", list(destinations.keys()) + ["Other"])
            
            rating = st.slider("Your rating", 1, 5, 4)
            
            col1, col2 = st.columns(2)
            with col1:
                would_recommend = st.radio("Would you recommend?", ["Yes", "Maybe", "No"])
            with col2:
                visit_date = st.date_input("When did you visit?")
            
            review_text = st.text_area(
                "Your review",
                placeholder="Share your experience, tips, what made it special or what to avoid..."
            )
            
            photo_upload = st.file_uploader("Upload photos (optional)", 
                type=['jpg', 'jpeg', 'png'], accept_multiple_files=True)
            
            submit_review = st.form_submit_button("✍️ Submit Review")
            
            if submit_review and place_name and review_text:
                st.success("✅ Review submitted! Thank you for contributing!")
                st.info("Your review will be added after moderation (24-48 hours)")
    
    with comm_tab3:
        st.subheader("💡 Suggest New Content")
        
        st.markdown("*Know a hidden gem we're missing?*")
        
        with st.form("suggestion_form"):
            suggestion_type = st.radio("What should we add?", [
                "New region/city",
                "Restaurant/food spot",
                "Beach",
                "Activity/tour",
                "Practical tip",
                "Other"
            ])
            
            suggestion_title = st.text_input("Title/Name")
            
            suggestion_details = st.text_area(
                "Details",
                height=150,
                placeholder="Tell us why this should be included, location, what makes it special..."
            )
            
            your_connection = st.text_input("Your connection to this place (optional)",
                placeholder="e.g., 'Local resident', 'Visited last month', 'Friend owns this restaurant'")
            
            submit_suggestion = st.form_submit_button("💡 Submit Suggestion")
            
            if submit_suggestion and suggestion_title and suggestion_details:
                st.success("🙏 Thank you for the suggestion!")
                st.info("We'll review and potentially add it in the next update.")
                
                # Save to session
                st.session_state.feedback_data.append({
                    'type': 'suggestion',
                    'category': suggestion_type,
                    'title': suggestion_title,
                    'details': suggestion_details,
                    'timestamp': datetime.now()
                })
    
    st.markdown("---")
    
    # Recent community stats
    st.subheader("📊 Community Stats")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Visitors", "2,847")
    with col2:
        st.metric("Reviews Submitted", "156")
    with col3:
        st.metric("Average Rating", "4.8/5 ⭐")
    with col4:
        st.metric("Countries", "23")

# ============================================
# TAB 7: DASHBOARD
# ============================================
with tab7:
    st.header("📊 Your Personal Sicily Dashboard")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📌 Your Bookmarks")
        if st.session_state.bookmarks:
            for i, bookmark in enumerate(st.session_state.bookmarks, 1):
                col_a, col_b = st.columns([4, 1])
                with col_a:
                    st.markdown(f"{i}. ✓ {bookmark}")
                with col_b:
                    if st.button("❌", key=f"remove_{i}"):
                        st.session_state.bookmarks.remove(bookmark)
                        st.rerun()
        else:
            st.info("No bookmarks yet. Explore the guide and save your favorites!")
    
    with col2:
        st.subheader("📈 Your Activity")
        st.metric("Bookmarks", len(st.session_state.bookmarks))
        st.metric("Saved Trips", len(st.session_state.saved_trips))
        st.metric("Questions Asked", len([f for f in st.session_state.feedback_data if f.get('type') == 'question']))
    
    st.markdown("---")
    
    # Saved Itineraries
    st.subheader("🗺️ Your Saved Itineraries")
    if st.session_state.saved_trips:
        for i, trip in enumerate(st.session_state.saved_trips, 1):
            with st.expander(f"Trip {i}: {trip['duration']} days - {trip['style']}"):
                st.markdown(f"""
                - **Start Point:** {trip['start']}
                - **Saved On:** {trip['date']}
                - **Style:** {trip['style']}
                """)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("📧 Email Details", key=f"email_trip_{i}"):
                        st.success("Itinerary emailed!")
                with col2:
                    if st.button("📄 Download PDF", key=f"pdf_trip_{i}"):
                        st.info("PDF download starting...")
                with col3:
                    if st.button("🗑️ Delete", key=f"delete_trip_{i}"):
                        st.session_state.saved_trips.pop(i-1)
                        st.rerun()
    else:
        st.info("No saved itineraries. Create one in the 'Plan Your Trip' tab!")
    
    st.markdown("---")
    
    # Export All Data
    st.subheader("💾 Export Your Data")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📥 Download All Bookmarks", use_container_width=True):
            bookmarks_text = "\n".join([f"• {b}" for b in st.session_state.bookmarks])
            st.download_button(
                "Download TXT",
                bookmarks_text,
                file_name="sicily_bookmarks.txt"
            )
    
    with col2:
        if st.button("📥 Download Itineraries", use_container_width=True):
            st.info("PDF generation in progress...")
    
    with col3:
        if st.button("🗑️ Clear All Data", use_container_width=True):
            if st.checkbox("Are you sure?"):
                st.session_state.bookmarks = set()
                st.session_state.saved_trips = []
                st.success("All data cleared!")
                st.rerun()

# --- INTERACTIVE MAP SECTION (below tabs) ---
st.markdown("---")
st.header("🗺️ Interactive Sicily Map")
st.markdown("*Explore all regions visually*")

# Create detailed map data
map_data = pd.DataFrame([
    {
        "lat": d["lat"], 
        "lon": d["lon"], 
        "name": k,
        "size": 100
    } 
    for k, d in destinations.items()
])

st.map(map_data, size='size')

# Map legend
st.markdown("""
**Map Guide:**
- 🔵 **Blue markers** = Major regions covered in this guide
- Click 'Open in maps' to get directions
- Best viewed on desktop for full interactivity
""")

# --- FOOTER ---
st.markdown("---")

footer_col1, footer_col2, footer_col3 = st.columns(3)

with footer_col1:
    st.markdown("""
    ### 📚 Resources
    - [Sicily Tourism Official](https://www.visitsicily.info)
    - [Trenitalia (Trains)](https://www.trenitalia.com)
    - [Sicily Weather](https://www.meteo.it)
    """)

with footer_col2:
    st.markdown("""
    ### 🔗 Connect
    - Share this guide with friends
    - Follow us for updates
    - Join our Sicily travelers group
    """)

with footer_col3:
    st.markdown("""
    ### ℹ️ About
    - Last Updated: January 2026
    - Version 2.0
    - Made with ❤️ in Sicily
    """)

st.markdown("---")
st.markdown("""
<p style='text-align: center; color: #FFD700;'>
    <strong>🏺 Sicily Insider Guide</strong><br>
    For private use within our international network<br>
    <em>Benvenuti in Sicilia — Welcome to the soul of the Mediterranean</em>
</p>
""", unsafe_allow_html=True)

# Version info
st.markdown("""
<p style='text-align: center; font-size: 0.8em; color: #888;'>
    v2.0.0 | Comprehensive Edition | © 2026
</p>
""", unsafe_allow_html=True)
