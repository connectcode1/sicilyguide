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

# --- CSS STYLING ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700;800&family=Lato:wght@300;400;700&display=swap');
    
    .stApp { background-color: #FFFFFF; color: #2C2C2C; font-family: 'Lato', sans-serif; }
    
    /* Elegant Content Cards */
    .content-card {
        background: #FFFFFF; padding: 50px; border-top: 6px solid #D4A574;
        margin: 40px 0; box-shadow: 0 4px 20px rgba(0,0,0,0.08); position: relative;
    }
    .content-card::after {
        content: ''; position: absolute; bottom: 0; left: 0; right: 0; height: 2px;
        background: linear-gradient(90deg, #C85A54 0%, #D4A574 50%, #C85A54 100%);
    }
    
    /* Typography */
    h1 { font-family: 'Playfair Display', serif !important; color: #2C2C2C !important; font-size: 3.5em !important; }
    h2 { font-family: 'Playfair Display', serif !important; color: #C85A54 !important; font-size: 2.2em !important; margin-top: 40px !important; }
    h3 { font-family: 'Playfair Display', serif !important; color: #5B8C85 !important; }
    h4 { font-family: 'Lato', sans-serif !important; text-transform: uppercase !important; letter-spacing: 2px !important; }
    p { font-family: 'Lato', sans-serif; font-size: 1.05em; line-height: 1.8; color: #4A4A4A; }
    
    /* Feature & Itinerary Cards */
    .feature-card {
        background: linear-gradient(135deg, #F8F6F2 0%, #FFFFFF 100%);
        border: 1px solid #E8E4DC; border-left: 4px solid #5B8C85;
        padding: 30px; margin: 20px 0; transition: all 0.3s ease;
    }
    .feature-card:hover { transform: translateY(-2px); box-shadow: 0 8px 30px rgba(91, 140, 133, 0.15); }
    
    .itinerary-stop {
        background: #FFF; border: 1px solid #E8E4DC; border-left: 6px solid #C85A54;
        padding: 25px; margin-bottom: 20px;
    }
    
    /* Sidebar & UI Elements */
    section[data-testid="stSidebar"] { background: #F8F6F2; border-right: 1px solid #E8E4DC; }
    .stButton>button { background: #C85A54; color: #FFFFFF; border: none; padding: 15px 40px; letter-spacing: 1.5px; text-transform: uppercase; }
    .stButton>button:hover { background: #B34A44; }
    .insider-quote { border-left: 4px solid #D4A574; padding: 25px; background: #F8F6F2; font-style: italic; margin: 30px 0; }
    
    /* Hero & Footer */
    .hero-section { text-align: center; padding: 80px 20px; background: linear-gradient(180deg, #FFFFFF 0%, #F8F6F2 100%); border-bottom: 1px solid #E8E4DC; }
    .footer { background: #F8F6F2; padding: 60px 40px; margin-top: 80px; border-top: 1px solid #E8E4DC; }
    </style>
    """, unsafe_allow_html=True)

# --- EXPANDED DESTINATIONS DATA WITH TAGS ---
destinations = {
    "Palermo & Western Sicily": {
        "tagline": "Where Arab Domes Meet Norman Grandeur",
        "tags": ["Culture", "Street Food", "History", "Beaches"],
        "description": """Palermo is a city of contradictions and unexpected beauty, a place where the air hangs heavy with the scent of jasmine and fried chickpea fritters. To walk its streets is to read a history book written in stone: Byzantine mosaics shimmer inside Norman chapels, while red-domed Arab churches sit comfortably beside flamboyant Baroque palaces. It is a city that doesn't just ask for your attention; it demands it with a chaotic, vibrant energy that is utterly unique in Europe.
        
        Head west, and the noise of the capital fades into the stillness of the salt pans of Trapani, where windmills silhouette against blazing sunsets. The medieval hilltop town of Erice floats above the clouds like a dream, offering almond pastries and ancient cobbled streets. The coast here is wilder, home to the pristine Riserva dello Zingaro and the translucent waters of San Vito Lo Capo. This region is Sicily at its most authentic—unpolished, deeply historical, and fiercely proud.""",
        "insider_tip": "Visit the Palatine Chapel at 9 AM to see the mosaics light up, then head immediately to Ballarò Market for a panelle sandwich.",
        "must_visit": ["Palatine Chapel", "Ballarò Market", "Erice", "Segesta Temple"],
        "lat": 38.1157, "lon": 13.3615, "days": "4-5 days"
    },
    "Taormina, Messina & The Northeast": {
        "tagline": "The Dolce Vita Terrace Overlooking the Sea",
        "tags": ["Luxury", "Views", "Romance", "Beaches"],
        "description": """There is a reason writers and artists have flocked to Taormina for centuries. Perched precariously on a cliffside, it offers perhaps the most dramatic view in all of Italy: the crumbling columns of an ancient Greek theater framing the smoking cone of Mount Etna and the turquoise Ionian Sea below. The town itself is a manicured jewel box of high-end boutiques, hidden gardens, and piazzas that turn into open-air living rooms at aperitivo hour.
        
        But the northeast is more than just Taormina's glitz. Just above lies the medieval village of Castelmola, famous for its almond wine and eagle-eye panoramas. Down on the coast, the Isola Bella nature reserve offers snorkeling in crystal-clear water. To the north, Messina guards the straits, a city of resilience and maritime history. This region blends the sophisticated 'Dolce Vita' lifestyle with breathtaking natural drama.""",
        "insider_tip": "Skip the main street of Taormina at midday. Instead, take the cable car down to Mazzarò and boat to the Blue Grotto before the crowds arrive.",
        "must_visit": ["Greek Theater", "Isola Bella", "Castelmola", "Savoca (Godfather tour)"],
        "lat": 37.8526, "lon": 15.2876, "days": "3-4 days"
    },
    "Aeolian Islands": {
        "tagline": "Seven Volcanic Sisters in the Deep Blue",
        "tags": ["Islands", "Nature", "Volcanoes", "Boating", "Relaxation"],
        "description": """Rising from the cobalt Tyrrhenian Sea like dark pyramids, the Aeolian Islands feel like a world apart. UNESCO-protected and fiercely beautiful, each of the seven islands has a distinct soul. Stromboli is the wild child, a continuously active volcano where you can watch lava fireworks against the night sky. Panarea is the chic retreat, a whitewashed maze of bougainvillea and luxury villas where cars are banned and time slows down.
        
        Salina, the greenest island, is a paradise of caper bushes and Malvasia vineyards climbing up extinct volcanic cones. Lipari offers history and life, while remote Alicudi offers total silence. The magic here is elemental: black sand beaches, thermal mud baths, and the sensation of being small in the face of nature's power. It is the ultimate escape for those seeking to disconnect from the modern world.""",
        "insider_tip": "Rent a private boat on Salina. It’s the only way to find the hidden cove of Pollara, made famous by the film 'Il Postino'.",
        "must_visit": ["Stromboli Night Boat", "Pollara Beach", "Vulcano Mud Baths", "Panarea Prehistoric Village"],
        "lat": 38.5667, "lon": 14.9564, "days": "5-7 days"
    },
    "Catania, Etna & The East": {
        "tagline": "Fire, Lava Stone, and Barque Energy",
        "tags": ["Volcanoes", "Wine", "Food", "City"],
        "description": """Catania is the city of the volcano. Built from the very lava that has destroyed it multiple times, it is a city of black and white—buildings of dark volcanic stone framed by white limestone trim. It is grittier than Palermo but arguably more alive, with a fish market that screams with the energy of a Souk and a nightlife scene that pulses until dawn.
        
        Looming over everything is 'Mamma Etna.' Europe's highest active volcano is not just a backdrop; it is a presence. Its slopes are home to some of the world's most exciting wine production, where ancient vines struggle through mineral-rich ash to produce reds of incredible depth. Visiting this region means embracing the power of the earth, from trekking the crater rim to tasting pistachios grown in lava soil.""",
        "insider_tip": "Don't just look at Etna; drink it. Book a tasting at a winery in Passopisciaro to taste the 'Nerello Mascalese' grown on volcanic terraces.",
        "must_visit": ["Mount Etna Summit", "Catania Fish Market", "Benedictine Monastery", "Etna Wineries"],
        "lat": 37.5079, "lon": 15.0830, "days": "3-4 days"
    },
    "Syracuse & The Baroque Southeast": {
        "tagline": "Greek Myths and Golden Stone",
        "tags": ["History", "Architecture", "Baroque", "Culture"],
        "description": """If you want to understand the ancient world, come to Syracuse. Once the rival of Athens, its archaeological park holds vast Greek theaters and Roman amphitheaters. But the true heart is the island of Ortigia, a labyrinth of narrow streets that opens onto a cathedral built literally around an ancient Greek temple.
        
        Travel inland to the Val di Noto, and the scenery changes to rolling hills and deep gorges. Here, the towns of Noto, Modica, and Ragusa Ibla cling to the hillsides in a riot of Baroque splendor. Rebuilt after a massive earthquake in 1693, they glow with a honey-colored limestone that turns gold at sunset. This is a region of intellect, elegance, and chocolate—Modica still makes it using an ancient Aztec recipe brought by the Spanish.""",
        "insider_tip": "In Ortigia, swim off the rocks at the Forte Vigliena at sunset, then walk to Piazza Duomo to see the cathedral lit up against the night sky.",
        "must_visit": ["Ortigia Island", "Neapolis Park", "Noto Cathedral", "Modica Chocolate Shop"],
        "lat": 37.0755, "lon": 15.2866, "days": "4-5 days"
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

# --- CLEANED SIDEBAR ---
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

# --- MAIN TABS (NO DASHBOARD) ---
tab1, tab2, tab3, tab4 = st.tabs(["EXPLORE REGIONS", "PLAN YOUR TRIP", "INSIDER TIPS", "COMMUNITY"])

# ============================================
# TAB 1: EXPLORE REGIONS
# ============================================
with tab1:
    st.markdown("## Discover by Region")
    selected_region = st.selectbox("Select a region to explore", list(destinations.keys()))
    region = destinations[selected_region]
    
    st.markdown(f"""
        <div class="content-card">
            <h2 style="margin-top:0;">{selected_region}</h2>
            <h4 style="color:#5B8C85;">{region['tagline']}</h4>
            <p style="margin-top:20px;">{region['description']}</p>
        </div>
    """, unsafe_allow_html=True)
    
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
        st.write("**Best For:** " + ", ".join(region['tags']))
        st.write(f"**Must See:** {', '.join(region['must_visit'][:2])}")

# ============================================
# TAB 2: INSTANT ITINERARY GENERATOR
# ============================================
with tab2:
    st.markdown("""
        <div class="section-header">
            <h2>Instant Itinerary Generator</h2>
            <p>Select your interests, and we will build a custom route for you instantly.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Input Section
    with st.container():
        col1, col2 = st.columns([1, 2])
        with col1:
            days = st.slider("Trip Duration (Days)", 3, 14, 7)
            pace = st.radio("Travel Pace", ["Relaxed", "Moderate", "Fast-Paced"])
        with col2:
            all_interests = ["History", "Food", "Beaches", "Volcanoes", "Luxury", "Nature", "Wine"]
            user_interests = st.multiselect("What are you interested in?", all_interests, default=["Food", "Beaches"])
    
    st.markdown("---")
    
    # Generator Logic
    if user_interests:
        st.subheader(f"Your {days}-Day Custom Journey")
        
        # Scoring Logic
        scored_regions = []
        for name, data in destinations.items():
            score = 0
            # Calculate match score based on tags
            for interest in user_interests:
                if interest in data['tags']:
                    score += 1
            if score > 0:
                scored_regions.append((name, score, data))
        
        # Sort by score
        scored_regions.sort(key=lambda x: x[1], reverse=True)
        
        # If no matches, fallback
        if not scored_regions:
            st.warning("No perfect matches found. Try selecting different interests (e.g., History or Food).")
        else:
            # Display the Route
            for i, (r_name, r_score, r_data) in enumerate(scored_regions[:3]): # Limit to top 3 regions
                st.markdown(f"""
                    <div class="itinerary-stop">
                        <h3 style="margin-top:0; color:#C85A54;">Stop {i+1}: {r_name}</h3>
                        <p><strong>Why this fits you:</strong> Matches your interest in {', '.join([t for t in user_interests if t in r_data['tags']])}.</p>
                        <p>{r_data['tagline']}</p>
                        <p><strong>Highlight:</strong> {r_data['must_visit'][0]}</p>
                    </div>
                """, unsafe_allow_html=True)
            
            # Summary
            st.info(f"💡 **Trip Logic:** Based on a {pace.lower()} pace, we recommend spending {int(days/len(scored_regions[:3]))} days in each location.")
            
    else:
        st.info("👈 Please select at least one interest to generate your itinerary.")

# ============================================
# TAB 3: INSIDER TIPS (Simplified)
# ============================================
with tab3:
    st.markdown("## Essential Travel Wisdom")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h4>Getting Around</h4>
            <p><strong>Car Rental:</strong> Essential for exploring the coasts and countryside. Book an automatic in advance.</p>
            <p><strong>Trains:</strong> Good for connecting Palermo, Messina, and Syracuse.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h4>Dining Etiquette</h4>
            <p><strong>Coperto:</strong> A €2-3 cover charge per person is standard.</p>
            <p><strong>Tipping:</strong> Not mandatory, but rounding up the bill is appreciated.</p>
        </div>
        """, unsafe_allow_html=True)

# ============================================
# TAB 4: COMMUNITY (Simplified - No Dashboard link)
# ============================================
with tab4:
    st.markdown("## Community Reviews")
    st.write("Recent highlights from our travelers.")
    
    reviews = [
        {"user": "Sarah J.", "place": "Bar Vitelli, Savoca", "text": "Touristy but worth it for the lemon granita!"},
        {"user": "Mark D.", "place": "Riserva dello Zingaro", "text": "The hike was tough in July, but the swim was magical."}
    ]
    
    for review in reviews:
        st.markdown(f"""
            <div style="background:#F9F9F9; padding:20px; margin-bottom:10px; border-left:3px solid #D4A574;">
                <strong>{review['place']}</strong><br>
                <span style="font-style:italic;">"{review['text']}"</span><br>
                <small>- {review['user']}</small>
            </div>
        """, unsafe_allow_html=True)

# --- MAP ---
st.markdown("---")
map_data = pd.DataFrame([{"lat": d["lat"], "lon": d["lon"], "name": k} for k, d in destinations.items()])
st.map(map_data)

# --- FOOTER ---
st.markdown("""
    <div class="footer">
        <div style="text-align: center;">
            <p style="font-size: 0.9em; color: #6A6A6A;">
                © 2026 Sicily Insider Guide • Curated by Locals
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
