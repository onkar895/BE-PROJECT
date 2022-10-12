import os
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
from tensorflow.keras.layers import Dense, Conv2D, Flatten, Dropout, MaxPooling2D

PATH = 'train_and_validation' #Path to training Data

train_data = os.path.join(PATH,'train')   #Train data extraction
validation_data = os.path.join(PATH,'validation')#validation data extraction

#train data
train_enhanced_dir = os.path.join(train_data,'en')
train_unenhanced_dir = os.path.join(train_data,'un')

#validation data
validation_enhanced_dir = os.path.join(validation_data,'en')
validation_unenhanced_dir = os.path.join(validation_data,'un')

#hyper parameters
batch_size =128
img_height = 150
img_width = 150

train_image_generator = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./255)
validation_image_generator = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./255)

train_data_gen = train_image_generator.flow_from_directory(batch_size=batch_size,directory=train_data,shuffle=True,target_size=(img_width,img_height),class_mode='binary')
val_data_gen = validation_image_generator.flow_from_directory(batch_size=batch_size,directory=validation_data,shuffle=True,target_size=(img_width,img_height),class_mode='binary')

check_point = 'check_point_en_un.cpkt'#check point
checkpoint_dir = os.path.dirname(check_point)
cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=check_point,save_weights_only=True,verbose=1)
num_enhanced_tr = len(os.listdir(train_enhanced_dir))
num_unenhanced_tr = len(os.listdir(train_unenhanced_dir))

num_enhanced_val = len(os.listdir(validation_enhanced_dir))
num_unenhanced_val = len(os.listdir(validation_unenhanced_dir))

total_train = num_enhanced_tr + num_unenhanced_tr
total_val = num_enhanced_val + num_unenhanced_val
#actual model
model = tf.keras.Sequential([

                                    Conv2D(16,3,input_shape=(img_height,img_width,3),activation='relu',padding='same'),
                                    MaxPooling2D(),

                                    Conv2D(32,3,padding='same',activation='relu'),
                                    MaxPooling2D(),
                                    Conv2D(64,3,padding='same',activation='relu'),
                                    MaxPooling2D(),
                                    Flatten(),
                                    Dense(512,activation='relu'),
                                    Dense(1)
                            ])
model.compile(optimizer='adam',loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),metrics=['accuracy'])

history = model.fit(
    train_data_gen,
    steps_per_epoch=total_train // batch_size,
    epochs=5,
    validation_data=val_data_gen,
    validation_steps=total_val // batch_size,
    callbacks=[cp_callback]
)
