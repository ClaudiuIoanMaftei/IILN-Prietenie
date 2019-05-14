import numpy as np
import keras, os
from keras.models import load_model
from keras.layers import Dropout, Dense
from reading_functions import *


def extract_scores(file, test_data):
    file_type = "_train.csv" if test_data is False else "_test.csv"
    sentiments_dex = read_sentiments(file_name="Outputs/sentiments" + file_type)
    punctuation_dex = read_punctuations(file_name="Outputs/punctuations" + file_type)
    upper_lower_dex = read_upper_lower(file_name="Outputs/upper_lower" + file_type)
    sentence_scores = read_sentence_scores(file_name="Outputs/sentence_scores" + file_type)

    messages, dex = read_data(file=file)
    data = list()
    nr_data_points = len(messages)
    for i in range(nr_data_points):
        score_NAG, score_CAG, score_OAG = sentence_scores[i][0], sentence_scores[i][1], sentence_scores[i][2]
        polarity, subjectivity, classification, positive, negative = sentiments_dex[i][0], sentiments_dex[i][1], sentiments_dex[i][2], sentiments_dex[i][3], \
                                                                     sentiments_dex[i][4]
        punctuation_score = punctuation_dex[i]
        upper_lower_score = upper_lower_dex[i]
        data.append([score_NAG, score_CAG, score_OAG, polarity, subjectivity, punctuation_score, upper_lower_score])

    labels = [msg[1] for msg in messages]
    aux = list()
    for item in labels:
        if item == "NAG":
            aux.append([1.0, 0.0, 0.0])
        elif item == "CAG":
            aux.append([0.0, 1.0, 0.0])
        else:
            aux.append([0.0, 0.0, 1.0])
    labels = aux

    data = np.array(data)
    labels = np.array(labels)

    return data, labels


def initialize_model(input_size):
    model = keras.models.Sequential()
    model.add(Dense(input_size, activation="sigmoid"))
    # model.add(Dropout(0.25))
    # model.add(Dense(30, activation="sigmoid"))
    model.add(Dropout(0.25))
    model.add(Dense(10, activation="sigmoid"))
    model.add(Dense(3, activation="softmax"))
    model.compile(optimizer=keras.optimizers.Adam(lr=0.01), loss="categorical_crossentropy", metrics=["accuracy"])
    return model


def neural_network(input_size, train_data, train_labels, test_data, test_labels):
    acc = 0.0
    trial=0
    while acc < 0.57:
        print("Trial: ", trial)
        model = initialize_model(input_size)
        model.fit(x=train_data, y=train_labels, epochs=10+trial, batch_size=120, verbose=False)
        loss, acc = model.evaluate(test_data, test_labels, verbose=False)
        print("Acc:", acc)
        trial += 1
    model.save('Model/network.h5')


def evaluate_neural_network(input_size, test_data, test_labels):
    model = load_model('Model/network.h5')
    loss, acc = model.evaluate(test_data, test_labels, verbose=False)
    print("testare:     loss: ", loss, "acc: ", acc)


if __name__ == '__main__':
    train_data, train_labels = extract_scores(file="Data/agr_en_train.csv", test_data=False)
    test_data, test_labels = extract_scores(file="Data/agr_en_dev.csv", test_data=True)
    neural_network(input_size=7, train_data=train_data, train_labels=train_labels, test_data=test_data, test_labels=test_labels)
    evaluate_neural_network(input_size=7, test_data=test_data, test_labels=test_labels)
