from keras.layers import BatchNormalization
from datetime import datetime
import pickle
from keras.utils import to_categorical
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
import matplotlib.pyplot as plt
from keras.callbacks import EarlyStopping

from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense

import os, glob
import numpy as np

from keras.wrappers.scikit_learn import KerasClassifier
from keras.utils import np_utils
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from keras.utils.vis_utils import plot_model
import sklearn


def baseline_model():
    model = Sequential()
    #model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(32, (5, 5), input_shape=(480, 640, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(BatchNormalization())
    model.add(Dropout(0.1))

    model.add(Conv2D(64, (5, 5)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(BatchNormalization())
    model.add(Dropout(0.1))

    model.add(Conv2D(128, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(BatchNormalization())
    model.add(Dropout(0.1))

    #model.add(Conv2D(128, (3, 3)))
    #model.add(Activation('relu'))
    #model.add(MaxPooling2D(pool_size=(2, 2)))
    #model.add(BatchNormalization())

    model.add(Conv2D(256, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(BatchNormalization())
    model.add(Dropout(0.1))
    
    
    model.add(Flatten())  # this converts our 3D feature maps to 1D feature vectors
    model.add(Dense(128))
    model.add(Activation('relu'))
    model.add(BatchNormalization())
    #model.add(Dropout(0.3))

    model.add(Dense(64))
    model.add(Activation('relu'))
    #model.add(Dropout(0.3))
    model.add(BatchNormalization())

    model.add(Dense(16))
    model.add(Activation('relu'))
    #model.add(Dropout(0.3))
    model.add(BatchNormalization())

    #model.add(Dense(64))
    #model.add(Activation('relu'))
    #model.add(BatchNormalization())


    model.add(Dense(NUM_RAGAS))
    model.add(Activation('softmax'))

    model.compile(loss='categorical_crossentropy',
                  optimizer='Nadam',
                  metrics=['accuracy'])

    # print(model.summary())
    # plot_model(model, to_file='model_plot.png', show_shapes=True, show_layer_names=True)
    return model


#logdir = "logs/scalars/" + str(datetime.now())
#tensorboard_callback = keras.callbacks.Tensorboard(logdir=logdir)
model = baseline_model()
es = EarlyStopping(monitor='val_loss', patience=15)

RAGAS = ["kalyani", "pantuvarali", "kedaragaula", "thodi", "begada", "bhairavi", "mohana", "sankarabharana"]
NUM_RAGAS = len(RAGAS)

data = []
labels = []
ctr=0

for raga in RAGAS:
    inp_files = glob.glob(os.path.join(raga, "*.png"))
    temp = [ctr] * len(inp_files)
    ctr += 1
    print("Raga: {} \t Number of Input files: {}".format(raga, len(inp_files)))
    labels += temp

    for f in inp_files:
        img = load_img(f)  
        x = img_to_array(img)  
        data.append(x)
        # np.append(data, x, axis=-1)

print(len(labels))
print(len(data))
data, labels = sklearn.utils.shuffle(data, labels, random_state=42)

X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.01, shuffle=True, random_state=42)

y_train = to_categorical(y_train)
y_test = to_categorical(y_test)




#history=model.fit(np.array(X_train), np.array(y_train), validation_split=0.0, epochs=2, verbose=2, callbacks=[tensorboard_callback])
history=model.fit(np.array(X_train), np.array(y_train), shuffle=True, validation_data=(np.array(X_test), np.array(y_test)), epochs=150, verbose=2, callbacks=[es], batch_size=32)
print(model.summary())

from sklearn.metrics import plot_confusion_matrix
y_pred = model.predict_classes(X_test)

score = model.evaluate(np.array(X_test), np.array(y_test))
print(score)

print(confusion_matrix(y_true=y_test, y_pred=y_pred, labels=RAGAS, normalize=True))

model.save('fully_convolutional_model_3_layers_with_batchnorm.h5')
#estimator = KerasClassifier(build_fn=baseline_model, epochs=1, batch_size=5, verbose=2)
#kfold = KFold(n_splits=10, shuffle=True)
#results = cross_val_score(estimator, np.array(data), np.array(labels), cv=kfold)
#print("Baseline: %.2f%% (%.2f%%)" % (results.mean()*100, results.std()*100))


# save history to a file
with open('./trainHistoryDict_maxpool_dropout_cnn3_batchnorm', 'wb') as file_pi:
    pickle.dump(history, file_pi)


#print(history.history.keys())
# summarize history for accuracy
#plt.plot(history.history['accuracy'])
#plt.plot(history.history['val_accuracy'])
#plt.title('model accuracy')
#plt.ylabel('accuracy')
#plt.xlabel('epoch')
#plt.legend(['train', 'test'], loc='upper left')
#plt.savefig('trainvstest.png')
# summarize history for loss
#plt.plot(history.history['loss'])
#plt.plot(history.history['val_loss'])
#plt.title('model loss')
#plt.ylabel('loss')
#plt.xlabel('epoch')
#plt.legend(['train', 'test'], loc='upper left')
#plt.savefig('traintestloss.png')
