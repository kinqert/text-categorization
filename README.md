# Text Categorization

Progetto per il corso di AI per l'università degli studi di Firenze.

text-categorization è un software, che serve per studiare l'andamento predittivo di due diversi modelli: Il Multi-variate Bernolli e il Multinomial.

Si vuole ottenere gli stessi risultati di [(McCallum & Nigam, 1998)](/documents/text-categorization.pdf)

Nel multinomial è presente anche un diverso approccio per la feature selection, che viene chiamato [KL-Divergence](/documents/kl.pdf).

## Dipendenze

Le seguenti dipendenze sono necessarie per il funzionamento del programma
- Sklearn
- Matplotlib
- PrettyTable
- Progressbar

```bash
pip install sklearn matplotlib progressbar PrettyTable
```

## Struttura

La struttra delle classi è la seguente.

![uml](documents/uml/UMLCompleto.jpg)

### Descrizione classi

Dataset: Classe principale che gestisce tutta la struttura, si occupa di leggere i gruppi, creare il dizionario pesato e effettua i test.

Group/Document: Classi che interpretano la gerarchia della directory del dataset. 

GroupedWord/DocumentWord: Classi che rappresentano la parola trovata, rispettivamente per le classi Group e Document. (Vedi sotto la modalità di raggruppamento)

Dictionary: Classe che gestisce le parole (GroupedWord/CountedWord) in modo ordinato e utilizza la ricerca binaria per ottenere una ottima efficenza.

WeightedDictionary: Classe astratta che eredita da Dictionary. Ma diversamente da Dictionary le sue parole sono dei WeightedWordVector.

MBMWeightedDictionary, MMWeightedDictionary: Classi che implementano il WeightedDictionary, e calcolano i parametri a seconda del modello predittivo Multi-variate o Multinomial.

WeightedWordVector: Classe astratta che contiene al suo interno un vettore di GroupedWord pari al numero delle classi totali. Si occupa di calcolare i parametri relativi alla parola data la classe.

MBMWeightedWordVector, MMWeightedWordVector: Classi che implementano WeightedWordVector, e creano i pesi a seconda del modello predittivo.

Test: Classe che tiene traccia dei risultati di un particolare test.

### Sequenza train e test

Qui viene mostrata la sequenza dei principali processi in train e test.

![flow train test](documents/uml/Flow-train-test.jpg)

### Grouping

Questa è la visualizzazione della modalità di raggruppamento. In alto la sequenza di raggruppamento in basso la relazione con le classi.

![Grouping](documents/uml/grouping.jpg)

## Comandi

Il software prevede 5 comandi principali, più eventuali argomenti posizionali che possono essere sia opzionali che obbligatori a seconda del comando.

### import-data

Questo comando serve per importare il dataset nella directory 'data' del progetto. Può anche essere aggiunta manualmente, semplicemente copiando il dataset nella directory e assicurandosi che i dati siano divisi in 'train' e 'test'.

Argomenti posizionali:
- -p | --path: Serve per indicare il percorso alla cartella contenente il dataset. (Obbligatorio)
- -s | --split [ratio]: Indica che il dataset deve essere diviso in 'train' e 'test', può anche essere indicato il rapporto di suddivisione. Default: 0.2 (80:20)
- -n | --name [name]: Imposta il nome da dare al dataset 

### start-learning

Questo comando inizia a leggere il dataset, e crea il dizionario con i suoi parametri.

Argomenti posizionali:
- -n | --name [name]: Il nome del dataset selezionato. (Obbligatorio)
- -sw | --stop-words [words ...]: Indica quali sono le stop words da rimuovere. Queste parole non verranno aggiunte al dizionario.
- -he | --headers [headers ...]: Se il dataset ha degli headers, che devono essere rimossi per non comprometere il risultato dei test, vengono indicati qui l'inizi delgli headers. (Esempio in news é stato indicato come headers: "Newsgroups:")
- -fr | --fast-reading: Imposta questo parametro per avere una lettura più veloce del dataset, questo in pratica rimuove la fase di tokenization e le parole saranno divise medianti gli spazi, questo comporta un maggior numero di parole trovate durante la lettura.

### start-testing

Effettua i test per tutti i file della sezione 'test' del dataset scelto.

Argomenti posizionali:
- -n | --name [name]: Il nome del dataset selezionato. (Obbligatorio)
- -fl | --feature-lenght [V ...]: Imposta il numero massimo di parole del dizionario per la feature selection, indicare con -1 se si vogliono usare tutte le parole.
- -kl | --kl-feature: Imposta come feature selection la versione KL al posto della informazione mutuale. Questo avviene solo per il modello multinomiale.

### plot-result

Mostra i risultati del test precedente.

Argomenti posizionali:
- -n | --name [name]: Il nome del dataset selezionato. (Obbligatorio)

### show-datasets

Mostra i datasets disponibili.

## Risultati

Data la natura casuale della suddivisione dei file in Train e Test, i risultati ottenuti possono variare, anche se in maniera lieve. I risultati qui riportati sono ottenuti tramite i dataset reperibili nella sezione dataset.

Sono stati utilizzati i 4 datasets scelti, sono stati messi a confronto i due modelli predittivi ed è stato analizato il comportamento delle due varianti di feture selection. 

### Newsgroup

Il dataset è formato da 19 gruppi e sono stati utilizzati tutti. Come headers è stato impostato "Newsgroups:".

Multi-variate Bernulli supera il multinomial in dizionari relativamente più piccoli, ma al aumentare delle parole il multinomial ha una performance superiore.
In entrambi casi si ha un miglioramento in termini di accuratezza al aumentare del numero di parole considerate. Arrivando fino al 85% di accuratezza per quanto riguarda il multinomial, e 80% per il multi-variate.

In questo caso il modello multinomiale, con il KL, ottiene un maggior incremento nell'accuratezza rispetto all'informazione mutuale.

#### Mutual information

![News Result](/results/plots/newsIM.png)

#### KL feature-selection

![News Result](/results/plots/newsKL.png)

### Webkb

Il dataset Webkb è formato da 7 gruppi, ma ne sono state utilizzati solo 4: student, faculty, staff e course.

Qui possiamo notare come il multi-variate già da subito ha un accuratezza molto elevata, con un massimo a 100 parole, e tiene un andamento costante.
Nel caso multinomiale si ha un accuratezza minore rispetto al multi-variate nel caso dei dizionari piccoli, e va ad aumentare man mano che le parole del dizionario aumentano.

Anche qui con la versione KL si ottengono dei risultati migliori.

#### Mutual information

![Webkb Result](/results/plots/webkbIM.png)

#### KL feature-selection

![Webkb Result](/results/plots/webkbKL.png)

### Sector 48

Il dataset è formato da categorie con vari sotto gruppi, sono stati quindi tutti trattati come gruppi diversi, e ne sono risultati in totale 48.

Qui il divario con poche parole è più ampio, e il multinomial supera il multi-variate quando ha all'incirca 5000 parole nel dizionario.

In questo caso la versione KL per la feature selection si compora peggio rispetto all'informazione mutuale e non si ottengono performance migliori rispetto al multivariate, fino a quando non vengono usate tutte le parole.

#### Mutual information

![Sector Result](/results/plots/Sector48IM.png)

#### KL feature-selection

![Sector Result](/results/plots/Sector48KL.png)

### Film

Il dataset è formato solo da due gruppi positivo e negativo. (nel dataset e presente anche una terza categoria che è stata rimossa)

Entrambi qui si comportano bene già con poche parole e tengono un andamento più o meno costante.

Qui abbiamo poca differenza tra il KL e l'informazione mutuale.

#### Mutual information

![Film result](/results/plots/filmIM.png)

#### KL feature-selection

![Film result](/results/plots/filmKL.png)

## Conclusioni

In generale il Multi-variate Bernulli Model supera il Multinomial, quando vengono selezionate relativamente poche parole dal dizionario, mentre il Multinomial tende ad avere una maggior accuratezza con l'utilizzo completo delle parole nel dizionario.

Per quanto riguarda le due tipologie di feature selection, la versione KL è quella che ottiene migliori risultati la maggior parte delle volte, ma non sempre accade come nel caso del dataset 'Sector48'.

## Riferimenti

[Testo assegnato](/documents/Adreani.pdf)

[(McCallum & Nigam, 1998)](/documents/text-categorization.pdf)

[KL-Selection](/documents/kl.pdf)

## Datasets:

News: http://www.cs.cmu.edu/afs/cs/project/theo-11/www/naive-bayes/20_newsgroups.tar.gz

Sector: http://archive.ics.uci.edu/ml/machine-learning-databases/00239/corpus.zip

Webkb: http://www.cs.cmu.edu/afs/cs.cmu.edu/project/theo-20/www/data/webkb-data.gtar.gz

Film: http://ai.stanford.edu/~amaas/data/sentiment/ 
