
class PredictedClass():

    def __init__(self, identifier:int, label:str, color:str):
        self.id = identifier
        self.label = label
        self.color = color
        self.score = None
        self.boxLimits = []

class ClassList():

    def __init__(self):
        self.classes = []

    def addClass(self, identifier:int, label:str, color:str):

        filteredList = [c for c in self.classes if c.id == identifier]

        if len(filteredList) > 0:
            raise ValueError('This List already have that id')

        predictedClass = PredictedClass(identifier, label, color)

        self.classes.append(predictedClass)

    def getClassByPredictedId(self, classId:int) -> PredictedClass:
        try:
            return next(predictedClass for predictedClass in self.classes if predictedClass.id == classId)
        except StopIteration:
            raise ValueError('Id not found')

