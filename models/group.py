from models.word import CountedWord, GroupedWord, Dictionary

from progressbar import ProgressBar, Percentage, Bar

class Group:

    def __init__(self, name, path, type):
        super().__init__()
        self.name = name
        self.path = path
        self.type = type

        self.dictionary = Dictionary()
        self.documents = []
    
    def readDocuments(self):
        self.dictionary.clean()

        print(f"Start learning group {self.name}, type: {self.type}")
        bar = ProgressBar(len(self.documents), [Percentage(), Bar()]).start()
        i = 0
        for document in self.documents:
            document.readWords()

            for word in document.dictionary.words:
                self.dictionary.searchAndAddWord(GroupedWord(word.text, self, word.counted, 1))
            
            document.clearReadedWords()
            i += 1
            bar.update(i)
        bar.finish()
        print(f"Done learning group {self.name}")

    def __str__(self):
        return f"Group: {self.name}"
