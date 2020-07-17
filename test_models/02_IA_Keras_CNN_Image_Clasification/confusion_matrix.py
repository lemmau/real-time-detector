import cv2
import os
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import model_from_json
from sklearn.metrics import confusion_matrix
from mlxtend.plotting import plot_confusion_matrix

# Parametros del modelo
length, height = 150, 150
lr = 0.0005
model_path = './test_models/02_IA_Keras_CNN_Image_Clasification/model/model.json'
weights_model_path = './test_models/02_IA_Keras_CNN_Image_Clasification/model/weights.h5'

# Path de imagenes de prueba
test_path = './test_models/02_IA_Keras_CNN_Image_Clasification/data/test'
test_batches = ImageDataGenerator().flow_from_directory(test_path, target_size=(height, length), classes=['with_mask', 'without_mask'], batch_size=200)

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
            optimizer=Adam(lr=lr),
            metrics=['accuracy'])

# informacion para la generacion de la matriz
test_imgs, test_labels = next(test_batches)
test_labels = test_labels[:,0]
predictions = cnn.predict_generator(test_batches, steps=1, verbose=0)

# se genera la matriz de confusion del modelo
cm = confusion_matrix(test_labels, predictions[:,0])

fig, ax = plot_confusion_matrix(conf_mat=cm, figsize=(14,14), class_names=('with_mask', 'without_mask'))
plt.show()
# se guarda el grafico de la matriz generada
fig.savefig('./test_models/02_IA_Keras_CNN_Image_Clasification/model/conf_matrix.png')