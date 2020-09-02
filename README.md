# STN
Spreading Tweet News Project

All'interno della repository è presente:
- Relazione
- Slide
- App



## APP

Flusso d'esecuzione:
1. cartella `1_scraper`, download dei dati da Twitter (follower di Conte nel nostro caso). Comando: `python3 scraper_twitter.py`.
2. cartella `2_graph_builder`, crea il grafo basandosi sulle informazioni scaricate. Comando: `python3 graph.py`.
3. cartella `3_soil_simulation`, esegue la simulazione della diffusione. Comando: `soil TweetSpreadConfig.yml --csv`.
4. cartella `4_visualization`, crea e visualizza i risultati ottenuti. Comando: `python3 build_resulting_graphs.py`.
5. cartella `5_statistics`, calcola statistiche sui risultati ottenuti. Comando: `python3 stats.py`.



Old Datasets

https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/LW0BTB