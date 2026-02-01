import streamlit as st
import time
import random

# =================================================================
# 1. CONFIGURAZIONE E DESIGN (WineArt Identity)
# =================================================================
st.set_page_config(page_title="Wine Selector 2.1", page_icon="🍷", layout="centered")

st.markdown("""
    <style>
    /* NASCONDE ELEMENTI DI SISTEMA */
    header {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    #MainMenu {visibility: hidden !important;}
    .stAppDeployButton {display:none !important;}
    [data-testid="stHeader"] {background: rgba(0,0,0,0) !important;}
    [data-testid="stToolbar"] {display: none !important;}
    #GithubIcon {visibility: hidden !important;}
    
    /* SFONDO E CARD */
    .main { background-color: #fdfaf5; }
    .wine-card {
        text-align: center;
        background-color: white;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        border: 1px solid #eee;
    }
    
    /* TESTI SCHEDA */
    .wine-title { color: #b00000; font-size: 32px; font-weight: bold; margin-bottom: 5px; }
    .wine-producer { font-size: 20px; font-weight: bold; color: #333; margin-bottom: 0px; }
    .wine-region { color: #b00000; font-weight: bold; font-size: 18px; margin-bottom: 5px; }
    .wine-price { font-size: 24px; color: #444; margin-bottom: 25px; font-weight: bold; }
    
    /* INFO TECNICHE */
    .tech-info { text-align: left; display: inline-block; max-width: 500px; font-size: 16px; line-height: 1.7; color: #444; }
    .check { color: #b00000; margin-right: 10px; font-weight: bold; font-size: 18px; }
    
    /* BOTTONI */
    .stButton>button { width: 100%; border-radius: 25px; background-color: #800020; color: white; height: 3.5em; font-weight: bold; border: none; }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] { background-color: #f1f1f1; border-radius: 10px 10px 0 0; padding: 10px 15px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# =================================================================
# 2. LINK CATEGORIE (Ancore WordPress)
# =================================================================
LINK_BASE = "https://www.cartavinidigitale.it/menu-digitale-wineart/"
LINK_BOLLICINE = f"{LINK_BASE}#1740398853462-a2bc72ab-7b7d"
LINK_CHAMPAGNE = f"{LINK_BASE}#1745914895725-84011f71-5d21"
LINK_BIANCHI = f"{LINK_BASE}#1745853678461-fb96405a-dddb"
LINK_ROSE = f"{LINK_BASE}#1740390912898-ab964a88-abf3"
LINK_ROSSI = f"{LINK_BASE}#1745654818035-20641e56-b023"
LINK_ESTERI = f"{LINK_BASE}#1745917570747-12734a65-c3ee"

# =================================================================
# 3. DATABASE VINI
# =================================================================
vini = [
    {
        "nome": "Petite Arvine", "produttore": "Les Cretes", "regione": "Valle d'Aosta",
        "prezzo": 36, "denominazione": "DOC", "affinamento": "In Acciaio", "uve": "Petite Arvine", "gradazione": "15%",
        "olfatto": "Note di frutta esotica, agrumi e biancospino.",
        "gusto": "Sapido e fresco, minerale e bilanciato.",
        "immagine": "https://www.lescretes.it/wp-content/uploads/2021/04/Petite-Arvine-Les-Cretes.png",
        "categoria": "Vini Bianchi", "abbinamento": "Pesce", "mood": "Incontro di lavoro", "struttura": "Leggero", "link": LINK_BIANCHI
    },
    {
        "nome": "Sassicaia", "produttore": "Tenuta San Guido", "regione": "Toscana",
        "prezzo": 350, "denominazione": "DOC", "affinamento": "24 mesi in Barrique", "uve": "Cabernet Sauvignon/Franc", "gradazione": "14%",
        "olfatto": "Frutti rossi, spezie, tabacco e note tostate.",
        "gusto": "Maestoso, con tannini setosi e infinita persistenza.",
        "immagine": "https://www.tenutasanguido.com/images/bottiglia_sassicaia.png",
        "categoria": "Vini Rossi", "abbinamento": "Carne", "mood": "Occasione Speciale", "struttura": "Robusto", "link": LINK_ROSSI
    },
    {
        "nome": "Cuvée Prestige", "produttore": "Ca' del Bosco", "regione": "Lombardia",
        "prezzo": 45, "denominazione": "DOCG", "affinamento": "28 mesi sui lieviti", "uve": "Chardonnay, Pinot Nero", "gradazione": "12.5%",
        "olfatto": "Crosta di pane e agrumi.", "gusto": "Equilibrato e piacevolmente acido.",
        "immagine": "https://www.cadelbosco.com/wp-content/uploads/2021/03/cuvee-prestige.png",
        "categoria": "Bollicine", "abbinamento": "Aperitivo", "mood": "Incontro di lavoro", "struttura": "Leggero", "link": LINK_BOLLICINE
    }
]

def render_wine_card(v):
    st.markdown(f"""
    <div class="wine-card">
        <img src="{v['immagine']}" width="160" style="margin-bottom:20px;">
        <div class="wine-title">{v['nome']}</div>
        <div class="wine-producer">{v['produttore']}</div>
        <div class="wine-region">{v['regione']}</div>
        <div class="wine-price">€ {v['prezzo']}</div>
        <div class="tech-info">
            <p><span class="check">✔</span> <b>Uve:</b> {v['uve']}</p>
            <p><span class="check">✔</span> <b>Olfatto:</b> {v['olfatto']}</p>
            <p><span class="check">✔</span> <b>Gusto:</b> {v['gusto']}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.link_button(f"🔎 VEDI TUTTI I {v['categoria'].upper()}", v['link'])
    st.write("")

# =================================================================
# 4. INTERFACCIA A SCHEDE
# =================================================================
st.title("🍷 Wine Selector 2.1")
st.link_button("📖 CARTA VINI COMPLETA", LINK_BASE)

tab_sommelier, tab_carta = st.tabs(["🤖 IL TUO SOMMELIER", "📖 SFOGLIA LA CARTA"])

# --- TAB 1: IL SOMMELIER ---
with tab_sommelier:
    st.subheader("Lasciati consigliare")
    c1, c2, c3 = st.columns(3)
    with c1: cibo = st.selectbox("Cosa mangi?", ["Scegli...", "Aperitivo", "Pesce", "Carne", "Dessert"])
    with c2: mood = st.selectbox("Atmosfera?", ["Scegli...", "Cena con amici", "Incontro di lavoro", "Occasione Speciale"])
    with c3: struttura = st.selectbox("Struttura?", ["Scegli...", "Leggero", "Di Medio Corpo", "Robusto"])
    
    if st.button("CHIEDI AL SOMMELIER 🍇"):
        if cibo == "Scegli..." or mood == "Scegli...":
            st.warning("Seleziona almeno cibo e atmosfera!")
        else:
            match = [v for v in vini if v["abbinamento"] == cibo and v["mood"] == mood]
            if not match: match = [v for v in vini if v["abbinamento"] == cibo]
            if match:
                selezione = random.sample(match, min(len(match), 3))
                st.success(f"Ho selezionato {len(selezione)} proposte per te:")
                for v in selezione: render_wine_card(v)
            else:
                st.error("Nessun vino trovato!")

# --- TAB 2: SFOGLIA LA CARTA ---
with tab_carta:
    ricerca = st.text_input("🔍 Cerca per nome, uva o cantina...", "").lower()
    cat_scelta = st.selectbox("Seleziona Categoria", ["Tutte", "Bollicine", "Champagne", "Vini Bianchi", "Vini Rosè", "Vini Rossi", "Vini Esteri"])

    with st.expander("🛠️ Filtri avanzati (Corpo e Budget)"):
        f1, f2 = st.columns(2)
        with f1: str_scelta = st.selectbox("Struttura", ["Tutti", "Leggero", "Di Medio Corpo", "Robusto"])
        with f2: prezzo_max = st.slider("Budget Max (€)", 10, 500, 500)

    st.write("---")
    
    v_fil = vini.copy()
    if cat_scelta != "Tutte": v_fil = [v for v in v_fil if v["categoria"] == cat_scelta]
    if str_scelta != "Tutti": v_fil = [v for v in v_fil if v["struttura"] == str_scelta]
    v_fil = [v for v in v_fil if v["prezzo"] <= prezzo_max]
    if ricerca: v_fil = [v for v in v_fil if ricerca in v["nome"].lower() or ricerca in v["uve"].lower() or ricerca in v["produttore"].lower()]

    if v_fil:
        st.caption(f"Visualizzando {len(v_fil)} etichette")
        for v in v_fil: render_wine_card(v)
    else:
        st.error("Nessun vino trovato con questi filtri.")
        # IL TASTO MAGICO DI RESET
        if st.button("🔄 AZZERA TUTTI I FILTRI"):
            st.rerun()

# --- 5. FOOTER ---
st.divider()
st.markdown("""
    <div style="text-align: center; color: #888; font-size: 14px;">
        Wine Selector 2.1 • Powered by 
        <a href="https://www.superstart.it" target="_blank" style="color: #b00000; text-decoration: none; font-weight: bold;">SuPeR</a> 
        & Streamlit
    </div>
    """, unsafe_allow_html=True)
