import cv2
import os
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras import optimizers
from tensorflow.keras.models import model_from_json

# Parametros del modelo

length, height = 150, 150
lr = 0.0005
model_path = './test_models/02_IA_Keras_CNN_Image_Clasification/model/model.json'
weights_model_path = './test_models/02_IA_Keras_CNN_Image_Clasification/model/weights.h5'

# Path de imagenes de prueba
path_with_mask = './test_models/02_IA_Keras_CNN_Image_Clasification/data/train/with_mask'
path_without_mask = './test_models/02_IA_Keras_CNN_Image_Clasification/data/train/without_mask'

print("Carga del modelo de prediccion")

# se obtiene el modelos en formato json
json_file = open(model_path, 'r')
loaded_model = json_file.read()
json_file.close()
cnn = model_from_json(loaded_model)

# se obtienen los pesos
cnn.load_weights(weights_model_path)

# compilacion del modelo con:
#  funcion de perdida categorical_crossentropy
#  funcion Adam con learning rate = 0.0005
#  metricas accuracy
cnn.compile(loss='categorical_crossentropy',
            optimizer=optimizers.Adam(lr=lr),
            metrics=['accuracy'])


# SHOW RESULT
list_file_with = os.listdir(path_with_mask)
list_file_without = os.listdir(path_without_mask)

fig = plt.figure(figsize=(14, 14))

# se obtienen cinco imagenes de caras con barbijos
for index, filename in enumerate(list_file_with[:5]):
    path_img = os.path.join(path_with_mask, filename)
    y = fig.add_subplot(6, 5, index+1)

    # se obtiene la imagen
    img_color = cv2.imread(path_img, cv2.IMREAD_COLOR) #RBG Level
    img_pixel = cv2.resize(img_color, (height, length)) #64 x 64 pixel
    
    # se convierte la imagen a matriz y se realiza la evaluacion
    data = img_pixel.reshape(1, height, length, 3)
    model_out = cnn.predict([data])
    
    # se establece la leyenda de salida
    if np.argmax(model_out) == 0:
        str_label = 'pred: With Mask'
    else:
        str_label = 'pred: Without Mask'

    # se muestra la imagen junto con su leyenda
    y.imshow(img_color)
    plt.title(str_label)
    y.axes.get_xaxis().set_visible(False)
    y.axes.get_yaxis().set_visible(False)

# se obtienen cinco imagenes de caras sin barbijos
for index, filename in enumerate(list_file_without[:5]):
    path_img = os.path.join(path_without_mask, filename)
    y = fig.add_subplot(6, 5, index+6)

    # se obtiene la imagen
    img_color = cv2.imread(path_img, cv2.IMREAD_COLOR) #RBG Level
    img_pixel = cv2.resize(img_color, (height, length)) #64 x 64 pixel
    
    # se convierte la imagen a matriz y se realiza la evaluacion
    data = img_pixel.reshape(1, height, length, 3)
    model_out = cnn.predict([data])
    
    # se establece la leyenda de salida
    if np.argmax(model_out) == 0:
        str_label = 'pred: With Mask'
    else:
        str_label = 'pred: Without Mask'

    y.imshow(img_color)
    plt.title(str_label)
    y.axes.get_xaxis().set_visible(False)
    y.axes.get_yaxis().set_visible(False)

plt.show()
