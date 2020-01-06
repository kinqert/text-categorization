import sys
import os

from threading import Thread, Lock, Event
from time import time, sleep
from queue import Queue

from models.dataset import Dataset
from models.group import Group
from models.word import Word
from models.document import Document
from setting import Setting

def startTraining(dataset: Dataset):
    print("Starting training")
    documentsQueue = Queue()
    print("document queue created")
    for group in dataset.trainGroups:
        print(f"reading document {group.name}")
        for document in group.documents:
            documentsQueue.put(document)
    
    print(f"Queue size {documentsQueue.qsize()}")
    threads = []
    print(f"reading files with {Setting.max_thread} threads")
    for i in range(0, Setting.max_thread):
        print(f"Starting thread {i}...")
        readThread = Thread(target=readDocuments, args=(documentsQueue,))
        readThread.start()
        threads.append(readThread)

    for thread in threads:
        thread.join()

    print("Done reading")
    

def readDocuments(documentQueue: Queue):
    while not documentQueue.empty():
        document = documentQueue.get()
        file = open(document.documentPath, 'r', encoding= "ISO-8859-1")

        totalWords = []
        for line in file.readlines():
            words = str(line).split(" ") # Add here more separator for testing
            totalWords += words
        
        for word in totalWords:
            document.searchAndAddWord(Word(word))
        sleep(0.0001)