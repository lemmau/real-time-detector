from tensorflow.keras.models import model_from_json
from tensorflow.keras.optimizers import Adam
from imutils.video import VideoStream
import face_recognition
import cv2
import numpy as np
import time
import imutils

# Antes de ejecutar este programa se deben crear y entrenar los modelos existentes
#  en este proyeco. Para hacerlo se ejecutan los programas generate_model.py lo cual
#  crea dos archivos en la carpeta ./model: model.json y weights.h5
# Una vez realizado esto, se modifican las variables model_path y weights_path con
#  sus respectivas direcciones y se ejecuta este programa.


# model paths
model_path = './test_models/03_IA_Keras_SSD_Object_Detection/model/model.json'
weights_path = './test_models/03_IA_Keras_SSD_Object_Detection/model/weights.h5'


# GET MODEL

# se obtiene el modelo generado
json_file = open(model_path, 'r')
loaded_model = json_file.read()
json_file.close()
model = model_from_json(loaded_model)

# se obtienen los pesos
model.load_weights(weights_path)
print("Modelo cargado") 

# se compila nuevamente el modelo
# optimizer = Adam(learning_rate=1e-4)
# model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])
epocas = 10
lr = 1e-4

opt = Adam(lr=lr, decay=lr / epocas)
model.compile(loss="binary_crossentropy", optimizer=opt, metrics=["accuracy"])


# se obtiene la referencia de la camara web
# 0 => default
# 2 => usb
vs = VideoStream(src=0).start()
time.sleep(2.0)


while True:
    
    # se obtiene la imagen de la webcam
    frame = vs.read()
    frame = imutils.resize(frame, width=400)

    # se convierte el color de imagen de BGR a RGB para la utilizacion del modelo 
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # se obtienen todos los rostros del framde video
    face_locations = face_recognition.face_locations(rgb_frame)

    # se recorre cada una de las imagenes de rostros
    for (top, right, bottom, left) in face_locations:
        # color = (0, 0, 255) #color rojo por default

        # se toman las coordenadas 
        #top, right, bottom, left = face_location

        # se prepara la imagen para enviar al modelo
        img_pixel = rgb_frame[top:bottom, left:right]
        img_pixel = cv2.resize(img_pixel, (224, 224)) #224 x 224 pixel

        # se converte la imagen a informacion y se predice el uso de barbijo
        data = img_pixel.reshape(1, 224, 224, 3)
        model_out = model.predict([data])

        # se verifica si se tiene puesto barbijo
        color = (0, 255, 0) if np.argmax(model_out) == 0 else (0, 0, 255)
        # if np.argmax(model_out) == 0:
            # color = (0, 255, 0) #color verde

        # se realiza el dibujo del rectangulo sobre el rostro
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)

    # show the output frame
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    # se espera la tecla 'q' para salir
    if key == ord("q"):
        break

# se liberan los recursos de la camara
cv2.destroyAllWindows()
vs.stop()