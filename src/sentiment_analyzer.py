import tensorflow as tf
import numpy as np
# from tensorflow import keras
# from tensorflow.keras.preprocessing.sequence import pad_sequences
from keras.utils import pad_sequences
from preprocess import tokenizer
# from keras.models import Model
# from keras.models import load_model

new_model = tf.keras.models.load_model(
    "./saved_model/sentiment_model.h5")


def sentiment_analyzer(text):
    tokenizer.fit_on_texts([text])
    text_input = tokenizer.texts_to_sequences([text])
    tweets = pad_sequences(text_input)

    prediction = new_model.predict(tweets)

    a = ['negative', 'neutral', 'positive']
    return a[np.argmax(prediction)], prediction.max()

# result = sentiment_analyzer('''
# Swapping batteries is stupid
# ''')
# result
