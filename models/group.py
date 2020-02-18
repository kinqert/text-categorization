from models.word import Word, GroupedWord, Dictionary

class Group:

    def __init__(self, name, path, type):
        super().__init__()
        self.name = name
        self.path = path
        self.type = type

        self.dictionary = Dictionary()
        self.documents = []
    
    def readDocuments(self):
        for document in self.documents:
            document.readWords()

            for word in document.dictionary.words:
                self.dictionary.searchAndAddWord(GroupedWord(word.text, self, word.counted))

    def toString(self):
        return f"Group: {self.name}, Type: {self.groupType},\nPath: {self.groupPath}, Documents: {len(self.documents)}\n"
