class Group:

    def __init__(self, groupName, groupPath, groupType):
        super().__init__()
        self.name = groupName
        self.groupPath = groupPath
        self.groupType = groupType

        self.documents = []
        self.dWords = []
        self.wordsFiles = []

    def toString(self):
        return f"Group: {self.name}, Type: {self.groupType},\nPath: {self.groupPath}, Documents: {len(self.documents)}\n"
