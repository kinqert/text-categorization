from models.word import CountedWord, GroupedWord
from models.dictionary import Dictionary

from util.defaultBar import defaultProgress

class Group:

    def __init__(self, name, path, type):
        super().__init__()
        self.name = name
        self.path = path
        self.type = type

        self.dictionary = Dictionary()
        self.documents = []

        self.totalCountedWords = 0
    
    def readDocuments(self):
        self.dictionary.clean()

        print(f"Start reading group {self.name}, type: {self.type}")
        bar = defaultProgress(len(self.documents)).start()
        i = 0
        for document in self.documents:
            document.readWords()

            for word in document.dictionary.words:
                self.dictionary.searchAndAddWord(GroupedWord(word.text, self, word.counted, 1))
            
            document.clearReadedWords()
            i += 1
            bar.update(i)
        self.setTotalCountedWords()
        bar.finish()
        print(f"Done reading group {self.name}")
        
    def setTotalCountedWords(self):
        self.totalCountedWords = 0
        for word in self.dictionary.words:
            self.totalCountedWords += word.counted

    def __str__(self):
        return f"Group: {self.name}"
