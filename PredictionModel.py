import statistics
import numpy
import pandas
import sklearn.metrics as metric
from keras.layers import LSTM, Dense, Bidirectional, TimeDistributed, ConvLSTM2D, Dropout, Flatten
from keras.legacy_tf_layers.convolutional import Conv1D
from keras.legacy_tf_layers.pooling import MaxPooling1D
from keras.models import Sequential
import tensorflow as tf

import Constants
import Util


def load_dataset(crypto, currency):
    filename = Util.generate_filename(crypto, currency, Constants.STAGE_PROCESSED)
    dataframe = pandas.read_csv(Constants.DATASET_DIRECTORY + "/" + filename)
    print("dataset loaded")

    return dataframe.values


def preprocess_data(dataset, testsize, steps):
    test_len = int(len(dataset) * testsize)
    train_len = len(dataset) - test_len
    trainset = dataset[0: train_len, 5].astype('float32')
    testset = dataset[train_len: len(dataset), 5].astype('float32')
    xtrain, ytrain = reconfigure_data(trainset, steps)
    xtest, ytest = reconfigure_data(testset, steps)
    print("preprocessing completed")

    return xtrain, ytrain, xtest, ytest, steps


def reconfigure_data(dataset, steps):
    dataset_x, dataset_y = [], []

    for i in range(len(dataset) - steps - 1):
        dataset_x.append(dataset[i: (i + steps)])
        dataset_y.append(dataset[i + steps])

    return numpy.array(dataset_x), numpy.array(dataset_y)


def create_models(steps):
    models = dict()
    lstm_base = Sequential()
    lstm_base.add(LSTM(50, activation=tf.keras.activations.relu, return_sequences=True, input_shape=(steps, 1)))
    # lstm_base.add(Dropout(0.1))
    lstm_base.add(Dense(10))
    lstm_base.add(Dense(1))
    lstm_base.compile(optimizer=tf.keras.optimizers.Adam(), loss=tf.keras.losses.mean_squared_error)
    models["LSTM vanilla"] = lstm_base

    lstm_stacked = Sequential()
    lstm_stacked.add(LSTM(50, activation=tf.keras.activations.relu, return_sequences=True, input_shape=(steps, 1)))
    # lstm_base.add(Dropout(0.1))
    lstm_stacked.add(LSTM(50, activation=tf.keras.activations.relu))
    # lstm_base.add(Dropout(0.1))
    lstm_stacked.add(Dense(10))
    lstm_stacked.add(Dense(1))
    lstm_stacked.compile(optimizer=tf.keras.optimizers.Adam(), loss=tf.keras.losses.mean_squared_error)
    models["LSTM stacked"] = lstm_stacked

    lstm_bidir = Sequential()
    lstm_bidir.add(Bidirectional(LSTM(50, activation=tf.keras.activations.relu), input_shape=(steps, 1)))
    # lstm_base.add(Dropout(0.1))
    lstm_bidir.add(Dense(10))
    lstm_bidir.add(Dense(1))
    lstm_bidir.compile(optimizer=tf.keras.optimizers.Adam(), loss=tf.keras.losses.mean_squared_error)
    models["LSTM bidirectional"] = lstm_bidir

    lstm_cnn = Sequential()
    lstm_cnn.add(TimeDistributed(Conv1D(filters=64, kernel_size=1, activation=tf.keras.activations.relu),
                                 input_shape=(None, steps, 1)))
    # lstm_base.add(Dropout(0.1))
    lstm_cnn.add(TimeDistributed(MaxPooling1D(pool_size=1, strides=1)))
    lstm_cnn.add(TimeDistributed(Flatten()))
    # lstm_base.add(Dropout(0.1))
    lstm_cnn.add(LSTM(50, activation=tf.keras.activations.relu))
    # lstm_base.add(Dropout(0.1))
    lstm_cnn.add(Dense(10))
    lstm_cnn.add(Dense(1))
    lstm_cnn.compile(optimizer=tf.keras.optimizers.Adam(), loss=tf.keras.losses.mean_squared_error)
    models["LSTM CNN"] = lstm_cnn

    lstm_conv = Sequential()
    lstm_conv.add(ConvLSTM2D(filters=64, kernel_size=(1, 1), activation=tf.keras.activations.relu,
                             input_shape=(steps, 1, steps, 1)))
    lstm_conv.add(Flatten())
    # lstm_base.add(Dropout(0.1))
    lstm_conv.add(Dense(10))
    lstm_conv.add(Dense(1))
    lstm_conv.compile(optimizer=tf.keras.optimizers.Adam(), loss=tf.keras.losses.mean_squared_error)
    models["LSTM conv"] = lstm_conv
    print("models created")

    return models


def train_and_predict_model(xtrain, ytrain, xtest, ytest, steps):
    models = create_models(steps)

    best_score = 0
    best_model = Sequential()
    for cur in models.keys():
        model = models[cur]
        print("training started for: ", cur)

        if cur in ["LSTM vanilla", "LSTM stacked", "LSTM bidirectional"]:
            x_train_reshaped = numpy.reshape(xtrain, (xtrain.shape[0], xtrain.shape[1], 1))
            x_test_reshaped = numpy.reshape(xtest, (xtest.shape[0], xtest.shape[1], 1))
        elif cur == "LSTM conv":
            x_train_reshaped = numpy.reshape(xtrain, (xtrain.shape[0], xtrain.shape[1], 1, 1, 1))
            x_test_reshaped = numpy.reshape(xtest, (xtest.shape[0], xtest.shape[1], 1, 1, 1))
        else:
            x_train_reshaped = numpy.reshape(xtrain, (xtrain.shape[0], xtrain.shape[1], 1, 1))
            x_test_reshaped = numpy.reshape(xtest, (xtest.shape[0], xtest.shape[1], 1, 1))
        model.fit(x_train_reshaped, ytrain, epochs=500, verbose=0, batch_size=10)
        ypred = model.predict(x_test_reshaped)
        mse = metric.mean_squared_error(ytest, ypred.flatten())
        r2_score = metric.r2_score(ytest, ypred.flatten())
        print("model {} mse: {}, score: {}".format(cur, mse, r2_score))

        if r2_score > best_score:
            best_score = r2_score
            best_model = model

    best_model.save(Constants.PREDICTION_MODEL_DIRECTORY + "/" + "trained_lstm_model")


dataset = load_dataset("doge", "inr")
xtrain, ytrain, xtest, ytest, step = preprocess_data(dataset, 0.15, 1)
train_and_predict_model(xtrain, ytrain, xtest, ytest, step)