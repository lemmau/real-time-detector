import cv2
import os
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import model_from_json
from sklearn.metrics import confusion_matrix
from mlxtend.plotting import plot_confusion_matrix

# GET MODEL


# path de imagenes
path_with_mask = './test_models/02_IA_Keras_CNN_Image_Clasification/data/test/with_mask'
path_without_mask = './test_models/02_IA_Keras_CNN_Image_Clasification/data/test/without_mask'

# Parametros para compilacion
length, height = 100, 100

# se obtiene el modelo generado
json_file = open('./test_models/04_IA_Keras_CNN_Image_Clasification/model/model.json', 'r')
loaded_model = json_file.read()
json_file.close()
model = model_from_json(loaded_model)

# se obtienen los pesos
model.load_weights("./test_models/04_IA_Keras_CNN_Image_Clasification/model/weights.h5")
print("Modelo cargado")

# se compila nuevamente el modelo
model.compile(loss='categorical_crossentropy',optimizer='adam',metrics=['accuracy'])


# SHOW CONFUSION MATRIX

list_file_with = os.listdir(path_with_mask)
list_file_without = os.listdir(path_without_mask)

test_labels = []
test_preds = []

# se obtienen cinco imagenes de caras con barbijos
for index, filename in enumerate(list_file_with[:100]):
    path_img = os.path.join(path_with_mask, filename)

    test_labels.append('with_mask')
    
    # se obtiene la imagen
    img_color = cv2.imread(path_img) #Gray Level
    img_gray = cv2.cvtColor(img_color,cv2.COLOR_BGR2GRAY)
    img_pixel = cv2.resize(img_gray, (height, length)) #100 x 100 pixel
    
    # se convierte la imagen a matriz y se realiza la evaluacion
    resized = img_pixel/255.0
    data = np.reshape(resized, (1, height, length, 1))
    model_out = model.predict(data)

    # se establece la leyenda de salida
    if np.argmax(model_out) == 0:
        test_preds.append('without_mask')
    else:
        test_preds.append('with_mask') 

# se obtienen cinco imagenes de caras sin barbijos
for index, filename in enumerate(list_file_without[:100]):
    path_img = os.path.join(path_without_mask, filename)

    test_labels.append('without_mask')

    # se obtiene la imagen
    img_color = cv2.imread(path_img) #Grey Level
    img_gray = cv2.cvtColor(img_color,cv2.COLOR_BGR2GRAY)
    img_pixel = cv2.resize(img_gray, (height, length)) #100 x 100 pixel
    
    # se convierte la imagen a matriz y se realiza la evaluacion
    resized = img_pixel/255.0
    data = np.reshape(resized, (1, height, length, 1))
    model_out = model.predict(data)
    
    # se establece la leyenda de salida
    if np.argmax(model_out) == 0:
        test_preds.append('without_mask')
    else:
        test_preds.append('with_mask')

# se genera la matriz de confusion del modelo
cm = confusion_matrix(test_labels, test_preds)


fig, ax = plot_confusion_matrix(conf_mat=cm, figsize=(14,14), class_names=('with_mask', 'without_mask'))
plt.show()
# se guarda el grafico de la matriz generada
fig.savefig('./test_models/04_IA_Keras_CNN_Image_Clasification/model/conf_matrix.png')