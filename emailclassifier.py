"""
     Importing Required Modules

"""

import tensorflow as tf
gpus = tf.config.experimental.list_physical_devices('GPU')


if gpus:
    tf.config.experimental.set_memory_growth(gpus[0], enable=True)


__author__ = "Siddharth Achari Sharabu"



from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
#from keras import utils as np_utils
from keras.utils.np_utils import to_categorical
from keras.callbacks import ModelCheckpoint, TensorBoard
from sklearn.model_selection import train_test_split
import time
import numpy as np
import pickle

from utilities import get_model, SEQUENCE_LENGTH, TEST_SIZE
from utilities import BATCH_SIZE, EPOCHS, label2int


"""
    Loading The Spam_Data

"""


def load_data():
    texts, labels = [], []
    with open("data/spam.txt") as f:
        for line in f:
            split = line.split()
            labels.append(split[0].strip())
            texts.append(' '.join(split[1:]).strip())
    return texts, labels

    
X, y = load_data()


"""
      Text tokenization
      vectorizing text, turning each text into sequence of integers

"""


tokenizer = Tokenizer()
tokenizer.fit_on_texts(X)
pickle.dump(tokenizer, open("results/tokenizer.pickle", "wb"))
X = tokenizer.texts_to_sequences(X)
print(X[0])
X = np.array(X)
y = np.array(y)
X = pad_sequences(X, maxlen=SEQUENCE_LENGTH)
print(X[0])


y = [ label2int[label] for label in y ]
y = to_categorical(y)
print(y[0])


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=TEST_SIZE, random_state=7)

print("X_train.shape:", X_train.shape)
print("X_test.shape:", X_test.shape)
print("y_train.shape:", y_train.shape)
print("y_test.shape:", y_test.shape)

model = get_model(tokenizer=tokenizer, lstm_units=128)


model_checkpoint = ModelCheckpoint("results/spam_classifier_{val_loss:.2f}.h5", save_best_only=True,verbose=1)

tensorboard = TensorBoard(f"logs/spam_classifier_{time.time()}")


model.fit(X_train, y_train, validation_data=(X_test, y_test),
          batch_size=BATCH_SIZE, epochs=EPOCHS,
          callbacks=[tensorboard, model_checkpoint],
          verbose=1)


result = model.evaluate(X_test, y_test)

loss = result[0]
accuracy = result[1]
precision = result[2]
recall = result[3]

print(f"[+] Accuracy: {accuracy*100:.2f}%")
print(f"[+] Precision:   {precision*100:.2f}%")
print(f"[+] Recall:   {recall*100:.2f}%")



