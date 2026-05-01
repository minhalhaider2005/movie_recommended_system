import streamlit as st
import pickle
import pandas as pd
import requests

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CineMatch – Movie Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Root Variables ── */
:root {
    --gold: #F5C518;
    --gold-dim: #c9a227;
    --bg-deep: #0a0a0f;
    --bg-card: #13131a;
    --bg-card2: #1a1a24;
    --text-primary: #f0ece4;
    --text-muted: #8a8698;
    --accent: #e63946;
    --radius: 14px;
}

/* ── Global ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg-deep) !important;
    color: var(--text-primary) !important;
}

.stApp {
    background: radial-gradient(ellipse at top left, #1a1230 0%, #0a0a0f 55%),
                radial-gradient(ellipse at bottom right, #12101f 0%, #0a0a0f 60%);
    background-attachment: fixed;
}

/* ── Hide Streamlit branding ── */
#MainMenu, footer, header { visibility: hidden; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg-deep); }
::-webkit-scrollbar-thumb { background: #3a3a52; border-radius: 3px; }

/* ── Hero Header ── */
.hero-header {
    text-align: center;
    padding: 3rem 1rem 1.5rem;
    position: relative;
}
.hero-badge {
    display: inline-block;
    background: rgba(245,197,24,0.12);
    border: 1px solid rgba(245,197,24,0.3);
    color: var(--gold);
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 3px;
    text-transform: uppercase;
    padding: 5px 16px;
    border-radius: 50px;
    margin-bottom: 1rem;
}
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(2.5rem, 5vw, 4.5rem);
    font-weight: 900;
    letter-spacing: -1px;
    line-height: 1.05;
    margin: 0 0 0.5rem;
    background: linear-gradient(135deg, #f0ece4 30%, var(--gold) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    color: var(--text-muted);
    font-size: 1rem;
    font-weight: 300;
    letter-spacing: 0.5px;
}
.hero-divider {
    width: 60px;
    height: 3px;
    background: linear-gradient(90deg, var(--gold), var(--accent));
    margin: 1.5rem auto 0;
    border-radius: 2px;
}

/* ── Search Section ── */
.search-container {
    background: var(--bg-card);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: var(--radius);
    padding: 2rem 2.5rem;
    margin: 1.5rem 0;
    box-shadow: 0 8px 40px rgba(0,0,0,0.4);
}
.search-label {
    font-size: 0.72rem;
    font-weight: 500;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: var(--gold);
    margin-bottom: 0.6rem;
}

/* ── Streamlit Selectbox ── */
.stSelectbox > div > div {
    background: #1f1f2e !important;
    border: 1px solid rgba(245,197,24,0.25) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
    font-size: 1rem !important;
}
.stSelectbox > div > div:hover {
    border-color: var(--gold) !important;
    box-shadow: 0 0 0 2px rgba(245,197,24,0.15) !important;
}

/* ── Button ── */
.stButton > button {
    background: linear-gradient(135deg, var(--gold) 0%, #e6a817 100%) !important;
    color: #0a0a0f !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.5px !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.65rem 2.5rem !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 4px 20px rgba(245,197,24,0.3) !important;
    width: 100% !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(245,197,24,0.45) !important;
}
.stButton > button:active { transform: translateY(0px) !important; }

/* ── Section Heading ── */
.section-heading {
    font-family: 'Playfair Display', serif;
    font-size: 1.6rem;
    font-weight: 700;
    color: var(--text-primary);
    margin: 2.5rem 0 1.2rem;
    display: flex;
    align-items: center;
    gap: 0.6rem;
}
.section-heading span {
    color: var(--gold);
}

/* ── Movie Card ── */
.movie-card {
    background: var(--bg-card);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: var(--radius);
    overflow: hidden;
    transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
    cursor: pointer;
    height: 100%;
}
.movie-card:hover {
    transform: translateY(-6px) scale(1.01);
    box-shadow: 0 20px 50px rgba(0,0,0,0.6), 0 0 0 1px rgba(245,197,24,0.2);
    border-color: rgba(245,197,24,0.25);
}
.movie-card img {
    width: 100%;
    aspect-ratio: 2/3;
    object-fit: cover;
    display: block;
}
.movie-card-body {
    padding: 0.9rem 1rem 1rem;
}
.movie-card-title {
    font-family: 'Playfair Display', serif;
    font-size: 0.95rem;
    font-weight: 700;
    color: var(--text-primary);
    margin: 0 0 0.3rem;
    line-height: 1.3;
}
.movie-card-rank {
    font-size: 0.72rem;
    color: var(--gold);
    font-weight: 500;
    letter-spacing: 1px;
    text-transform: uppercase;
}

/* ── Rating Stars ── */
.star-rating {
    color: var(--gold);
    font-size: 0.8rem;
    letter-spacing: 2px;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--bg-card) !important;
    border-right: 1px solid rgba(255,255,255,0.06) !important;
}
[data-testid="stSidebar"] * {
    color: var(--text-primary) !important;
}

/* ── Stats Strip ── */
.stats-strip {
    display: flex;
    gap: 1rem;
    margin: 1rem 0 1.5rem;
}
.stat-pill {
    background: var(--bg-card2);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 50px;
    padding: 0.4rem 1rem;
    font-size: 0.78rem;
    color: var(--text-muted);
}
.stat-pill b { color: var(--gold); }

/* ── Info Chips ── */
.info-chip {
    display: inline-block;
    background: rgba(245,197,24,0.1);
    border: 1px solid rgba(245,197,24,0.2);
    color: var(--gold);
    border-radius: 50px;
    padding: 3px 12px;
    font-size: 0.72rem;
    font-weight: 500;
    margin: 2px;
}

/* ── Divider ── */
.fancy-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(245,197,24,0.3), transparent);
    margin: 1.5rem 0;
}

/* ── Loader ── */
.loading-text {
    text-align: center;
    color: var(--text-muted);
    font-size: 0.9rem;
    padding: 2rem;
    animation: pulse 1.5s ease-in-out infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 0.5; }
    50% { opacity: 1; }
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: var(--bg-card) !important;
    border-radius: 10px;
    gap: 4px;
    padding: 4px;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--text-muted) !important;
    border-radius: 8px !important;
    font-size: 0.85rem !important;
}
.stTabs [aria-selected="true"] {
    background: rgba(245,197,24,0.15) !important;
    color: var(--gold) !important;
}

/* ── Movie Detail Panel ── */
.detail-panel {
    background: linear-gradient(135deg, var(--bg-card) 0%, var(--bg-card2) 100%);
    border: 1px solid rgba(245,197,24,0.15);
    border-radius: var(--radius);
    padding: 1.5rem;
    margin-bottom: 1rem;
}
.detail-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.3rem;
    font-weight: 700;
    margin: 0 0 0.3rem;
}
.detail-meta {
    font-size: 0.8rem;
    color: var(--text-muted);
}

/* ── Watchlist Button ── */
.wl-btn {
    background: rgba(230,57,70,0.1) !important;
    border: 1px solid rgba(230,57,70,0.3) !important;
    color: #e63946 !important;
    border-radius: 8px !important;
    font-size: 0.8rem !important;
    padding: 0.3rem 1rem !important;
    transition: all 0.2s !important;
}
.wl-btn:hover {
    background: rgba(230,57,70,0.2) !important;
}

/* ── Footer ── */
.app-footer {
    text-align: center;
    padding: 3rem 1rem 2rem;
    color: var(--text-muted);
    font-size: 0.78rem;
    letter-spacing: 0.5px;
}
.app-footer a { color: var(--gold); text-decoration: none; }

/* ── Spinner Override ── */
.stSpinner > div { border-top-color: var(--gold) !important; }

/* ── Number Input ── */
.stNumberInput input {
    background: #1f1f2e !important;
    border: 1px solid rgba(245,197,24,0.25) !important;
    color: var(--text-primary) !important;
    border-radius: 8px !important;
}
</style>
""", unsafe_allow_html=True)

# ─── API & Data Functions ────────────────────────────────────────────────────
API_KEY = "40c2ef328526f5f2abe5c45ac037bdfd"

@st.cache_data(show_spinner=False)
def fetch_movie_details(movie_id):
    """Fetch poster + extra metadata from TMDB."""
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
        data = requests.get(url, timeout=6).json()
        poster = (
            "https://image.tmdb.org/t/p/w500" + data["poster_path"]
            if data.get("poster_path") else
            "https://placehold.co/500x750/13131a/8a8698?text=No+Image"
        )
        return {
            "poster": poster,
            "rating": round(data.get("vote_average", 0), 1),
            "year": data.get("release_date", "")[:4],
            "overview": data.get("overview", ""),
            "genres": [g["name"] for g in data.get("genres", [])],
            "runtime": data.get("runtime", 0),
        }
    except Exception:
        return {
            "poster": "https://placehold.co/500x750/13131a/8a8698?text=Error",
            "rating": 0, "year": "", "overview": "", "genres": [], "runtime": 0,
        }


@st.cache_data(show_spinner=False)
def recommend(movie, n=5):
    idx = movies[movies["title"] == movie].index[0]
    distances = similarity[idx]
    ranked = sorted(enumerate(distances), key=lambda x: x[1], reverse=True)[1 : n + 1]
    results = []
    for i, score in ranked:
        row = movies.iloc[i]
        details = fetch_movie_details(row.movie_id)
        results.append({
            "title": row.title,
            "movie_id": row.movie_id,
            "score": round(score * 100, 1),
            **details,
        })
    return results


# ─── Load Data ──────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_data():
    movies_df = pd.DataFrame(pickle.load(open("movie_dict.pkl", "rb")))
    sim = pickle.load(open("similarity.pkl", "rb"))
    return movies_df, sim

movies, similarity = load_data()

# ─── Sidebar ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🎬 CineMatch")
    st.markdown("<div style='height:1px;background:rgba(255,255,255,0.08);margin:0.5rem 0 1rem'></div>", unsafe_allow_html=True)

    st.markdown("**⚙️ Settings**")
    num_recs = st.slider("Number of Recommendations", 3, 10, 5)
    st.markdown("<div style='height:1px;background:rgba(255,255,255,0.08);margin:1rem 0'></div>", unsafe_allow_html=True)

    st.markdown("**🗂️ My Watchlist**")
    if "watchlist" not in st.session_state:
        st.session_state.watchlist = []

    if st.session_state.watchlist:
        for wm in st.session_state.watchlist:
            col_a, col_b = st.columns([4, 1])
            col_a.markdown(f"<small>🎥 {wm}</small>", unsafe_allow_html=True)
            if col_b.button("✕", key=f"rm_{wm}"):
                st.session_state.watchlist.remove(wm)
                st.rerun()
        if st.button("🗑️ Clear All", use_container_width=True):
            st.session_state.watchlist = []
            st.rerun()
    else:
        st.markdown("<small style='color:#8a8698'>No movies saved yet.<br>Click ➕ on any card to add!</small>", unsafe_allow_html=True)

    st.markdown("<div style='height:1px;background:rgba(255,255,255,0.08);margin:1rem 0'></div>", unsafe_allow_html=True)

# ─── Hero Header ────────────────────────────────────────────────────────────
st.markdown("""
<div class='hero-header'>
    <div class='hero-title'>CineMatch</div>
    <div class='hero-sub'>Discover your next favourite film</div>
    <div class='hero-divider'></div>
    <div style='margin-top:0.9rem;font-size:0.72rem;color:#5a5670;letter-spacing:0.5px'>
        Made By Minhal Haider Naqvi 
        Movie Recommended System
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Search Panel ───────────────────────────────────────────────────────────
st.markdown("<div class='search-container'>", unsafe_allow_html=True)
st.markdown("<div class='search-label'>🔍 Pick a movie you love</div>", unsafe_allow_html=True)

col_sel, col_btn = st.columns([4, 1])
with col_sel:
    selected_movie = st.selectbox(
        label="movie",
        options=movies["title"].values,
        label_visibility="collapsed",
    )
with col_btn:
    st.markdown("<div style='margin-top:0.15rem'>", unsafe_allow_html=True)
    find_btn = st.button("✦ Find Films", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ─── Selected Movie Detail ───────────────────────────────────────────────────
if selected_movie:
    sel_id = movies[movies["title"] == selected_movie].iloc[0].movie_id
    sel_details = fetch_movie_details(sel_id)

    dcol1, dcol2 = st.columns([1, 4])
    with dcol1:
        st.image(sel_details["poster"], use_container_width=True)
    with dcol2:
        stars = "★" * int(sel_details["rating"] / 2) + "☆" * (5 - int(sel_details["rating"] / 2))
        genres_html = "".join(f"<span class='info-chip'>{g}</span>" for g in sel_details["genres"][:4])
        runtime_txt = f"{sel_details['runtime']} min" if sel_details["runtime"] else ""
        st.markdown(f"""
        <div class='detail-panel'>
            <div class='detail-title'>{selected_movie}</div>
            <div class='detail-meta'>{sel_details['year']}  {('· ' + runtime_txt) if runtime_txt else ''}</div>
            <div class='star-rating' style='margin:0.5rem 0'>{stars} <span style='color:#8a8698;font-size:0.8rem'>({sel_details['rating']}/10)</span></div>
            <div style='margin-bottom:0.7rem'>{genres_html}</div>
            <div style='font-size:0.85rem;color:#b0acbe;line-height:1.6'>{sel_details['overview'][:320] + ('…' if len(sel_details['overview']) > 320 else '')}</div>
        </div>
        """, unsafe_allow_html=True)

        # Add to watchlist
        if st.button(f"{'✓ In Watchlist' if selected_movie in st.session_state.watchlist else '➕ Add to Watchlist'}",
                     key="add_sel"):
            if selected_movie not in st.session_state.watchlist:
                st.session_state.watchlist.append(selected_movie)
                st.toast(f"✅ '{selected_movie}' added to watchlist!", icon="🎬")
            else:
                st.session_state.watchlist.remove(selected_movie)
                st.toast(f"Removed from watchlist.", icon="🗑️")
            st.rerun()

# ─── Recommendations ────────────────────────────────────────────────────────
if find_btn:
    st.markdown("<div class='fancy-divider'></div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class='section-heading'>
        🎯 Because you liked <span>"{selected_movie}"</span>
    </div>
    """, unsafe_allow_html=True)

    with st.spinner(""):
        st.markdown("<div class='loading-text'>✦ Analysing taste profile…</div>", unsafe_allow_html=True)
        recs = recommend(selected_movie, n=num_recs)

    # Stats strip
    avg_rating = round(sum(r["rating"] for r in recs) / len(recs), 1)
    st.markdown(f"""
    <div class='stats-strip'>
        <div class='stat-pill'>🎬 <b>{len(recs)}</b> recommendations</div>
        <div class='stat-pill'>⭐ Avg rating <b>{avg_rating}/10</b></div>
        <div class='stat-pill'>🔮 AI similarity match</div>
    </div>
    """, unsafe_allow_html=True)

    # Tabs: Grid View | List View
    tab1, tab2 = st.tabs(["🃏  Card View", "📋  List View"])

    with tab1:
        cols = st.columns(min(num_recs, 5))
        for i, rec in enumerate(recs):
            with cols[i % 5]:
                stars = "★" * int(rec["rating"] / 2)
                st.markdown(f"""
                <div class='movie-card'>
                    <img src='{rec["poster"]}' alt='{rec["title"]}'/>
                    <div class='movie-card-body'>
                        <div class='movie-card-rank'>#{i+1} · {rec['score']}% match</div>
                        <div class='movie-card-title'>{rec["title"]}</div>
                        <div class='star-rating'>{stars}</div>
                        <div style='font-size:0.72rem;color:#8a8698;margin-top:3px'>{rec["year"]} · {rec["rating"]}/10</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Watchlist toggle per card
                in_wl = rec["title"] in st.session_state.watchlist
                if st.button(
                    "✓ Saved" if in_wl else "➕ Save",
                    key=f"wl_{i}",
                    use_container_width=True
                ):
                    if in_wl:
                        st.session_state.watchlist.remove(rec["title"])
                    else:
                        st.session_state.watchlist.append(rec["title"])
                        st.toast(f"✅ '{rec['title']}' added!", icon="🎬")
                    st.rerun()

    with tab2:
        for i, rec in enumerate(recs):
            lc1, lc2, lc3 = st.columns([1, 5, 2])
            with lc1:
                st.image(rec["poster"], use_container_width=True)
            with lc2:
                genres_h = " · ".join(rec["genres"][:3])
                st.markdown(f"""
                <div style='padding:0.4rem 0'>
                    <div style='font-family:Playfair Display,serif;font-size:1.05rem;font-weight:700'>{rec["title"]}</div>
                    <div style='font-size:0.75rem;color:#8a8698;margin:3px 0'>{rec["year"]} · {genres_h} · {rec["runtime"]} min</div>
                    <div style='font-size:0.78rem;color:#b0acbe;margin-top:0.4rem;line-height:1.5'>{rec["overview"][:200]}{'…' if len(rec["overview"]) > 200 else ''}</div>
                </div>
                """, unsafe_allow_html=True)
            with lc3:
                st.markdown(f"""
                <div style='text-align:center;padding:0.5rem'>
                    <div style='font-size:1.6rem;font-weight:700;color:#F5C518'>{rec["rating"]}</div>
                    <div style='font-size:0.7rem;color:#8a8698'>/ 10</div>
                    <div style='font-size:0.75rem;color:#e63946;margin-top:4px'>{rec["score"]}% match</div>
                </div>
                """, unsafe_allow_html=True)
                in_wl = rec["title"] in st.session_state.watchlist
                if st.button("✓ Saved" if in_wl else "➕ Watchlist", key=f"wl_list_{i}", use_container_width=True):
                    if in_wl:
                        st.session_state.watchlist.remove(rec["title"])
                    else:
                        st.session_state.watchlist.append(rec["title"])
                        st.toast(f"✅ Added to watchlist!", icon="🎬")
                    st.rerun()
            st.markdown("<div class='fancy-divider'></div>", unsafe_allow_html=True)