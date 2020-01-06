from threading import Thread, Event
from time import sleep
from queue import Queue

import matplotlib.pyplot as plt

from models.dataset import Dataset
from setting import Setting

def plotWordsCountForAllDocuments(dataset: Dataset):
    wordTimesAxis = []

    wordQueue = Queue()
    queueDone = Event()

    loadWordThread = Thread(target=loadWordQueue, args=(dataset, wordQueue, queueDone, ))
    loadWordThread.start()

    threads = [] 
    threads.append(loadWordThread)

    remainingThread = 1
    if (Setting.max_thread - 1 >= 1):
        remainingThread = Setting.max_thread - 1
    
    for i in range(0, remainingThread):
        countThread = Thread(target=countWordsTimes, args=(wordQueue, wordTimesAxis, queueDone, ))
        countThread.setDaemon(True)
        countThread.start()
        threads.append(countThread)
    
    for thread in threads:
        thread.join()
    
    print("Plot created")
    
    plt.plot(wordTimesAxis)
    plt.ylabel('Number of words')
    plt.xlabel('Number of count')
    plt.show()

def loadWordQueue(dataset: Dataset, wordQueue: Queue, queueDone: Event):
    for group in dataset.trainGroups:
        for document in group.documents:
            for word in document.words:
                wordQueue.put(word)
    
    queueDone.set()

def countWordsTimes(wordQueue: Queue, wordTimesAxis, queueDone: Event):
    while not queueDone.isSet():
        while not wordQueue.empty():
            word = wordQueue.get()
            if len(wordTimesAxis) > word.counted and wordTimesAxis[word.counted] != None:
                wordTimesAxis[word.counted] += 1
            else:
                wordTimesAxis.insert(word.counted + 1, 1)

            sleep(0.0001)