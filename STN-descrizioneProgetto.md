# Cosa fare

## **Domande di ricerca**

1. All'interno di una rete sociale massimizzare (simulare) il numero di persone che visualizzano una notizia in un numero di step determinato (step = tempo di diffusione) 
2. Dove è possibile posizionare i nodi (bot, ma non gli opinion leader) che generano i contenuti per massimizzare (simulare) la diffusione ed eventualmente minimizzare (simulazione) il tempo di diffusione
3. Distinguere chi è venuto in contatto con una notizia pubblicata da un determinato tipo di utente (bot o opinion leader):  
4. Studiare diffusione di contenuti in base a particolari caratteristiche (topic)
5. Sviluppi futuri (ma non trattati): studiare ottimizzazione della rete (seguire persone tramite bot o studiare come la rete può evolversi in base agli utenti e ai contenuti)

** tempo = facoltativo in un secondo momento, al massimo simulare e basta tutto allo stesso tempo

## Assunzioni / Ipotesi

Cosa ci aspettiamo dal modello?

- Opinion Leader influenza maggiore sulla rete rispetto ai Bot
- Bot hanno un'influenza più sparsa (ampia)
- Opinion Leader hanno un'influenza maggiore sulla community
- Alcuni utenti influenzano pochi vicini perchè leggono una notizia particolare
- Cambiando il posizionamento dei bot (ma anche il numero dei bot esistenti) cambia (aumenta o diminuisce) la diffusione, non solo più sparsa, ma anche più densa. (cambia percentuale di diffusione, contagio)
- Community o gruppi di persone che seguono un particolare topic verranno infettate rispetto quel topic, ma ci saranno delle persone che verranno infettate anche su altri topics secondari o terziari.

## **Composizione della rete**

- Bot che generano o ripostano contenuti: contenuti pubblicati hanno un livello basso e una frequenza rapida
- Opinion Leader: tipicamente influencer, persone che hanno una community di follower e tipicamente pubblicano contenuti meno frequenti ma di qualità maggiore rispetto i bot per la loro rete di influenza
- Utenti normali: utenti passivi o attivi che leggono, interagiscono e condividono notizie nella rete sociale
- Relazioni: Follower / Following = il grafo è quindi orientato

**Eventualmente generalizzare la relazione, ovvero togliere Follower e Following in modo da studiare una generica rete sociale

Posizionamento dei bot:

- Evitare sempre il nodo centrale (Opinion Leader)
- Posizione random
- Nodi di grado alto (molto connessi in-bound): attenzione a non tenere nodi di grado alto
- Alta Betweenness
- Mettere un numero n di bot all'interno di una community

**attenzione nelle simulazioni a mantenere un numero confrontabile di bot a disposizione

## **Dati**

- Rete costruita su conte a partire da Twitter (che si ferma al secondo grado di profondità)
- Usare rete simulata Barabasi e Albert (scale_free_graph)
- Eventualmente modificare la rete a mano (cambiando relazioni, modificando opinion leaders, inserendo bot, ...)

** confrontare diverse reti come validazione

## **Modelli e caratteristiche**

- Opinion Leader hanno una qualità di generazione del materiale più alto rispetto ai bot
- Utenti hanno comunque probabilità di generare e ricondividere delle notizie (probabilità più bassa rispetto a Opinion Leader e Bot che sono i generatori dei contenuti primari)
- variabile infezione 0: utente (persona cerca direttamente un contenuto, è infetta per conto suo senza ricevere informazione dagli altri) = alla fine tutti sono utenti
- variabile infezione 1 = persona infettata da un bot oppure da un'altra persona infettata da un bot
- variabile infezione 2 = persona infettata da un opinion leader o da un'altra persona infettata da un opinion leader

** relazione di infezione è ricorsiva (e così via...)

- Topic per un contenuto: generare dei topics per caratterizzare l'utente oppure il contenuto (utente x interessato di politica e di sport sarà più incline a guardare contenuti di quei due topics)

Stati a disposizione del modello (Modello di diffusione epidemiologica)

- Suscettibile (non esposto) = utente normale che non è ancora venuto a contatto
- Esposto = chi visualizza il contenuto ed è venuto a contatto con la notizia, ma non ha fatto nessuna azione (retweet, condivisione)
- Infetto = contributors: ha visto, è stato esposto e ha condiviso, ha parlato di quel contenuto

Modello multi agente = il modello di diffusione epidemiologica viene valutato su ogni utente che è indipendente ed è un agente singolo

**Eventualmente inserire un bias come variabile di ambiente random per limitare la visibilità o altro(??)

**Generare caratteristiche della rete (clustering, divisione, aggregazioni, ....) che possono arricchire le caratteristiche per i modelli (ad esempio community) (??)

## **Tools**

- Twint: Scraper per Twitter
- Networkx
- PyCx
- Gephi (per visualizzazione del grafo)
- Plotly (per visualizzazione del grafo)
- Soil