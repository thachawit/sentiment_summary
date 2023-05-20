import tensorflow as tf


model = tf.saved_model.load('model.pb')


print('line7')


def load_sentiment_model():
    result = model.sentiment_analyzer('''Swapping batteries is stupid''')
    print(result)
    return result


print(load_sentiment_model())
