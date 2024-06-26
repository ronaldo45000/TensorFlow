import tensorflow as tf
from tensorflow.keras import layers, models, callbacks
from tensorflow.keras.datasets import mnist
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Load and preprocess the MNIST dataset
(train_images, train_labels), (test_images, test_labels) = mnist.load_data()
#default inputs: (60000, 28, 28), 28 by 28 MNIST images
#we know that The MNIST database contains 60,000 training images and 10,000 testing images to test models
train_images = train_images.reshape((60000, 28, 28, 1)).astype('float32') / 255
test_images = test_images.reshape((10000, 28, 28, 1)).astype('float32') / 255

# Use Data augmentation technique increase the diversity of training set by applying random transformations, such as image rotation for enhancing the performance.
datagen = ImageDataGenerator(
    rotation_range=10,  # Rotate images by up to 10 degrees
    width_shift_range=0.1,  # Shift images horizontally by up to 10% of the width
    height_shift_range=0.1,  # Shift images vertically by up to 10% of the height
    shear_range=0.1,  # Apply shear transformations with a maximum shear intensity of 0.1
    zoom_range=0.1  # Apply zoom transformations with a maximum zoom intensity of 0.1
)
datagen.fit(train_images)  # Calculate stats required for data augmentation

# This is to reconstruct the LeNet-5 architecture ( base on structure from wiki Lenet)
model = models.Sequential([
    layers.Conv2D(6, kernel_size=(5, 5), activation='relu', input_shape=(28, 28, 1)),  # Convolutional layer with 6 filters and ReLU activation
    layers.MaxPooling2D(pool_size=(2, 2)),  # Max pooling layer with 2x2 pool size
    layers.Conv2D(16, kernel_size=(5, 5), activation='relu'),  # Convolutional layer with 16 filters and ReLU activation
    layers.MaxPooling2D(pool_size=(2, 2)),  # Max pooling layer with 2x2 pool size
    layers.Flatten(),  # Flatten the output for input to fully connected layers
    layers.Dense(120, activation='sigmoid'),  # Fully connected layer with 120 neurons and sigmoid activation
    layers.Dense(84, activation='sigmoid'),  # Fully connected layer with 84 neurons and sigmoid activation
    layers.Dense(10, activation='sigmoid')  # Output layer with 10 neurons for classification and sigmoid activation
])

#  To compile the model
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])



#  Train the model with data augmentation
history = model.fit(datagen.flow(train_images, train_labels, batch_size=64),  # Use data generator to feed augmented images in batches
                    steps_per_epoch=len(train_images) / 64,  # Number of steps per epoch
                    epochs=5,  # Number of epochs for training
                    validation_data=(test_images, test_labels)  # Validation data
                )

# Display training history
#we can use Matplotlib to visualize the results
import matplotlib.pyplot as plt

plt.plot(history.history['loss'], label='train_loss')  # Plot training loss
plt.plot(history.history['val_loss'], label='val_loss')  # Plot validation loss
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.show()

plt.plot(history.history['accuracy'], label='train_accuracy')  # Plot training accuracy
plt.plot(history.history['val_accuracy'], label='val_accuracy')  # Plot validation accuracy
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.show()

#  This is to evaluate the model on test data
test_loss, test_accuracy = model.evaluate(test_images, test_labels)  # Evaluate model performance on test data
print('Final Lost:', test_loss)  # Print test loss
print('Final Accuracy:', test_accuracy)  # Print test accuracy
