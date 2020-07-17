
import cv2
import os
import numpy as np
from tensorflow.keras import backend as K
from tensorflow.keras import utils
from tensorflow.keras.models import Sequential
from tensorflow.keras.models import model_from_json
from tensorflow.keras.layers import Dense, Activation, Flatten, Dropout
from tensorflow.keras.layers import Conv2D, MaxPooling2D
from tensorflow.keras.callbacks import ModelCheckpoint
from sklearn.model_selection import train_test_split
from matplotlib import pyplot as plt

# se cancela cuaquier otro proceso de entrenamiento
K.clear_session()

# carpetas de archivos de entrenamiento, validacion y almacenamiento del modelo
train_data_path = './test_models/02_IA_Keras_CNN_Image_Clasification/data/train'
target_dir = './test_models/04_IA_Keras_CNN_Image_Clasification/model/'

categories = os.listdir(train_data_path)
labels = [i for i in range(len(categories))]

labels_dict = dict(zip(categories, labels))

# Parametros de Entrenamiento

epocas = 10
length, height = 100, 100
# batch_size = 32
# steps = 100
# validation_steps = 30
# Conv1_filters = 32
# Conv2_filters = 64
# filter1_size = (3, 3)
# filter2_size = (2, 2)
# pool_size = (2, 2)
# classes = 2
# lr = 0.0005
errors = 0

data = []
target = []

# por cada categoria (en este caso dos: with_mask - without_mask), se
#  se obtiene cada una de las imagenes, se da formato de tamanio 100x100
#  y color gris para luego agregarse a los arrays de data y target
for category in categories:
    folder_path = os.path.join(train_data_path, category)
    img_names = os.listdir(folder_path)

    for img_name in img_names:
        img_path = os.path.join(folder_path, img_name)
        img = cv2.imread(img_path)

        try:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            resized = cv2.resize(gray, (height, length))
            data.append(resized)
            target.append(labels_dict[category])
        except Exception as e:
            print('Error: ', img_path)

# formato final de datos en forma de matriz para el entrenamiento del modelo
data = np.array(data)/255.0
data = np.reshape(data, (data.shape[0], height, length, 1))
target = np.array(target)

new_target = utils.to_categorical(target)


# MODEL CREATION

model = Sequential()

# primera capa Imput conv-relu-pooling
model.add(Conv2D(200,(3,3),input_shape=data.shape[1:]))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2,2)))

# segunda capa conv-relu-pooling
model.add(Conv2D(100,(3,3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2,2)))

# tercera capa plana y dropout
model.add(Flatten())
model.add(Dropout(0.5))

# cuarta capa de activacion relu y de salida softmax
model.add(Dense(50,activation='relu'))
model.add(Dense(2,activation='softmax'))

# compilacion del modelo con:
#  funcion de perdida categorical_crossentropy
#  funcion Adam
#  metricas accuracy
model.compile(loss='categorical_crossentropy',optimizer='adam',metrics=['accuracy'])

print("Modelo compilado")

# se muestra la arquitectura del modelo generado
model.summary()

# se prepara la info para el entrenamiento
train_data, test_data, train_target, test_target = train_test_split(data, new_target, test_size=0.1)

# se crean los puntos de comprobacion
checkpoint = ModelCheckpoint('model-{epoch:03d}.model', monitor='val_loss', verbose=0, save_best_only=True, mode='auto')

# entrenamiento del modelo con:
#  imagenes de entrenamiento
#  cantidad de epocas 20
history = model.fit(
    train_data,
    train_target,
    epochs=epocas,
    callbacks=[checkpoint],
    validation_split=0.2)

print("Fin de entrenamiento del modelo")

# se crea la carpeta el almacenamiento del modelo
if not os.path.exists(target_dir):
  os.mkdir(target_dir)

# se crea el modelo .json
model_jason = model.to_json()

# se almacena el modelo generado en formato json y los pesos en h5
with open("./test_models/04_IA_Keras_CNN_Image_Clasification/model/model.json", "w") as json_file:
    json_file.write(model_jason)

# se almacenan los pesos en formato h5
model.save_weights('./test_models/04_IA_Keras_CNN_Image_Clasification/model/weights.h5')

print("Se ha guardado el modelo generado")

# SHOW MODEL TRAIN SEQUENCE

# se muestra el avance del entrenamiendo en cuanto a la presicion
plt.figure()
plt.plot(history.history['accuracy'],'r',label='training accuracy')
plt.plot(history.history['val_accuracy'],label='validation accuracy')
plt.xlabel('# epochs')
plt.ylabel('accurancy')
plt.legend()
plt.savefig('./test_models/04_IA_Keras_CNN_Image_Clasification/model/accur.png')
plt.close()

# se muestra el avance del entrenamiento en cuanto a la perdida
plt.figure()
plt.plot(history.history['loss'],'r',label='training loss')
plt.plot(history.history['val_loss'],label='validation loss')
plt.xlabel('# epochs')
plt.ylabel('loss')
plt.legend()
plt.savefig('./test_models/04_IA_Keras_CNN_Image_Clasification/model/loss.png')
plt.close()