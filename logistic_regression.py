from keras.utils import to_categorical
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
import matplotlib.pyplot as plt

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

from keras.utils.vis_utils import plot_model


RAGAS = ["thodi", "begada", "bhairavi", "mohana", "sankarabharana"]
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

# print(labels)
print(len(labels))
print(len(data))

# encode class values as integers
#encoder = LabelEncoder()
#encoder.fit(labels)
#encoded_Y = encoder.transform(labels)
# convert integers to dummy variables (i.e. one hot encoded)
#dummy_y = np_utils.to_categorical(encoded_Y)
labels = to_categorical(labels)


def baseline_model():
    model = Sequential()
    model.add(Flatten())
    model.add(Dense(NUM_RAGAS) )
    model.add(Activation('softmax'))
    model.compile(loss='categorical_crossentropy',
                  optimizer='rmsprop',
                  metrics=['accuracy'])

    # print(model.summary())
    # plot_model(model, to_file='model_plot.png', show_shapes=True, show_layer_names=True)
    return model

model = baseline_model()
#print(model.summary())
history=model.fit(np.array(data), np.array(labels), validation_split=0.20, epochs=200, verbose=2)


#estimator = KerasClassifier(build_fn=baseline_model, epochs=1, batch_size=5, verbose=2)
#kfold = KFold(n_splits=10, shuffle=True)
#results = cross_val_score(estimator, np.array(data), np.array(labels), cv=kfold)
#print("Baseline: %.2f%% (%.2f%%)" % (results.mean()*100, results.std()*100))


# save history to a file
f = open("history", "w")
f.write(history)
f.close()

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
