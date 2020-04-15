# Text Categorization

Progetto per il corso di AI per l'università degli studi di Firenze

## Dipendenze

Le seguenti dipendenze sono necessarie per il funzionamento del programma
- Sklearn
- Matplotlib
- PrettyTable
- Progressbar

```bash
pip install sklearn matplotlib progressbar PrettyTable
```

## Argomenti

### Comandi princpali

- import-dataset: Importa un dataset
  - -s | --split: il dataset viene diviso in due gruppi train e test con rapporto 80:20
- start-training: Elabora i dati del dataset specificato
- show-datasets: Mostra i dataset salvati
- plot-risult: Mostra il grafico con i risultati del test precedente

## Risultati

Data la natura casuale della suddivisione dei file in Train e Test, i risultati ottenuti possono variare, anche se in maniera lieve.

Questi risultati qui riportati sono ottenuti tramite i dataset reperibili nella sezione dataset.

### Newsgroup

Il dataset é formato da 19 gruppi, e sono stati utilizzati tutti.

Multi-variate Bernulli supera il multinomial in dizionari relativamente piu' piccoli, ma al aumentare delle parole il multinomial ha una performance superiore.
Ma in entrambi casi ci sa un miglioramento in termini di accuratezza al amuentare del numero di parole considerate. Arrivando fino al 85% di accuratezza per quanto riguarda il multinomial, e 80% per il multi-variate.

![News Result](/results/NewsResult.png)

### Webkb

Il dataset Webkb é formato da 7 gruppi, ma ne sono state utilizzate solo 4: student, faculty, staff e course.


![Webkb Result](/results/WebkbResult.png)

### Sector 48

![Sector Result](/results/SectorResult.png)

### Film

Il dataset é formato solo da due gruppi (nel dataset e presente anche una terza categoria che e' stata rimossa), positivo e negativo.

Multi-variate Bernulli si comporta già bene con poche parole nel dizionario.
Il Multivariate ottiene delle prestazioni analoge al multi-variate bernulli, ma con delle prestazioni leggermente inferiori

![Film result](/results/FilmResult.png)

## Datasets:

News: http://www.cs.cmu.edu/afs/cs/project/theo-11/www/naive-bayes/20_newsgroups.tar.gz

Sector: http://archive.ics.uci.edu/ml/machine-learning-databases/00239/corpus.zip

Webkb: http://www.cs.cmu.edu/afs/cs.cmu.edu/project/theo-20/www/data/webkb-data.gtar.gz

Film: http://ai.stanford.edu/~amaas/data/sentiment/ 
