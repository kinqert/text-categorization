import sys
import os

from models.dataset import Dataset

def createDirIfNotExist(dir):

    if os.path.isdir(dir) is False:
        os.mkdir(dir)

def saveDataset(dataset: Dataset):

    resultPath = f"{sys.path[0]}/data/{dataset.name}/results"

    createDirIfNotExist(resultPath)
    
    for group in dataset.trainGroups:
        groupPath = f"{resultPath}/{group.name}"
        
        file = open(groupPath, "w")

        for document in group.documents:
            file.write(f"Documnet: {documemt.documentName} [")
            for word in document.words:
                file.write(f"'word: {word.word}, counted: {word.counted}'")
            file.write("]")
        file.close()
        
