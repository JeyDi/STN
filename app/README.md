## APP

Flusso d'esecuzione:
1. cartella `1_scraper`, download dei dati da Twitter (follower di Conte nel nostro caso). Comando: `python3 scraper_twitter.py`.
2. cartella `2_graph_builder`, crea il grafo basandosi sulle informazioni scaricate. Comando: `python3 graph.py`.
3. cartella `3_soil_simulation`, esegue la simulazione della diffusione. Comando: `soil TweetSpreadConfig.yml --csv`.
4. cartella `4_visualization`, visualizza i risultati ottenuti. Comando: `python3 viusualize_graph.py`.