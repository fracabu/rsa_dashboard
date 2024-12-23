# Dashboard RSA ASL Roma 1

## 📋 Descrizione
Dashboard interattiva per la visualizzazione e l'analisi delle strutture RSA nell'area dell'ASL Roma 1. La dashboard permette di esplorare, confrontare e analizzare i dati relativi alle strutture RSA, facilitando la scelta della struttura più adatta alle proprie esigenze.

## 🔧 Funzionalità Principali

### 📍 Mappa Interattiva
- Visualizzazione geografica di tutte le strutture RSA
- Filtri per municipi e tipologie di strutture
- Tooltip informativi al passaggio del mouse
- Popup dettagliati al click sui marker

### 📊 Statistiche
- Distribuzione dei posti letto per municipio
- Rapporto tra posti totali e accreditati
- Analisi delle tipologie di strutture
- Metriche chiave del sistema RSA

### 📋 Dettagli Strutture
- Ricerca strutture per nome
- Visualizzazione dettagliata delle informazioni
- Accesso rapido ai contatti
- Informazioni sui servizi specializzati

### 🔍 Confronto
- Confronto diretto tra due strutture
- Analisi comparativa dei servizi
- Visualizzazione grafica delle differenze
- Metriche comparative

### 📖 Guida
- Istruzioni dettagliate per l'utilizzo
- Spiegazione dei dati e delle metriche
- Criteri di scelta della struttura
- Suggerimenti per l'uso ottimale

## 🛠️ Requisiti Tecnici
```bash
streamlit==1.24.0
pandas==2.0.3
folium==0.14.0
streamlit-folium==0.13.0
geopy==2.3.0
plotly==5.15.0
```

## 🚀 Installazione e Avvio

1. Clona il repository:
```bash
git clone https://github.com/tuousername/dashboard-rsa.git
cd dashboard-rsa
```

2. Crea e attiva un ambiente virtuale:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Installa le dipendenze:
```bash
pip install -r requirements.txt
```

4. Avvia l'applicazione:
```bash
streamlit run app.py
```

## 📦 Struttura del Progetto
```
dashboard-rsa/
├── app.py              # Applicazione principale
├── requirements.txt    # Dipendenze
├── README.md          # Documentazione
└── data/              # Dati delle strutture
```

## 📊 Dataset
Il dataset include informazioni su 14 strutture RSA nell'area dell'ASL Roma 1, con dettagli su:
- Nome e localizzazione
- Posti letto totali e accreditati
- Tipologie di assistenza
- Servizi specializzati
- Contatti e informazioni amministrative

## 🤝 Contributi
Siete invitati a contribuire al progetto! Per farlo:
1. Fate un fork del repository
2. Create un branch per le vostre modifiche
3. Inviate una pull request

## 📝 Note di Rilascio
- Versione 1.0.0
  - Rilascio iniziale con funzionalità base
  - Integrazione mappa interattiva
  - Sistema di confronto strutture
  - Guida utente completa

## 📄 Licenza
Questo progetto è distribuito sotto licenza MIT. Vedere il file `LICENSE` per maggiori dettagli.

## 👥 Team
- Sviluppato per ASL Roma 1
- Mantenuto da [Nome del Team/Organizzazione]

## 📞 Contatti
Per supporto o informazioni:
- Email: [inserire email]
- Issue Tracker: GitHub Issues

## 🙏 Ringraziamenti
- ASL Roma 1 per i dati e il supporto
- OpenStreetMap per i dati cartografici
- Streamlit per il framework di sviluppo
