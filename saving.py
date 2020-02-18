import sys
import os
import pickle

from models.dataset import Dataset

def createDirIfNotExist(dir):

    if os.path.isdir(dir) is False:
        os.mkdir(dir)

def saveDataset(dataset: Dataset):

    dataPath = f"{sys.path[0]}/data/{dataset.name}/save/"
    datasetPath = f"{sys.path[0]}/data/{dataset.name}/save/{dataset.name}.pkl"

    createDirIfNotExist(dataPath)

    with open(datasetPath, "wb") as file:
        pickle.dump(dataset, file, pickle.HIGHEST_PROTOCOL)

def loadDataset(name):
    resultPath = f"{sys.path[0]}/data/{name}/save/{name}.pkl"

    with open(resultPath, "rb") as file:
        return pickle.load(file)
    
