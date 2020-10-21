import torch
import json
from datetime import datetime
from torchvision import transforms
from PIL import Image
from ElementDrawer import ElementDrawer
from PredictedClass import ClassList
from src.Event import Event
from core.definitions import BACKGROUND_RGB, WITH_MASK_RGB, WITH_MASK_AND_GLASSES_RGB, WITH_GLASSES_RGB, CLEAN_RGB, MASK, GLASSES, FACE_SHIELD, WITH_FACE_SHIELD_RGB, INFRACTION_ID
from core.definitions import MASK, GLASSES, FACE_SHIELD, GLASSES_AND_MASK

class IAModel():
    def __init__(self, modelPath: str):
        classes = ClassList()
        # classes.addClass(0, 'background', BACKGROUND_RGB)
        # classes.addClass(1, 'with_mask', WITH_MASK_RGB)
        # classes.addClass(2, 'with_glasses', WITH_GLASSES_RGB)
        # classes.addClass(3, 'with_mask_and_glasses', WITH_MASK_AND_GLASSES_RGB)
        # classes.addClass(4, 'with_face_shield', WITH_FACE_SHIELD_RGB)
        # classes.addClass(5, 'clean', CLEAN_RGB)
        classes.addClass(0, 'background', BACKGROUND_RGB)
        classes.addClass(1, MASK, WITH_MASK_RGB)
        classes.addClass(2, GLASSES, WITH_GLASSES_RGB)
        classes.addClass(3, GLASSES_AND_MASK, WITH_MASK_AND_GLASSES_RGB)
        classes.addClass(4, FACE_SHIELD, WITH_FACE_SHIELD_RGB)
        classes.addClass(5, 'INFRACCION', CLEAN_RGB)
        
        self.modelPath = modelPath
        self.model = torch.load(self.modelPath, map_location='cpu')
        print('\nLoaded checkpoint from epoch %d.\n' % (self.model['epoch'] + 1))
        self.model = self.model['model'].to(torch.device('cpu')).eval()
        self.classes = classes
        self.device = torch.device('cpu')
        self.detectedClassesPrevious = []

    def detect(self, original_image, min_score:float ,max_overlap:float, max_objects:int, elementsConfiguration:str, app) -> Image:
        # Transforms needed for SSD300 (we are using torchvision to apply image tranformation) -> https://pytorch.org/docs/stable/torchvision/transforms.html
        resize = transforms.Resize((300, 300))
        to_tensor = transforms.ToTensor()
        normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                        std=[0.229, 0.224, 0.225]) # We use the standard transformation for RGB images - More info can be found here https://discuss.pytorch.org/t/understanding-transform-normalize/21730/22

        image = normalize(to_tensor(resize(original_image)))
        image = image.to(self.device)
        predicted_locs, predicted_scores = self.model(image.unsqueeze(0)) # Unsqueeze -> Returns a new tensor with a dimension of size one inserted at the specified position.

        # Run the detection over locations
        det_boxes, det_labels, det_scores = self.model.detect_objects(predicted_locs, predicted_scores, min_score=min_score,
                                                                    max_overlap=max_overlap, top_k=max_objects)

        det_boxes = det_boxes[0].to('cpu')
        det_labels = det_labels[0].to('cpu').tolist() # returns list of ints
        det_scores = det_scores[0].to('cpu')

        # Transform back to original image dimensions
        original_dims = torch.FloatTensor(
            [original_image.width, original_image.height, original_image.width, original_image.height]).unsqueeze(0)
        det_boxes = det_boxes * original_dims

        annotated_image = original_image

        if det_labels == [0]:
            return original_image

        currentDetectedClasses = []

        for labelId, box, score in zip(det_labels, det_boxes.tolist(), det_scores):
            predictedClass = self.evaluateElementsConfiguration(prediction=self.classes.getClassByPredictedId(labelId), elementsDict=elementsConfiguration)
            currentDetectedClasses.append(predictedClass)

            if (not predictedClass):
                return original_image

            boxLimits = box
            score = round(score.item(), 4)

            ElementDrawer.drawRectangule(annotated_image, boxLimits, predictedClass.color)
            text = predictedClass.label.upper()+ " " + "{:.0%}".format(score)
            ElementDrawer.drawTextBox(annotated_image, text, "calibri.ttf", boxLimits, predictedClass.color)

        Event.processAndPersistEvent(self.detectedClassesPrevious, currentDetectedClasses, datetime.timestamp(datetime.now()), app)

        soundAlarmOn = app.config['soundAlarm']

        if self.shouldThrowAlarm(currentDetectedClasses):
            for client in app.config["clients"]:
                app.config["socketIo"].emit('alarm', {'isAudioEnable': soundAlarmOn}, room=client)

        self.detectedClassesPrevious = currentDetectedClasses

        return annotated_image

    def shouldThrowAlarm(self, currentDetectedClasses):
        if (len(self.detectedClassesPrevious) >= len(currentDetectedClasses)):
            return False
        else:
            # INFRACTION_ID represent the 'clean' class
            previousInfractions = list(filter(lambda detectedClass: detectedClass.id == INFRACTION_ID, self.detectedClassesPrevious))
            currentInfractions = list(filter(lambda detectedClass: detectedClass.id == INFRACTION_ID, currentDetectedClasses))

            if(len(currentInfractions) > len(previousInfractions)):
                return True

        return False
    
    def evaluateElementsConfiguration(self, prediction, elementsDict):
        maskEnable = elementsDict[MASK]["isChecked"]
        glassesEnable = elementsDict[GLASSES]["isChecked"]
        faceShieldEnable = elementsDict[FACE_SHIELD]["isChecked"]

        if (not maskEnable and not glassesEnable):
            if(prediction.id == 1 or prediction.id == 2 or prediction.id == 3):
                return self.classes.getClassByPredictedId(INFRACTION_ID)
        elif (not maskEnable):
            if(prediction.id == 1 or prediction.id == 4):
                return self.classes.getClassByPredictedId(INFRACTION_ID)
            if(prediction.id == 3):
                return self.classes.getClassByPredictedId(2)
        elif (not glassesEnable):
            if(prediction.id == 2 or prediction.id == 4):
                return self.classes.getClassByPredictedId(INFRACTION_ID)
            if(prediction.id == 3):
                return self.classes.getClassByPredictedId(1)
        elif (not faceShieldEnable):
            if(prediction.id == 4):
                return self.classes.getClassByPredictedId(INFRACTION_ID)
        
        return prediction
