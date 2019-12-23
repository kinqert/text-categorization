class Group:
    group = ""
    dWords = []
    wordsFiles = []


    def __init__(self, group, dWords = [], wordsFiles = []):
        super().__init__()
        self.group = group
        self.dWords = dWords
        self.wordsFiles = wordsFiles