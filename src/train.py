from sklearn.model_selection import train_test_split
# import tensorflow as tf
from tensorflow import keras
from preprocess import tweets, label
# from keras.models import Model
# from keras.models import load_model

X_train, X_test, y_train, y_test = train_test_split(
    tweets, label, test_size=0.15)
X_train, X_valid, y_train, y_valid = train_test_split(
    X_train, y_train, test_size=0.2)

model = keras.models.Sequential([
    keras.layers.Embedding(input_dim=8150, output_dim=32),
    keras.layers.GRU(128),
    keras.layers.Dense(128, activation="leaky_relu",
                       kernel_initializer="he_normal", kernel_regularizer="l1"),
    keras.layers.Dropout(0.5),
    keras.layers.Dense(3, activation="softmax",
                       kernel_initializer="glorot_normal")
])
model.summary()

model.compile(optimizer='adam', loss='categorical_crossentropy',
              metrics=['accuracy'])

history = model.fit(
    X_train, y_train,
    epochs=500, validation_data=(X_valid, y_valid),
    callbacks=[keras.callbacks.EarlyStopping(
        patience=3, restore_best_weights=True)]
)

model.evaluate(X_test, y_test)
