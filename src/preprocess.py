from keras.preprocessing.text import Tokenizer
from keras.utils import pad_sequences
# import numpy as np
import pandas as pd
# import tensorflow as tf
# from tensorflow import keras

df = pd.read_csv("./Twitter_Data.csv")
# download data from kaggle
df = df.dropna()
df_cleaned = df

label = pd.get_dummies(df_cleaned.category)
label.columns = ["negative", "neutral", "positive"]
text_only = df_cleaned.drop(columns="category")

# Tokenization

tokenizer = Tokenizer(num_words=8150, lower=True, split=" ", oov_token="~")
tokenizer.fit_on_texts(text_only["clean_text"])
word_ind = tokenizer.word_index

text_only["clean_text"] = tokenizer.texts_to_sequences(text_only["clean_text"])
tweets = pad_sequences(text_only["clean_text"])
