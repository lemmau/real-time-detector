import cv2
import torch
import numpy as np
import imutils
from utils import *
from torchvision import transforms
from PIL import Image, ImageDraw, ImageFont
from imutils.video import VideoStream
from imutils.video import FPS

device = torch.device('cpu')

# Load model checkpoint
checkpoint = 'core\models\checkpoint_ssd300_kaggle.pth.tar'
checkpoint = torch.load(checkpoint, map_location='cpu')
print('\nLoaded checkpoint from epoch %d.\n' % (checkpoint['epoch'] + 1))

model = checkpoint['model'].to(device).eval() # eval() turn the model into evaluation mode

# Transforms needed for SSD300 (we are using torchvision to apply image tranformation) -> https://pytorch.org/docs/stable/torchvision/transforms.html
resize = transforms.Resize((300, 300))
to_tensor = transforms.ToTensor()
normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225]) # We use the standard transformation for RGB images - More info can be found here https://discuss.pytorch.org/t/understanding-transform-normalize/21730/22 


def detect(original_image, min_score, max_overlap, max_objects):
    image = normalize(to_tensor(resize(original_image)))
    image = image.to(device)
    predicted_locs, predicted_scores = model(image.unsqueeze(0)) # Unsqueeze -> Returns a new tensor with a dimension of size one inserted at the specified position.

    # Run the detection over locations
    det_boxes, det_labels, det_scores = model.detect_objects(predicted_locs, predicted_scores, min_score=min_score,
                                                             max_overlap=max_overlap, top_k=max_objects)
    det_boxes = det_boxes[0].to('cpu')
    det_labels = det_labels[0].to('cpu').tolist()

    # Transform back to original image dimensions
    original_dims = torch.FloatTensor(
        [original_image.width, original_image.height, original_image.width, original_image.height]).unsqueeze(0)
    det_boxes = det_boxes * original_dims

    # Decode class integer labels
    det_labels = [rev_label_map[l] for l in det_labels]

    if det_labels == ['background']:
        return original_image

    annotated_image = original_image
    draw = ImageDraw.Draw(annotated_image)
    font = ImageFont.truetype("./calibril.ttf", 15) # If fails with calibril, use some available font

    for i in range(det_boxes.size(0)): # det_boxes contains an array of values for each object detected, so we need to loop and take each array of values
        box_location = det_boxes[i].tolist()
        detected_label = det_labels[i]

        draw.rectangle(xy=box_location, outline=label_color_map[detected_label]) # Draw rectangle more info -> https://www.geeksforgeeks.org/python-pil-imagedraw-draw-rectangle/
        
        # Increase thickness on rectangle
        draw.rectangle(xy=[l + 1. for l in box_location], outline=label_color_map[detected_label])
        draw.rectangle(xy=[l + 2. for l in box_location], outline=label_color_map[detected_label])
        draw.rectangle(xy=[l + 3. for l in box_location], outline=label_color_map[detected_label])

        text_size = font.getsize(detected_label.replace('_', ' ', 1).upper())
        text_location = [box_location[0] + 2., box_location[1] - text_size[1]]
        textbox_location = [box_location[0], box_location[1] - text_size[1], box_location[0] + text_size[0] + 4., box_location[1]]
        draw.rectangle(xy=textbox_location, fill=label_color_map[detected_label])
    del draw
    return annotated_image

# Use to run SSD300 on image
if __name__ == '__main__':
    img_path = './core/data/test_data/2.jpg'
    original_image = Image.open(img_path, mode='r')
    detect(original_image, min_score=0.2, max_overlap=0.5, max_objects=200).show()

# Use to run SSD300 on webcam
# if __name__ == '__main__':
#     video_capture = cv2.VideoCapture(0)

#     while True:
#         ret, frame = video_capture.read()
#         original_image = Image.fromarray(frame)
#         prediction = detect(original_image, min_score=0.1,
#                             max_overlap=0.5, max_objects=100)

#         cv2.imshow('Video', np.array(prediction))

#         # Se espera la tecla 'q' para salir
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     # se liberan los recursos de la camara
#     video_capture.release()
#     cv2.destroyAllWindows()
