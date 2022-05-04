
import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt

# load dataset (MNIST Fashion dataset = 70000 clothing images)

fashion_mnist = keras.datasets.fashion_mnist
(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()  # split into testing and training
train_images.shape

class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

#Preprocessing
#Transformer/normaliser... dataset avant de le donner au model
train_images = train_images / 255.0

test_images = test_images / 255.0
#On divise par 255 pour avoir une dataset comprise entre 0 et 1

#Building model
#Sequential = architecture la plus basique (calcul de gauche à droite)
model = keras.Sequential([
    keras.layers.Flatten(input_shape=(28, 28)),  # input layer (1) #on applatti la matrice de pixels pour avoir une input layer de 784 nodes
    keras.layers.Dense(128, activation='relu'),  # hidden layer (2)#Dense = chaques input nodes connectés a chaque hidden nodes
    keras.layers.Dense(10, activation='softmax') # output layer (3)#nb output nodes = nb classes
])
#Compile model
model.compile(optimizer='adam',#on choisi l'optimizer 'adam'
              loss='sparse_categorical_crossentropy',#on choisi la fonction loss 'sparse...'
              metrics=['accuracy'])#on veut accuracy en output

#Training
model.fit(train_images, train_labels, epochs=3)  # we pass the data, labels and epochs and watch the magic!

test_loss, test_acc = model.evaluate(test_images,  test_labels, verbose=1)

print('Test accuracy:', test_acc)

#Predictions
predictions = model.predict(test_images)
print(predictions[0])#prediction de la premiere image : tableau de 10 floats (1 par output nodes),
#correspond a la probabilité que la premiere image appartienne à la nième classe
#max du tableau = classe de l'image
np.argmax(predictions[0])#retourne l'index du max du tableau
plt.figure()
plt.imshow(test_images[0])
plt.colorbar()
plt.grid(False)
plt.show()
print(class_names[np.argmax(predictions[0])])

