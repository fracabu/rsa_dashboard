import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import time
import plotly.express as px
import plotly.graph_objects as go

# Configurazione della pagina
st.set_page_config(page_title="Dashboard RSA ASL Roma 1", layout="wide")

# Dati dettagliati delle strutture RSA
data = {
    'Nome': [
        'VILLA SACRA FAMIGLIA', 'VILLA DOMELIA', 'DON ORIONE', 'SANTA CHIARA', 
        'RSA SALUS', 'VILLA GRAZIA', 'VILLA VERDE', 'SANTA LUCIA DEI FONTANILI',
        'AUXOLOGICO ROMA BUON PASTORE', 'NOSTRA SIGNORA DEL SACRO CUORE',
        'SAN RAFFAELE MONTE MARIO', 'SANTA FRANCESCA ROMANA',
        'SAN RAFFAELE FLAMINIA', 'ANNI AZZURRI - PARCO DI VEIO'
    ],
    'Posti_Letto': [
        120, 98, 70, 40, 83, 30, 130, 80, 202, 110, 60, 60, 77, 118
    ],
    'Posti_Accreditati': [
        80, 67, 70, 40, 80, 30, 120, 80, 180, 100, 60, 60, 77, 110
    ],
    'Tipologia': [
        'Mant. A', 'Intensivo', 'Mant. A', 'Mant. B', 
        'Mant. A - Intensivo', 'E.P.D.C.C.', 'Mant. A - Intensivo',
        'Mant. A', 'Mant. A - Intensivo', 'Mant. A/B',
        'Mant. A - E.P.N.A. - E.P.D.C.C. S.R.', 'Mant. A',
        'Mant. A', 'Mant. A'
    ],
    'Indirizzo': [
        'Largo Ottorino Respighi, 6, Roma', 'Via Arbe, 1, Roma',
        'Via della Camilluccia, 112, Roma', 'Via dello Scalo di Settebagni, 77, Roma',
        'Via Paolo Monelli, 43, Roma', 'Via Francesco Cherubini, 26, Roma',
        'Via di Torrevecchia, 250, Roma', 'Via Valle dei Fontanili, 211, Roma',
        'Via di Vallelunga, 8, Roma', 'Via Cardinal Pacca, 16, Roma',
        'Via delle Benedettine, 18, Roma', 'Via Casal del Marmo, 401, Roma',
        'Via del Labaro, 121, Roma', 'Via Barbarano Romano, 43, Roma'
    ],
    'Municipio': [15, 3, 15, 3, 3, 14, 14, 14, 13, 13, 14, 14, 15, 15],
    'Telefono': [
        '06 4040851', '06 8170202', '06 35420803', '06 88565953',
        '06 872032', '06 3386284', '06 3012892', '06 6111901',
        '06 61521965', '06 6621748', '06 52253845', '06 3097439',
        '06 33610024', '06 995071'
    ],
    'Email': [
        'accoglienzavsf@italianhospitalgroup.com', 'accettazione@villadomelia.it',
        'info@endofap.lazio.it', 'info@rsasantachiara.com',
        'amministrazione@rsasalus.it', 'staff@villa-grazia.com',
        'villaverde@tiscali.it', 'segreteria@gruppopaganini.it',
        'fatturazione@auxologicoroma.it', 'ospitinssc@gmail.com',
        'sr.montemario@sanraffaele.it', 'ppetrucci@dongnocchi.it',
        'sr.flaminia@sanraffaele.it', 'antonella.dibernardini@anniazzurri.it'
    ],
    'Servizi_Specializzati': [
        'Fisioterapia, Riabilitazione', 'Medicina Generale, Diagnostica',
        'Riabilitazione, Formazione', 'Assistenza base, Riabilitazione',
        'Assistenza intensiva, Riabilitazione', 'Disturbi comportamentali',
        'Lungodegenza, RSA', 'Assistenza base, Riabilitazione',
        'Riabilitazione, Lungodegenza', 'Servizi ambulatoriali',
        'RSA estensiva, DCCG', 'Riabilitazione, Assistenza',
        'Mantenimento, DCCG', 'Telemedicina, Riabilitazione'
    ]
}

df = pd.DataFrame(data)

# Funzione per geocodificare gli indirizzi
@st.cache_data
def geocode_addresses(df):
    geolocator = Nominatim(user_agent="rsa_app")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
    
    locations = []
    for idx, row in df.iterrows():
        try:
            location = geocode(row['Indirizzo'])
            if location:
                locations.append({
                    'lat': location.latitude,
                    'lon': location.longitude
                })
            else:
                locations.append({'lat': None, 'lon': None})
        except Exception as e:
            st.error(f"Errore nella geocodifica per {row['Nome']}: {str(e)}")
            locations.append({'lat': None, 'lon': None})
        time.sleep(1)
    
    return pd.DataFrame(locations)

# Titolo dell'applicazione
st.title("Dashboard RSA ASL Roma 1")

# Tabs per diverse visualizzazioni
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📍 Mappa", "📊 Statistiche", "📋 Dettagli Strutture", "🔍 Confronto", "📖 Guida"])

with tab1:
    # Sidebar per i filtri della mappa
    st.sidebar.title("Filtri Mappa")
    selected_municipio = st.sidebar.multiselect(
        "Seleziona Municipi (opzionale)",
        sorted(df['Municipio'].unique())
    )

    selected_tipologia = st.sidebar.multiselect(
        "Seleziona Tipologie",
        sorted(df['Tipologia'].unique()),
        default=sorted(df['Tipologia'].unique())
    )

    # Geocodifica gli indirizzi per tutti i dati
    if 'coords' not in st.session_state:
        with st.spinner('Geocodifica degli indirizzi in corso...'):
            coords = geocode_addresses(df)
            st.session_state.coords = coords

    # Aggiungi le coordinate al DataFrame originale
    df_with_coords = df.copy()
    df_with_coords['lat'] = st.session_state.coords['lat']
    df_with_coords['lon'] = st.session_state.coords['lon']

    # Applica i filtri dopo aver aggiunto le coordinate
    mask = df_with_coords['Tipologia'].isin(selected_tipologia)
    if selected_municipio:  # Applica il filtro municipio solo se è stato selezionato qualcosa
        mask = mask & df_with_coords['Municipio'].isin(selected_municipio)
    
    filtered_df = df_with_coords[mask]

    # Crea la mappa
    m = folium.Map(location=[41.9028, 12.4964], zoom_start=12)

    # Aggiungi i marker alla mappa solo per le strutture filtrate
    for idx, row in filtered_df.iterrows():
        if pd.notnull(row['lat']) and pd.notnull(row['lon']):
            popup_html = f"""
                <b>{row['Nome']}</b><br>
                <b>Indirizzo:</b> {row['Indirizzo']}<br>
                <b>Municipio:</b> {row['Municipio']}<br>
                <b>Tipologia:</b> {row['Tipologia']}<br>
                <b>Posti letto:</b> {row['Posti_Letto']}<br>
                <b>Posti accreditati:</b> {row['Posti_Accreditati']}<br>
                <b>Telefono:</b> {row['Telefono']}<br>
                <b>Email:</b> {row['Email']}<br>
                <b>Servizi:</b> {row['Servizi_Specializzati']}
            """
            tooltip_html = f"""
                <div style='font-family: Arial; font-size: 12px;'>
                {row['Nome']}<br>
                Tipologia: {row['Tipologia']}<br>
                Posti: {row['Posti_Letto']}<br>
                Tel: {row['Telefono']}<br>
                Mail: {row['Email']}
                </div>
            """
            folium.Marker(
                [row['lat'], row['lon']],
                popup=folium.Popup(popup_html, max_width=300),
                tooltip=tooltip_html
            ).add_to(m)

    # Visualizza la mappa
    folium_static(m, width=1200, height=600)

with tab2:
    col1, col2 = st.columns(2)
    
    with col1:
        # Grafico distribuzione posti letto per municipio
        fig_posti = px.bar(
            df.groupby('Municipio')['Posti_Letto'].sum().reset_index(),
            x='Municipio',
            y='Posti_Letto',
            title='Distribuzione Posti Letto per Municipio'
        )
        st.plotly_chart(fig_posti, use_container_width=True)

        # Grafico rapporto posti accreditati/totali
        fig_accreditati = go.Figure()
        fig_accreditati.add_trace(go.Bar(
            name='Posti Totali',
            x=df['Nome'],
            y=df['Posti_Letto']
        ))
        fig_accreditati.add_trace(go.Bar(
            name='Posti Accreditati',
            x=df['Nome'],
            y=df['Posti_Accreditati']
        ))
        fig_accreditati.update_layout(
            title='Rapporto Posti Accreditati/Totali per Struttura',
            barmode='group',
            xaxis_tickangle=-45,
            height=600
        )
        st.plotly_chart(fig_accreditati, use_container_width=True)

    with col2:
        # Grafico distribuzione tipologie
        fig_tipologie = px.pie(
            df,
            names='Tipologia',
            title='Distribuzione Tipologie di Strutture'
        )
        st.plotly_chart(fig_tipologie, use_container_width=True)

        # Statistiche generali
        st.subheader("Statistiche Generali")
        tot_posti = df['Posti_Letto'].sum()
        tot_accreditati = df['Posti_Accreditati'].sum()
        n_strutture = len(df)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Totale Strutture", n_strutture)
        col2.metric("Totale Posti Letto", tot_posti)
        col3.metric("Totale Posti Accreditati", tot_accreditati)

with tab3:
    # Visualizzazione dettagliata delle strutture
    st.subheader("Dettagli delle Strutture")
    
    # Filtro per ricerca
    search = st.text_input("Cerca struttura per nome:")
    
    if search:
        filtered = df[df['Nome'].str.contains(search, case=False)]
    else:
        filtered = df
    
    # Mostra i dettagli in cards
    for _, row in filtered.iterrows():
        with st.expander(f"{row['Nome']} - Municipio {row['Municipio']}"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Indirizzo:** {row['Indirizzo']}")
                st.write(f"**Telefono:** {row['Telefono']}")
                st.write(f"**Email:** {row['Email']}")
                st.write(f"**Tipologia:** {row['Tipologia']}")
            with col2:
                st.write(f"**Posti Letto:** {row['Posti_Letto']}")
                st.write(f"**Posti Accreditati:** {row['Posti_Accreditati']}")
                st.write(f"**Servizi Specializzati:** {row['Servizi_Specializzati']}")

with tab4:
    # Tool di confronto tra strutture
    st.subheader("Confronto tra Strutture")
    
    col1, col2 = st.columns(2)
    with col1:
        struttura1 = st.selectbox("Seleziona prima struttura", df['Nome'].unique())
    with col2:
        struttura2 = st.selectbox("Seleziona seconda struttura", df['Nome'].unique(), index=1)
    
    if struttura1 and struttura2:
        df1 = df[df['Nome'] == struttura1].iloc[0]
        df2 = df[df['Nome'] == struttura2].iloc[0]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader(struttura1)
            st.write(f"**Tipologia:** {df1['Tipologia']}")
            st.write(f"**Posti Letto:** {df1['Posti_Letto']}")
            st.write(f"**Posti Accreditati:** {df1['Posti_Accreditati']}")
            st.write(f"**Municipio:** {df1['Municipio']}")
            st.write(f"**Servizi:** {df1['Servizi_Specializzati']}")
            
        with col2:
            st.subheader(struttura2)
            st.write(f"**Tipologia:** {df2['Tipologia']}")
            st.write(f"**Posti Letto:** {df2['Posti_Letto']}")
            st.write(f"**Posti Accreditati:** {df2['Posti_Accreditati']}")
            st.write(f"**Municipio:** {df2['Municipio']}")
            st.write(f"**Servizi:** {df2['Servizi_Specializzati']}")

        # Grafico comparativo
        comparison_data = {
            'Struttura': [struttura1, struttura2],
            'Posti Letto': [df1['Posti_Letto'], df2['Posti_Letto']],
            'Posti Accreditati': [df1['Posti_Accreditati'], df2['Posti_Accreditati']]
        }
        df_comp = pd.DataFrame(comparison_data)
        
        fig_comparison = go.Figure(data=[
            go.Bar(name='Posti Letto', x=df_comp['Struttura'], y=df_comp['Posti Letto']),
            go.Bar(name='Posti Accreditati', x=df_comp['Struttura'], y=df_comp['Posti Accreditati'])
        ])
        fig_comparison.update_layout(
            title='Confronto Posti Letto e Accreditati',
            barmode='group'
        )
        st.plotly_chart(fig_comparison, use_container_width=True)

        # Calcola e mostra le differenze percentuali
        st.subheader("Analisi Comparativa")
        diff_posti = abs(df1['Posti_Letto'] - df2['Posti_Letto'])
        diff_accreditati = abs(df1['Posti_Accreditati'] - df2['Posti_Accreditati'])
        
        col1, col2 = st.columns(2)
        col1.metric("Differenza Posti Letto", diff_posti)
        col2.metric("Differenza Posti Accreditati", diff_accreditati)

# Aggiungi pulsante per scaricare i dati
st.sidebar.markdown("---")
st.sidebar.subheader("Download Dati")
# Tab Guida
with tab5:
    st.header("Guida all'utilizzo della Dashboard RSA")
    
    st.subheader("🎯 Scopo della Dashboard")
    st.write("""
    Questa dashboard è stata progettata per aiutare utenti, famiglie e operatori sanitari a:
    - Trovare la struttura RSA più adatta alle proprie esigenze
    - Confrontare diverse strutture tra loro
    - Analizzare la distribuzione dei servizi nel territorio
    - Valutare la disponibilità di posti letto e servizi specializzati
    """)

    st.subheader("📱 Come utilizzare le diverse sezioni")
    
    with st.expander("📍 Mappa Interattiva"):
        st.markdown("""
        La mappa permette di visualizzare tutte le strutture RSA nel territorio:
        - Usa i filtri sulla sinistra per selezionare municipi specifici e/o tipologie di strutture
        - Passa il mouse sopra i marker per vedere le informazioni principali
        - Clicca sui marker per vedere tutti i dettagli della struttura
        - I filtri sono combinabili: puoi selezionare più municipi e più tipologie contemporaneamente
        """)

    with st.expander("📊 Statistiche"):
        st.markdown("""
        La sezione statistiche offre una visione d'insieme:
        - Distribuzione dei posti letto per municipio
        - Rapporto tra posti totali e accreditati
        - Tipologie di strutture disponibili
        - Metriche chiave come totale strutture e posti disponibili
        
        Usa questi dati per:
        - Identificare le zone con maggiore disponibilità
        - Valutare il livello di accreditamento delle strutture
        - Capire la distribuzione delle diverse tipologie di servizio
        """)

    with st.expander("📋 Dettagli Strutture"):
        st.markdown("""
        Questa sezione permette di:
        - Cercare strutture specifiche per nome
        - Visualizzare tutti i dettagli di ogni struttura
        - Accedere a informazioni di contatto e servizi specializzati
        
        Utile per:
        - Approfondire i servizi offerti da una struttura specifica
        - Trovare informazioni di contatto dettagliate
        - Valutare i servizi specializzati disponibili
        """)

    with st.expander("🔍 Confronto"):
        st.markdown("""
        Il tool di confronto permette di:
        - Selezionare due strutture da confrontare
        - Visualizzare le differenze in termini di posti e servizi
        - Analizzare graficamente le differenze
        
        Ideale per:
        - Prendere decisioni informate tra due opzioni
        - Valutare pro e contro di diverse strutture
        - Confrontare la capacità e i servizi offerti
        """)

    st.subheader("📊 Come interpretare i dati")
    st.markdown("""
    **Tipologie di strutture:**
    - **Mant. A**: Mantenimento alto (per pazienti con necessità di assistenza continua)
    - **Mant. B**: Mantenimento basso (per pazienti più autonomi)
    - **Intensivo**: Per pazienti che necessitano di cure intensive
    - **E.P.D.C.C.**: Estensiva Per Disturbi Cognitivo Comportamentali
    
    **Posti letto vs Posti accreditati:**
    - I posti accreditati sono quelli convenzionati con il SSN
    - Un alto rapporto posti accreditati/totali indica maggiore accessibilità economica
    
    **Criteri per scegliere la struttura migliore:**
    1. **Localizzazione**:
       - Vicinanza alla famiglia
       - Accessibilità della zona
       - Presenza di servizi nel quartiere
    
    2. **Tipologia di assistenza**:
       - Valutare il livello di assistenza necessario
       - Verificare la presenza di servizi specializzati richiesti
       - Controllare il rapporto personale/ospiti
    
    3. **Disponibilità e costi**:
       - Numero di posti accreditati
       - Liste d'attesa
       - Costi aggiuntivi per servizi extra
    
    4. **Servizi specializzati**:
       - Presenza di servizi riabilitativi specifici
       - Attività sociali e ricreative
       - Assistenza medica specialistica
    """)

    st.subheader("💡 Suggerimenti per l'uso ottimale")
    st.markdown("""
    1. Inizia dalla mappa per una visione d'insieme della zona di interesse
    2. Usa le statistiche per capire la distribuzione dei servizi
    3. Approfondisci i dettagli delle strutture che ti interessano
    4. Usa il tool di confronto per fare una scelta finale informata
    5. Scarica i dati completi se hai bisogno di fare analisi più approfondite
    """)
# Converti il DataFrame in CSV
@st.cache_data
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

csv = convert_df_to_csv(df)
st.sidebar.download_button(
    label="📥 Scarica dati completi (CSV)",
    data=csv,
    file_name='rsa_roma1_dati.csv',
    mime='text/csv'
)

# Footer con informazioni
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>Dashboard RSA ASL Roma 1 - Versione 1.0</p>
    <p>Dati aggiornati al 2024</p>
</div>
""", unsafe_allow_html=True)