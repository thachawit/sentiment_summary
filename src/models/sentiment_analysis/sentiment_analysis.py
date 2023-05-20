import tensorflow as tf

class SentimentAnalysis(tf.keras.Model):
    def __init__(self) -> None:
        super().__init__()
        self.embedding = tf.keras.layers.Embedding(
            input_dim=8150, output_dim=32)
        self.gru = tf.keras.layers.GRU(128)
        self.dense1 = tf.keras.layers.Dense(128, activation="leaky_relu",
                                            kernel_initializer="he_normal", kernel_regularizer="l1")
        self.dropout = tf.keras.layers.Dropout(0.5)
        self.dense2 = tf.keras.layers.Dense(3, activation="softmax",
                                            kernel_initializer="glorot_normal")

    def call(self, inputs, training=False):
        x = self.embedding(inputs)
        x = self.gru(x)

        x = self.dense1(x)
        if training:
            x = self.dropout(x)

        x = self.dense2(x)

        return x