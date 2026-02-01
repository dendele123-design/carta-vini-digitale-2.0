import streamlit as st
import time
import random

# =================================================================
# 1. CONFIGURAZIONE E DESIGN
# =================================================================
st.set_page_config(page_title="Wine Selector 2.3", page_icon="🍷", layout="centered")

st.markdown("""
    <style>
    header {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    #MainMenu {visibility: hidden !important;}
    .stAppDeployButton {display:none !important;}
    [data-testid="stHeader"] {background: rgba(0,0,0,0) !important;}
    
    .main { background-color: #fdfaf5; }
    
    /* SCHEDA VINO */
    .wine-card {
        text-align: center;
        background-color: white;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.06);
        margin-bottom: 20px;
        border: 1px solid #eee;
        position: relative; /* Per posizionare il bollino esaurito */
    }
    
    /* EFFETTO PER VINO ESAURITO */
    .out-of-stock-card {
        opacity: 0.6; /* Rende la scheda un po' sbiadita */
    }
    .out-of-stock-badge {
        background-color: #ff4b4b;
        color: white;
        padding: 5px 15px;
        border-radius: 10px;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 15px;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-size: 14px;
    }

    .wine-title { color: #b00000; font-size: 30px; font-weight: bold; margin-bottom: 5px; }
    .wine-producer { font-size: 18px; font-weight: bold; color: #333; }
    .wine-region-label { color: #b00000; font-weight: bold; font-size: 16px; margin-bottom: 5px; }
    .wine-price { font-size: 22px; color: #444; margin-bottom: 20px; font-weight: bold; }
    
    .tech-info { text-align: left; display: inline-block; max-width: 500px; font-size: 15px; color: #444; }
    .check { color: #b00000; margin-right: 8px; font-weight: bold; }
    
    .stButton>button { width: 100%; border-radius: 25px; background-color: #800020; color: white; height: 3.5em; font-weight: bold; border: none; }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] { background-color: #f1f1f1; border-radius: 10px 10px 0 0; padding: 10px 15px; font-weight: bold; }
    
    .region-divider {
        background-color: #f4ece2;
        padding: 10px;
        border-radius: 10px;
        margin: 20px 0;
        font-weight: bold;
        color: #800020;
        text-align: center;
        border-bottom: 2px solid #800020;
        text-transform: uppercase;
    }
    </style>
    """, unsafe_allow_html=True)

# =================================================================
# 2. ORDINE GEOGRAFICO
# =================================================================
ORDINE_REGIONI = [
    "Valle d'Aosta", "Piemonte", "Lombardia", "Liguria", "Trentino-Alto Adige", 
    "Veneto", "Friuli-Venezia Giulia", "Emilia-Romagna", 
    "Toscana", "Umbria", "Marche", "Lazio", "Abruzzo", "Molise", 
    "Campania", "Basilicata", "Puglia", "Calabria", "Sicilia", "Sardegna"
]
LINK_BASE = "https://www.cartavinidigitale.it/menu-digitale-wineart/"

# =================================================================
# 3. DATABASE VINI (Con gestione ESAURITO)
# =================================================================
vini = [
    {
        "nome": "Petite Arvine", "produttore": "Les Cretes", "regione": "Valle d'Aosta",
        "prezzo": 36, "denominazione": "DOC", "affinamento": "In Acciaio", "uve": "Petite Arvine", "gradazione": "15%",
        "olfatto": "Note di frutta esotica.", "gusto": "Sapido e minerale.",
        "immagine": "https://www.lescretes.it/wp-content/uploads/2021/04/Petite-Arvine-Les-Cretes.png",
        "categoria": "Vini Bianchi", "abbinamento": "Pesce", "mood": "Incontro di lavoro", "struttura": "Leggero",
        "esaurito": False # Questo vino c'è
    },
    {
        "nome": "Sassicaia", "produttore": "Tenuta San Guido", "regione": "Toscana",
        "prezzo": 350, "denominazione": "DOC", "affinamento": "24 mesi in Barrique", "uve": "Cabernet Sauvignon", "gradazione": "14%",
        "olfatto": "Spezie e note tostate.", "gusto": "Maestoso.",
        "immagine": "https://www.tenutasanguido.com/images/bottiglia_sassicaia.png",
        "categoria": "Vini Rossi", "abbinamento": "Carne", "mood": "Occasione Speciale", "struttura": "Robusto",
        "esaurito": True # <--- QUESTO VINO APPARIRÀ COME NON DISPONIBILE
    }
]

# FUNZIONE PER MOSTRARE LA SCHEDA
def render_wine_card(v):
    # Controlliamo se è esaurito per aggiungere le classi CSS
    classe_esaurito = "out-of-stock-card" if v.get("esaurito") else ""
    label_esaurito = '<div class="out-of-stock-badge">❌ MOMENTANEAMENTE ESAURITO</div>' if v.get("esaurito") else ""

    st.markdown(f"""
    <div class="wine-card {classe_esaurito}">
        {label_esaurito}
        <img src="{v['immagine']}" width="150" style="margin-bottom:15px;">
        <div class="wine-title">{v['nome']}</div>
        <div class="wine-producer">{v['produttore']}</div>
        <div class="wine-region-label">{v['regione']}</div>
        <div class="wine-price">€ {v['prezzo']}</div>
        <div class="tech-info">
            <p><span class="check">✔</span> <b>Denominazione:</b> {v['denominazione']}</p>
            <p><span class="check">✔</span> <b>Uve:</b> {v['uve']}</p>
            <p><span class="check">✔</span> <b>Olfatto:</b> {v['olfatto']}</p>
            <p><span class="check">✔</span> <b>Gusto:</b> {v['gusto']}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.write("")

# =================================================================
# 4. INTERFACCIA
# =================================================================
st.title("🍷 Wine Selector 2.3")
st.link_button("📖 CARTA VINI COMPLETA", LINK_BASE)

tab_sommelier, tab_carta = st.tabs(["🤖 IL TUO SOMMELIER", "📖 SFOGLIA LA CARTA"])

# --- TAB 1: SOMMELIER (Escludiamo gli esauriti!) ---
with tab_sommelier:
    c1, c2, c3 = st.columns(3)
    with c1: cibo = st.selectbox("Cosa mangi?", ["Scegli...", "Aperitivo", "Pesce", "Carne", "Dessert"])
    with c2: mood = st.selectbox("Atmosfera?", ["Scegli...", "Cena con amici", "Incontro di lavoro", "Occasione Speciale"])
    with c3: struttura = st.selectbox("Struttura?", ["Scegli...", "Leggero", "Di Medio Corpo", "Robusto"])
    
    if st.button("CHIEDI AL SOMMELIER 🍇"):
        if cibo == "Scegli..." or mood == "Scegli...":
            st.warning("Seleziona almeno cibo e atmosfera!")
        else:
            # Filtro: cerchiamo solo vini DISPONIBILI (esaurito == False)
            match = [v for v in vini if v["abbinamento"] == cibo and v["mood"] == mood and not v.get("esaurito")]
            if not match: match = [v for v in vini if v["abbinamento"] == cibo and not v.get("esaurito")]
            
            if match:
                selezione = random.sample(match, min(len(match), 3))
                st.success(f"Ecco le migliori proposte disponibili:")
                for v in selezione: render_wine_card(v)
            else:
                st.error("Nessun vino disponibile per questa scelta.")

# --- TAB 2: CARTA VINI (Qui mostriamo anche gli esauriti) ---
with tab_carta:
    ricerca = st.text_input("🔍 Cerca per nome, uva o cantina...", "").lower()
    cat_scelta = st.selectbox("Seleziona Categoria", ["Tutte", "Bollicine", "Champagne", "Vini Bianchi", "Vini Rosè", "Vini Rossi", "Vini Esteri"])

    with st.expander("🛠️ Filtri avanzati"):
        f1, f2, f3 = st.columns(3)
        with f1: reg_scelta = st.selectbox("Regione", ["Tutte"] + ORDINE_REGIONI)
        with f2: str_scelta = st.selectbox("Corpo", ["Tutti", "Leggero", "Di Medio Corpo", "Robusto"])
        with f3: prezzo_max = st.slider("Budget Max (€)", 10, 500, 500)

    st.write("---")
    
    # Logica Filtri
    v_fil = vini.copy()
    if cat_scelta != "Tutte": v_fil = [v for v in v_fil if v["categoria"] == cat_scelta]
    if reg_scelta != "Tutte": v_fil = [v for v in v_fil if v["regione"] == reg_scelta]
    if str_scelta != "Tutti": v_fil = [v for v in v_fil if v["struttura"] == str_scelta]
    v_fil = [v for v in v_fil if v["prezzo"] <= prezzo_max]
    if ricerca: v_fil = [v for v in v_fil if ricerca in v["nome"].lower() or ricerca in v["uve"].lower() or ricerca in v["produttore"].lower()]

    def sort_geo(v):
        try: return ORDINE_REGIONI.index(v['regione'])
        except ValueError: return 999
    v_fil.sort(key=sort_geo)

    if v_fil:
        current_region = ""
        for v in v_fil:
            if v['categoria'] in ["Vini Bianchi", "Vini Rossi", "Vini Rosè"] and v['regione'] != current_region:
                current_region = v['regione']
                st.markdown(f"<div class='region-divider'>📍 {current_region.upper()}</div>", unsafe_allow_html=True)
            render_wine_card(v)
    else:
        st.error("Nessun vino trovato.")
        if st.button("🔄 AZZERA FILTRI"): st.rerun()

# --- 5. FOOTER ---
st.divider()
st.markdown("""
    <div style="text-align: center; color: #888; font-size: 14px;">
        Wine Selector 2.3 • Powered by 
        <a href="https://www.superstart.it" target="_blank" style="color: #b00000; text-decoration: none; font-weight: bold;">SuPeR</a> 
        & Streamlit
    </div>
    """, unsafe_allow_html=True)
