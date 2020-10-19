# STN
**Spreading Tweet News Project.**

Progetto realizzato da:

- Lidia Alecci - 852501
- Andrea Guzzo - 761818
- Vittorio Maggio - 817034
- Manuel Zanaboni - 816105



All'interno della repository sono presenti le seguenti risorse

- **Relazione**: report finale su analisi e spiegazione del progetto
- **Slide**: presentazione dei risultati e del lavoro
- **Applicazione Streamlit**: Dashboard interattiva che consente di effettuare gli esperimenti (simulatore)



# Introduzione

Una persona passa mediamente 5 anni e 4 mesi della propria vita sui social network, secondo uno studio condotto dall’agenzia di marketing americana Mediakix. 

Sui social network ci informiamo e discutiamo di tutto ormai, eppure non è sempre un'idea saggia credere a tutto quello che si legge su internet, alcune notizie sono infatti pilotate per raggiungere in minor tempo più persone possibili. Tale obiettivo è raggiunto impiegando i bot. 

Quest'ultimi, come qualunque cosa, possono essere sfruttati per motivi nobili (informare di fatti reali che necessitano di raggiungere la popolazione il più in fretta possibile) o per diffondere fake news.

All'interno del progetto è stato realizzato un simulatore multi agente che consente di studiare la miglior collocazione dei bot all’interno di una rete sociale, in modo da massimizzare il numero di persone potenzialmente raggiunte dalla diffusione di un contenuto sfruttando modelli epidemiologici.



## APP

L'applicazione è stata realizzata con Streamlit in modo da avere a disposizione una dashboard grafica che consenta la configurazione degli esperimenti e la visualizzazione di statistiche e informazioni a supporto.



### Lanciare l'applicazione

Per lanciare l'applicazione consigliamo di creare un virtual environment con Python 3.7

All'interno della cartella di streamlit (streamlit_app) è presente il file con la definizione delle librerie necessarie, per installarle (dopo aver attivato l'ambiente virtuale) fare: `pip install -r requirements.txt`

Una volta installato le librerie è sufficiente posizionarsi all'interno della cartella: streamlit_app e lanciare da terminale: `streamlit run main.py`



### Funzionalità

Le funzionalità principali dell'applicazione sono:

1. Scraping di nuove informazioni da twitter usando la libreria di Twint
2. Creazione del grafo a partire da dati in formato .csv
3. Configurare e lanciare nuove simulazioni con soil
4. Visualizzare le informazioni delle simulazioni e i grafici di valutazione
5. Calcolare statistiche finali

All'interno dell'applicazione sono presenti sulla sinistra una finestra di configurazione delle funzionalità, mentre al centro la schermata principale con i risultati delle esecuzioni.