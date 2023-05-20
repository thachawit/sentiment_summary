import pandas as pd
from keras.utils import pad_sequences
from sklearn.base import TransformerMixin
from keras.preprocessing.text import Tokenizer
import nltk
import re
import string

class Preprocessor(TransformerMixin):
    def fit_transform(self, X: pd.DataFrame, y=None, **fit_params):
        df = X.dropna()

        label = pd.get_dummies(df.category)
        label.columns = ["negative", "neutral", "positive"]

        text_only = df.drop(columns="category")
        tokenizer = Tokenizer(num_words=8150, lower=True,
                              split=" ", oov_token="~")
        tokenizer.fit_on_texts(text_only["clean_text"])

        text_only["clean_text"] = tokenizer.texts_to_sequences(
            text_only["clean_text"])
    
        

        return pad_sequences(text_only["clean_text"])