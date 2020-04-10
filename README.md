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

Questi risultati sono ottenuti tramite i dataset reperibili sotto.

## Newsgroup

Il dataset e' formato da 19 gruppi.

Multi-variate Bernulli supera il multivariate 

![News Result](/results/NewsResult.png)

## Webkb

![Webkb Result](/results/WebkbResult.png)

## Sector 48

![Sector Result](/results/SectorResult.png)

## Film

Il dataset e formato solo da due gruppi (nel dataset e presente anche una terza categoria che e' stata rimossa), positivo e negativo.

Multi-variate Bernulli si comporta gia' bene con poche parole nel dizionario.
Mentre il Multivariate si comporta bene solo con l'utilizzo massimo delle parole nel dizionario. 

![Film result](/results/FilmResult.png)

Datasets:

News: http://www.cs.cmu.edu/afs/cs/project/theo-11/www/naive-bayes/20_newsgroups.tar.gz

Sector: http://archive.ics.uci.edu/ml/machine-learning-databases/00239/corpus.zip

Webkb: http://www.cs.cmu.edu/afs/cs.cmu.edu/project/theo-20/www/data/webkb-data.gtar.gz

Film: http://ai.stanford.edu/~amaas/data/sentiment/ 
