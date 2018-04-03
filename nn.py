from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout
import pandas as pd
import numpy as np


def get_model(x, y):
    print('Getting model...')
    model = Sequential()
    model.add(Dense(20, input_dim=(x.shape[1]), activation='relu'))
    model.add(Dense(15, activation='relu'))
    model.add(Dense(10, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
    print('Model is ready!')
    return model


database = pd.read_csv('numeric_database.csv', dtype='float')
y_data_train = database['starting_price'][:int(database.shape[0]*0.9)]
y_data_test = database['starting_price'][int(database.shape[0]*0.9):]
del database['starting_price'], database['Unnamed: 0']
x_data_train = database[:int(database.shape[0]*0.9)]
x_data_test = database[int(database.shape[0]*0.9):]
m = get_model(x_data_train, y_data_train)
m.fit(x_data_train, y_data_train, epochs=1000, batch_size=128, verbose=1)
prediction = m.predict(x_data_test)
print(prediction.to_matrix())
print(y_data_test.to_matrix())

