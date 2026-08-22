from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D
from tensorflow.keras.layers import MaxPooling1D
from tensorflow.keras.layers import Bidirectional
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout

model = Sequential()

model.add(Conv1D(filters=64, kernel_size=3, activation="relu", input_shape=(155, 1)))

model.add(MaxPooling1D())

model.add(Bidirectional(LSTM(64)))

model.add(Dropout(0.3))

model.add(Dense(64, activation="relu"))

model.add(Dense(13, activation="softmax"))

model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])

model.fit(X_train, y_train, epochs=20, batch_size=128)

model.save("cnn_bilstm.h5")
