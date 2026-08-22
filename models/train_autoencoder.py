from tensorflow.keras.layers import Input
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Model

input_dim = 155

inputs = Input(shape=(input_dim,))

encoded = Dense(128, activation="relu")(inputs)
encoded = Dense(64, activation="relu")(encoded)

decoded = Dense(128, activation="relu")(encoded)
decoded = Dense(input_dim, activation="linear")(decoded)

autoencoder = Model(inputs, decoded)

autoencoder.compile(optimizer="adam", loss="mse")

autoencoder.fit(X_normal, X_normal, epochs=20, batch_size=256)

autoencoder.save("autoencoder.h5")
