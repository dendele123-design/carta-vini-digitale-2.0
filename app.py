import streamlit as st
import time
import random

# =================================================================
# 1. CONFIGURAZIONE E DESIGN (Wine Selector 2.0)
# =================================================================
st.set_page_config(page_title="Wine Selector 2.0", page_icon="🍷", layout="centered")

# CSS Avanzato per ricreare la scheda dello screenshot
st.markdown("""
    <style>
    .main { background-color: #fdfaf5; }
    
    /* Contenitore della scheda vino */
    .wine-card {
        text-align: center;
        background-color: white;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        margin-bottom: 30px;
        border: 1px solid #eee;
    }
    
    .wine-title { color: #b00000; font-size: 34px; font-weight: bold; margin-bottom: 10px; }
    .wine-producer { font-size: 22px; font-weight: bold; color: #333; margin-bottom: 0px; }
    .wine-region { color: #b00000; font-weight: bold; font-size: 20px; margin-bottom: 5px; }
    .wine-price { font-size: 24px; color: #444; margin-bottom: 25px; }
    
    /* Sezione Info Tecniche con icone spunta */
    .tech-info {
        text-align: left;
        display: inline-block;
        max-width: 500px;
        font-size: 17px;
        line-height: 1.8;
        color: #444;
    }
    .check { color: #b00000; margin-right: 10px; font-weight: bold; font-size: 20px; }
    
    /* Bottoni e Navigazione */
    .stButton>button { width: 100%; border-radius: 25px; background-color: #800020; color: white; height: 3.5em; font-weight: bold; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { 
        background-color: #f1f1f1; border-radius: 10px 10px 0 0; padding: 10px 20px; font-weight: bold; 
    }
    </style>
    """, unsafe_allow_html=True)

# =================================================================
# 2. IL DATABASE DEI VINI (Qui aggiungerai tutti i tuoi vini)
# =================================================================
# Ogni vino ha una "categoria" per la carta e dei "tag" per il sommelier.
vini = [
    {
        "nome": "Petite Arvine",
        "produttore": "Les Cretes",
        "regione": "Valle d'Aosta",
        "prezzo": "36 €",
        "denominazione": "DOC",
        "affinamento": "In Acciaio",
        "uve": "Petite Arvine",
        "gradazione": "15%",
        "olfatto": "Note di frutta esotica, agrumi, bacche di ginepro, biancospino, glicine e gelsomino.",
        "gusto": "Sapido e fresco grazie alla sua buona acidità, minerale e bilanciato.",
        "immagine": "https://www.lescretes.it/wp-content/uploads/2021/04/Petite-Arvine-Les-Cretes.png",
        "categoria": "Vini Bianchi",
        "abbinamento": "Pesce",
        "mood": "Incontro di lavoro",
        "struttura": "Leggero"
    },
    {
        "nome": "Champagne Vintage 2013",
        "produttore": "Dom Pérignon",
        "regione": "Épernay - Francia",
        "prezzo": "280 €",
        "denominazione": "AOC",
        "affinamento": "Oltre 96 mesi sui lieviti",
        "uve": "Chardonnay, Pinot Noir",
        "gradazione": "12.5%",
        "olfatto": "Note floreali, polvere di cacao e sentori tostati.",
        "gusto": "Preciso, elegante, con una mineralità salina iconica.",
        "immagine": "https://media-verticomm.freetls.fastly.net/product-images/120286-champagne-dom-perignon-vintage-2013-box.png",
        "categoria": "Champagne",
        "abbinamento": "Pesce",
        "mood": "Occasione Speciale",
        "struttura": "Robusto"
    },
    # AGGIUNGI QUI I PROSSIMI VINI COPIANDO IL BLOCCO SOPRA...
]

# Funzione per stampare la scheda vino (per non ripetere il codice)
def render_wine_card(v):
    st.markdown(f"""
    <div class="wine-card">
        <img src="{v['immagine']}" width="180" style="margin-bottom:20px;">
        <div class="wine-title">{v['nome']}</div>
        <div class="wine-producer">{v['produttore']}</div>
        <div class="wine-region">{v['regione']}</div>
        <div class="wine-price">{v['prezzo']}</div>
        <div class="tech-info">
            <p><span class="check">✔</span> <b>Denominazione:</b> {v['denominazione']}</p>
            <p><span class="check">✔</span> <b>Affinamento:</b> {v['affinamento']}</p>
            <p><span class="check">✔</span> <b>Uve:</b> {v['uve']}</p>
            <p><span class="check">✔</span> <b>Gradazione:</b> {v['gradazione']}</p>
            <p><span class="check">✔</span> <b>Olfatto:</b> {v['olfatto']}</p>
            <p><span class="check">✔</span> <b>Gusto:</b> {v['gusto']}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# =================================================================
# 3. INTERFACCIA PRINCIPALE A SCHEDE
# =================================================================
st.title("🍷 Wine Selector 2.0")
st.write("L'eccellenza della nostra cantina a portata di click.")

tab_sommelier, tab_carta = st.tabs(["🤖 IL TUO SOMMELIER", "📖 SFOGLIA LA CARTA"])

# --- TAB 1: IL SOMMELIER (Ricerca filtrata) ---
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
                st.success(f"Ho selezionato {len(match)} bottiglie perfette:")
                for v in match: render_wine_card(v)
            else:
                st.error("Nessun vino trovato!")

# --- TAB 2: LA CARTA VINI (Suddivisa per categorie) ---
with tab_carta:
    categorie = ["Bollicine", "Champagne", "Vini Bianchi", "Vini Rossi", "Vini Esteri"]
    scelta_cat = st.selectbox("Seleziona una categoria:", categorie)
    
    st.divider()
    
    # Filtriamo i vini per la categoria scelta
    vini_categoria = [v for v in vini if v["categoria"] == scelta_cat]
    
    if vini_categoria:
        st.write(f"Visualizzando **{len(vini_categoria)}** etichette in **{scelta_cat}**")
        for v in vini_categoria:
            render_wine_card(v)
    else:
        st.info(f"Stiamo aggiornando la selezione di {scelta_cat}. Torna a trovarci!")

# Footer
st.divider()
# --- FOOTER PERSONALIZZATO ---
st.divider()
st.markdown("""
    <div style="text-align: center; color: #888; font-size: 14px;">
        Wine Selector 2.0 • Powered by 
        <a href="https://www.superstart.it" style="color: #b00000; text-decoration: none; font-weight: bold;">SuPeR</a> 
        & Streamlit
    </div>
    """, unsafe_allow_html=True)
