import numpy as np
import keras
import csv
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Conv2D, MaxPooling2D, Flatten, BatchNormalization
from keras.optimizers import Adam
from keras.callbacks import CSVLogger
from keras.preprocessing.image import ImageDataGenerator

img_size = 64
n_epochs = 100
batch_sizes = 4
n_steps_per_epoch = 500
n_validation_steps = 100
csv_logger = CSVLogger('cnn_aug_1.csv')

try:
    train_data = np.load('CNN_train_feature.npy') 
    train_target = np.load('CNN_train_target.npy') 
    test_data = np.load('CNN_test_feature.npy') 
    test_target = np.load('CNN_test_target.npy') 
    
    #print(train_target.shape)
    train_target = keras.utils.to_categorical(train_target,10)
    test_target = keras.utils.to_categorical(test_target,10)
    #print(train_target[0:10])

    '''
    print('train_data:')
    print(train_data)
    print('test_data:')
    print(test_data)
    print('train_target:')
    print(train_target)
    print('test_target:')
    print(test_target)
    '''

except ValueError:
    print('Dataset files not founded ')


train_datagen = ImageDataGenerator()
train_generator = train_datagen.flow(train_data, train_target, batch_size = batch_sizes)
test_datagen = ImageDataGenerator()
test_generator = test_datagen.flow(test_data, test_target, batch_size = batch_sizes)

#Build AlexNet model
model = Sequential()
 
model.add(Conv2D(64, kernel_size=5, input_shape=(img_size, img_size, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(3,3)))
model.add(Conv2D(32, kernel_size=3, activation='relu'))
model.add(Dense(512, activation='relu'))
model.add(Flatten())
model.add(Dense(10, activation='softmax'))

model.summary()

model.compile(loss="categorical_crossentropy", optimizer = Adam(lr=0.0001) ,
              metrics=["accuracy"])

model.fit_generator(train_generator,
                    epochs=n_epochs,
                    validation_data=test_generator,
                    steps_per_epoch = n_steps_per_epoch,
                    validation_steps = n_validation_steps,
                    callbacks=[csv_logger])

model.save('CNN_model_cnn.h5')

x = model.evaluate_generator(test_generator, steps=n_validation_steps)
print(x)

input('')
