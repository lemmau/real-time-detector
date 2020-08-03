import sys
import torch
from torchvision import transforms
from PIL import Image
sys.path.insert(0, 'commons')
from ElementDrawer import ElementDrawer

class IAModel():

    def __init__(self, modelPath: str, classes:list):
  
        self.modelPath = modelPath
        self.model = torch.load("core/checkpoint_ssd300_kaggle.pth.tar", map_location='cpu')
        print('\nLoaded checkpoint from epoch %d.\n' % (self.model['epoch'] + 1))
        self.model = self.model['model'].to(torch.device('cpu')).eval()
        self.classes = classes
        self.device = torch.device('cpu')

    def detect(self, original_image, min_score:float ,max_overlap:float, max_objects:int) -> Image:

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

        # Transform back to original image dimensions
        original_dims = torch.FloatTensor(
            [original_image.width, original_image.height, original_image.width, original_image.height]).unsqueeze(0)
        det_boxes = det_boxes * original_dims

        annotated_image = original_image

        if det_labels == ['background']:
            return original_image

        for labelId, box, score in zip(det_labels, det_boxes, det_scores):
            c = self.classes.getClassByPredictedId(labelId)
            boxLimits = box.tolist()
            score = round(score.tolist()[0], 4)
            
            ElementDrawer.drawRectangule(annotated_image, boxLimits, c.color)
            text = c.label.upper()+ " " + "{:.2%}".format(score)
            ElementDrawer.drawTextBox(annotated_image, text, "calibri.ttf", boxLimits, c.color)

        return annotated_image
