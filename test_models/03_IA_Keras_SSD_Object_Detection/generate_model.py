import matplotlib.pyplot as plt
import numpy as np
import argparse
import os
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import AveragePooling2D
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Input
from tensorflow.keras.models import Model
from tensorflow.keras.models import model_from_json
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.utils import to_categorical
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from imutils import paths


# carpetas de archivos de entrenamiento y download de modelo
images_path = './test_models/03_IA_Keras_SSD_Object_Detection/data/train'
target_dir = './test_models/03_IA_Keras_SSD_Object_Detection/model/'

# Parametros de entrenamiento

epocas = 10
lr = 1e-4
batch_size = 32

# se crea la lista de imagenes
image_list = list(paths.list_images(images_path))
data = []
labels = []

# loop over the image paths
for image_path in image_list:
	# se obtiene el nombre de la imagen
	label = image_path.split(os.path.sep)[-2]

	# se convierte la imagen a matrix de 224x224 pixels
	image = load_img(image_path, target_size=(224, 224))
	image = img_to_array(image)
	# preproceso de la imagen para la red mobile
	image = preprocess_input(image)

	# se agrega la imagen y el label
	data.append(image)
	labels.append(label)

# se convierte la informacion al matriz final
data = np.array(data, dtype="float32")
labels = np.array(labels)

# perform one-hot encoding on the labels
lb = LabelBinarizer()
labels = lb.fit_transform(labels)
labels = to_categorical(labels)

# se dividen las imagenes para entrenamiento y validacion usando el 75%
# para el entrenamiento y el 25% para validacion
(trainX, testX, trainY, testY) = train_test_split(data, labels,
	test_size=0.20, stratify=labels, random_state=42)

# generador d eimagenes para el entrenamiento
aug = ImageDataGenerator(
	rotation_range=20,
	zoom_range=0.15,
	width_shift_range=0.2,
	height_shift_range=0.2,
	shear_range=0.15,
	horizontal_flip=True,
	fill_mode="nearest")

print("Comienzo del proceso de armado del modelos")

# se obteien la red mobile a reentrenar y se agrega la capa Input
baseModel = MobileNetV2(weights="imagenet", include_top=False,
	input_tensor=Input(shape=(224, 224, 3)))

# se agregan capas adicionales de pooling, relu, dropout y salida softmax
headModel = baseModel.output
headModel = AveragePooling2D(pool_size=(7, 7))(headModel)
headModel = Flatten(name="flatten")(headModel)
headModel = Dense(128, activation="relu")(headModel)
headModel = Dropout(0.5)(headModel)
headModel = Dense(2, activation="softmax")(headModel)

# modelo final para el entrenamiento
model = Model(inputs=baseModel.input, outputs=headModel)

# loop over all layers in the base model and freeze them so they will
# *not* be updated during the first training process
for layer in baseModel.layers:
	layer.trainable = False

# funcion de optimizacion
opt = Adam(lr=lr, decay=lr / epocas)

# compilacion del modelo con:
#  funcion de perdida binary_crossentropy
#  funcion Adam con learning rate = e-4
#  metricas accuracy
model.compile(loss="binary_crossentropy", optimizer=opt,
	metrics=["accuracy"])

print("Modelo compilado")

model.summary()

# entrenamiento del modelo con:
#  generador de imagenes de entrenamiento y validacion
#  batch_size = 32
#  cantidad de pasos para entrenamiento = cantidad de imagenes
#   de entrenamiento sobre el tamanio del batch
#  generador de imagenes de validacion
#  cantidad de pasos para validacion = cantidad de imagenes
#   de validacion sobre el tamanio del batch
#  cantidad de epocas 10
model.fit(
	aug.flow(trainX, trainY, batch_size=batch_size),
	steps_per_epoch=len(trainX) // batch_size,
	validation_data=(testX, testY),
	validation_steps=len(testX) // batch_size,
	epochs=epocas)

print("Fin de entrenamiento del modelo")

# se crea la carpeta el almacenamiento del modelo
if not os.path.exists(target_dir):
  os.mkdir(target_dir)

# se crea el modelo .json
model_jason = model.to_json()

# se almacena el modelo generado en formato json y los pesos en h5
with open("./test_models/03_IA_Keras_SSD_Object_Detection/model/model.json", "w") as json_file:
    json_file.write(model_jason)

# se almacenan los pesos en formato h5
model.save_weights('./test_models/03_IA_Keras_SSD_Object_Detection/model/weights.h5')

print("Se ha guardado el modelo generado")

# # make predictions on the testing set
# print("[INFO] evaluating network...")
# predIdxs = model.predict(testX, batch_size=BS)

# # for each image in the testing set we need to find the index of the
# # label with corresponding largest predicted probability
# predIdxs = np.argmax(predIdxs, axis=1)

# # show a nicely formatted classification report
# print(classification_report(testY.argmax(axis=1), predIdxs,
# 	target_names=lb.classes_))

# # serialize the model to disk
# print("[INFO] saving mask detector model...")
# model.save(args["model"], save_format="h5")

# # plot the training loss and accuracy
# N = EPOCHS
# plt.style.use("ggplot")
# plt.figure()
# plt.plot(np.arange(0, N), H.history["loss"], label="train_loss")
# plt.plot(np.arange(0, N), H.history["val_loss"], label="val_loss")
# plt.plot(np.arange(0, N), H.history["acc"], label="train_acc")
# plt.plot(np.arange(0, N), H.history["val_accuracy"], label="val_acc")
# plt.title("Training Loss and Accuracy")
# plt.xlabel("Epoch #")
# plt.ylabel("Loss/Accuracy")
# plt.legend(loc="lower left")
# plt.savefig(args["plot"])
