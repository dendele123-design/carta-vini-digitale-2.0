import streamlit as st
import time
import random

# =================================================================
# 1. CONFIGURAZIONE E DESIGN (WineArt Identity)
# =================================================================
st.set_page_config(page_title="Wine Selector 2.3", page_icon="🍷", layout="centered")

ROSSO_BRAND = "#DC0612"

st.markdown(f"""
<style>
/* FORZA IL COLORE DEL TESTO PER EVITARE PROBLEMI CON DARK MODE */
html, body, [class*="css"], .stMarkdown, p, label {{
    color: #1a1a1a !important;
}}

/* NASCONDE ELEMENTI DI SISTEMA */
header {{visibility: hidden !important;}}
footer {{visibility: hidden !important;}}
#MainMenu {{visibility: hidden !important;}}
.stAppDeployButton {{display:none !important;}}
[data-testid="stHeader"] {{background: rgba(0,0,0,0) !important;}}

/* SFONDO GENERALE FORZATO CHIARO */
.stApp {{
    background-color: #fdfaf5 !important;
}}

/* STILE LINGUETTE (TABS) */
.stTabs [data-baseweb="tab-list"] {{
    gap: 8px;
}}
.stTabs [data-baseweb="tab"] {{
    background-color: #e0e0e0 !important;
    border-radius: 10px 10px 0 0;
    padding: 10px 15px;
    color: #555 !important;
}}
.stTabs [data-baseweb="tab"][aria-selected="true"] {{
    background-color: #800020 !important;
    color: white !important;
}}

/* SCHEDA VINO */
.wine-card {{
    text-align: center;
    background-color: white !important;
    padding: 30px;
    border-radius: 20px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    margin-bottom: 20px;
    border: 1px solid #eee;
}}
.out-of-stock-card {{ opacity: 0.4; filter: grayscale(100%); }}
.out-of-stock-badge {{
    background-color: #ff4b4b !important;
    color: white !important;
    padding: 5px 15px;
    border-radius: 10px;
    font-weight: bold;
    display: inline-block;
    margin-bottom: 15px;
    font-size: 14px;
}}

.wine-title {{ color: #b00000 !important; font-size: 30px; font-weight: bold; margin-bottom: 5px; }}
.wine-producer {{ font-size: 18px; font-weight: bold; color: #333 !important; }}
.wine-region-label {{ color: #b00000 !important; font-weight: bold; font-size: 16px; margin-bottom: 5px; }}
.wine-price {{ font-size: 22px; color: #444 !important; margin-bottom: 20px; font-weight: bold; }}

/* INFO TECNICHE */
.tech-info {{ text-align: left; display: inline-block; max-width: 500px; font-size: 15px; color: #444 !important; }}
.check {{ color: #b00000 !important; margin-right: 8px; font-weight: bold; }}

/* BOTTONI */
.stButton>button {{ 
    width: 100%; 
    border-radius: 25px; 
    background-color: #800020 !important; 
    color: white !important; 
    height: 3.5em; 
    font-weight: bold; 
    border: none; 
}}

.region-divider {{
    background-color: #f4ece2 !important;
    padding: 10px;
    border-radius: 10px;
    margin: 20px 0;
    font-weight: bold;
    color: #800020 !important;
    text-align: center;
    border-bottom: 2px solid #800020;
    text-transform: uppercase;
}}
</style>
""", unsafe_allow_html=True)

# =================================================================
# 2. ORDINE E REGOLAZIONI
# =================================================================
ORDINE_REGIONI = ["Valle d'Aosta", "Piemonte", "Lombardia", "Liguria", "Trentino-Alto Adige", "Veneto", "Friuli-Venezia Giulia", "Emilia-Romagna", "Toscana", "Umbria", "Marche", "Lazio", "Abruzzo", "Molise", "Campania", "Basilicata", "Puglia", "Calabria", "Sicilia", "Sardegna"]

# =================================================================
# 3. DATABASE VINI
# =================================================================
vini = [
    {
        "nome": "Petite Arvine", "produttore": "Les Cretes", "regione": "Valle d'Aosta",
        "prezzo": 36, "denominazione": "DOC", "affinamento": "In Acciaio", "uve": "Petite Arvine", "gradazione": "15%",
        "olfatto": "Note di frutta esotica.", "gusto": "Sapido e minerale.",
        "immagine": "https://www.cartavinidigitale.it/wp-content/uploads/2026/01/Les_cretes_petite_arvine_superstart.jpg.jpeg",
        "categoria": "Vini Bianchi", "abbinamento": "Pesce", "mood": "Incontro di lavoro", "struttura": "Leggero",
        "esaurito": False
    },
    {
        "nome": "Athena", "produttore": "Il Vino e le Rose", "regione": "Piemonte",
        "prezzo": 34, "denominazione": "DOC", "affinamento": "In Acciaio", "uve": "70% Cortese 30% Timorasso ", "gradazione": "12,5%",
        "olfatto": "Note di frutta esotica, agrumi, bacche di ginepro, biancospino, glicine e gelsomino. ", "gusto": "Sapido e fresco grazie alla sua buona acidità.",
        "immagine": "https://www.cartavinidigitale.it/wp-content/uploads/2025/07/Athena_cortese_timorasso_il_vino_e_le_rose_superstart.jpg",
        "categoria": "Vini Bianchi", "abbinamento": "Pesce", "mood": "Incontro di lavoro", "struttura": "Leggero",
        "esaurito": False
    },
    {
        "nome": "Etna Rosso “Fragore”", "produttore": "Donnafugata", "regione": "Sicilia",
        "prezzo": 82, "denominazione": "DOC", "affinamento": "In Inox", "uve": "Etna Rosso", "gradazione": "14%",
        "olfatto": "Sfumature di grafite e bacche selvatiche.", "gusto": "Profondo e sapido-minerale.",
        "immagine": "https://www.cartavinidigitale.it/wp-content/uploads/2025/07/Fragore.jpg",
        "categoria": "Vini Rossi", "abbinamento": "Carne", "mood": "Occasione Speciale", "struttura": "Robusto",
        "esaurito": True
    }
]

# --- FUNZIONE RENDER SCHEDA (FLUSH LEFT) ---
def render_wine_card(v):
    classe_esaurito = "out-of-stock-card" if v.get("esaurito") else ""
    label_esaurito = '<div class="out-of-stock-badge">❌ MOMENTANEAMENTE ESAURITO</div>' if v.get("esaurito") else ""

    html_code = f"""<div class="wine-card {classe_esaurito}">
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
</div>"""
    st.markdown(html_code, unsafe_allow_html=True)

# =================================================================
# 4. INTERFACCIA
# =================================================================
st.title("🍷 Wine Selector")

tab_sommelier, tab_carta = st.tabs(["🤖 IL TUO SOMMELIER", "📖 SFOGLIA LA CARTA"])

with tab_sommelier:
    c1, c2, c3 = st.columns(3)
    with c1: cibo = st.selectbox("Cosa mangi?", ["Scegli...", "Aperitivo", "Pesce", "Carne", "Dessert"])
    with c2: mood = st.selectbox("Atmosfera?", ["Scegli...", "Cena con amici", "Incontro di lavoro", "Occasione Speciale"])
    with c3: struttura = st.selectbox("Struttura?", ["Scegli...", "Leggero", "Di Medio Corpo", "Robusto"])
    
    if st.button("CHIEDI AL SOMMELIER 🍇"):
        if cibo == "Scegli..." or mood == "Scegli...":
            st.warning("Seleziona almeno cibo e atmosfera!")
        else:
            match = [v for v in vini if v["abbinamento"] == cibo and v["mood"] == mood and not v.get("esaurito")]
            if not match: match = [v for v in vini if v["abbinamento"] == cibo and not v.get("esaurito")]
            if match:
                selezione = random.sample(match, min(len(match), 3))
                st.success(f"Ecco le migliori proposte disponibili:")
                for v in selezione: render_wine_card(v)
            else:
                st.error("Nessun vino disponibile.")

with tab_carta:
    ricerca = st.text_input("🔍 Cerca per nome, uva o cantina...", "").lower()
    cat_scelta = st.selectbox("Seleziona Categoria", ["Tutte", "Bollicine", "Champagne", "Vini Bianchi", "Vini Rosè", "Vini Rossi", "Vini Esteri"])
    with st.expander("🛠️ Filtri avanzati"):
        f1, f2, f3 = st.columns(3)
        with f1: reg_scelta = st.selectbox("Regione", ["Tutte"] + ORDINE_REGIONI)
        with f2: str_scelta = st.selectbox("Corpo", ["Tutti", "Leggero", "Di Medio Corpo", "Robusto"])
        with f3: prezzo_max = st.slider("Budget Max (€)", 10, 500, 500)

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
        curr_reg = ""
        for v in v_fil:
            if v['categoria'] in ["Vini Bianchi", "Vini Rossi", "Vini Rosè"] and v['regione'] != curr_reg:
                curr_reg = v['regione']
                st.markdown(f"<div class='region-divider'>📍 {curr_reg.upper()}</div>", unsafe_allow_html=True)
            render_wine_card(v)
    else:
        st.error("Nessun vino trovato.")
        if st.button("🔄 AZZERA FILTRI"): st.rerun()

# =================================================================
# 5. TASTO HUB UNIVERSALE (FUORI DAI TAB)
# =================================================================
st.write("")
st.write("---")
st.markdown("<p style='text-align:center; font-size:13px; color:#888;'>Hai bisogno di altri strumenti?</p>", unsafe_allow_html=True)
# Ho inserito il link alla tua stazione centrale
st.link_button("🌐 VEDI TUTTE LE NOSTRE WEB APP", "https://app-comunicattivamente-center.streamlit.app/")

# --- FOOTER ---
st.divider()
st.markdown(f"""
<div style="text-align: center; color: #888 !important; font-size: 14px;">
Wine Selector 2.3 • Powered by 
<a href="https://www.superstart.it" target="_blank" style="color: {ROSSO_BRAND} !important; text-decoration: none; font-weight: bold;">SuPeR</a> 
& Streamlit
</div>
""", unsafe_allow_html=True)
