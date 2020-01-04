import os
import sys

from threading import Thread, Lock, Event
from time import time, sleep
from queue import Queue

from models.dataset import Dataset
from models.group import Group
from models.document import Document

def createDataset(datasethName):
    dataset = Dataset(datasethName)
    groupQueue = Queue()

    for groupName in os.listdir(dataset.trainPath):
        trainGroup = Group(groupName, f"{dataset.trainPath}/{groupName}" , "train")
        testGroup = Group(groupName, f"{dataset.testPath}/{groupName}", "test")

        dataset.trainGroups.append(trainGroup)
        dataset.testGroups.append(testGroup)

        groupQueue.put(trainGroup)
        groupQueue.put(testGroup)
    
    threads = []
    maxThreads = 16

    for i in range(0, maxThreads):
        t = Thread(target=createDocumentsForGroup, args=(groupQueue,))
        t.start()
        threads.append(t)

    for i in range(0, maxThreads):
        threads[i].join()
    
    return dataset
    
def createDocumentsForGroup(groupQueue: Queue):
    while not groupQueue.empty():
        group = groupQueue.get()
        print(f"Creating group {group.name} for {group.groupType}...")
        nameDirs = os.listdir(group.groupPath)
        print(f"Total documents for {group.name}-{group.groupType}: {len(nameDirs)}")
        print(f"Dir list: {nameDirs}")
        for fileName in nameDirs:
            doc = Document(fileName, f"{group.groupPath}/{fileName}")
            group.documents.append(doc)
        print(f"Done creating group {group.name}-{group.groupType}!\nDocument size:{len(group.documents)}")

