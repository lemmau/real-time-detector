import sys
import cv2
sys.path.insert(0, 'commons')
from PIL import Image
from imutils.video import VideoStream
from PredictedClass import ClassList
from IAModel import IAModel

classes = ClassList()
classes.addClass(0, 'background', '#ffffff')
classes.addClass(1, 'with_mask', '#3cb44b')
classes.addClass(2, 'without_mask', '#e6194B')

# Load model checkpoint
checkpoint = "core/checkpoint_ssd300_kaggle.pth.tar"
model = IAModel(checkpoint, classes)


# Use to run SSD300 on image
if __name__ == '__main__':
    img_path = '/home/depi/Desktop/depi.png'
    original_image = Image.open(img_path, mode='r')
    result = model.detect(original_image, min_score=0.2, max_overlap=0.5, max_objects=200)
    result.show()

# Use to run SSD300 on webcam
# if __name__ == '__main__':
#     video_capture = cv2.VideoCapture(0)

#     while True:
#         ret, frame = video_capture.read()
#         original_image = Image.fromarray(frame)
#         prediction = detect(original_image, min_score=0.7,
#                             max_overlap=0.1, max_objects=100)

#         cv2.imshow('Video', np.array(prediction))

#         # Se espera la tecla 'q' para salir
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     # se liberan los recursos de la camara
#     video_capture.release()
#     cv2.destroyAllWindows()
