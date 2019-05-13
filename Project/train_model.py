import numpy as np
from tokens_and_lemmas_module import read
import keras, os
from keras.layers import InputLayer, Dropout, Dense
from compute_word_scores import get_sentence_score

def read_word_scores(file):
    word_scores = dict()
    line = file.readline().strip()
    while line:
        word, score_NAG, score_CAG, score_OAG = line.split(',')[0], float(line.split(',')[1]), float(line.split(',')[2]), float(line.split(',')[3])
        word_scores[word] = [score_NAG, score_CAG, score_OAG]
        line = file.readline().strip()
    return word_scores


def read_lemmas(file):
    lemmas = dict()
    line = file.readline().strip()
    while line:
        lemmas[line.split(',')[0]] = line.split(',')[1]
        line = file.readline().strip()
    return lemmas


def read_punctuations(file):
    pairs = dict()
    line = file.readline().strip()
    while line:
        pairs[int(line.split(',')[0])] = float(line.split(',')[1])
        line = file.readline().strip()
    return pairs


def read_upper_lower(file):
    pairs = dict()
    line = file.readline().strip()
    while line:
        pairs[int(line.split(',')[0])] = float(line.split(',')[1])
        line = file.readline().strip()
    return pairs


def read_sentiments(file):
    sentiments = dict()
    line = file.readline().strip()
    while line:
        index, polarity, subjectivity, classification, positive, negative = int(line.split(',')[0]), float(line.split(',')[1]), float(line.split(',')[2]), \
                                                                            line.split(',')[3], float(line.split(',')[4]), float(line.split(',')[5])
        sentiments[index] = [polarity, subjectivity, classification, positive, negative]
        line = file.readline().strip()
    return sentiments


def extract_scores(file):
    sentiments_dex = read_sentiments(file=open("Outputs/sentiments.csv", 'r', encoding="UTF-8"))
    punctuation_dex = read_punctuations(file=open("Outputs/punctuations.csv", 'r', encoding="UTF-8"))
    upper_lower_dex = read_upper_lower(file=open("Outputs/upper_lower.csv", 'r', encoding="UTF-8"))
    word_scores = read_word_scores(file=open("Outputs/word_scores.csv", 'r', encoding="UTF-8"))
    lemmas_dex = read_lemmas(file=open("Outputs/lemmas.csv", 'r', encoding="UTF-8"))

    messages, dex = read(file=file)
    data = list()
    nr_data_points = len(messages)
    for i in range(nr_data_points):
        try:
            score_NAG, score_CAG, score_OAG = get_sentence_score(sentence=messages[i][0], scores=word_scores, lemma_dex=lemmas_dex)
        except:
            pass
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


def neural_network(input_size, train_data, train_labels, test_data, test_labels):
    # if os.path.isfile("network"):
    #     model = keras.models.load_model("network")
    # else:
    model = keras.models.Sequential()
    model.add(InputLayer((input_size,)))
    model.add(Dropout(0.25))
    model.add(Dense(30, activation="sigmoid"))
    model.add(Dropout(0.25))
    model.add(Dense(15, activation="sigmoid"))
    # model.add(Dropout(0.25))
    # model.add(Dense(12000, activation="sigmoid"))
    model.add(Dense(3, activation="softmax"))
    model.compile(optimizer=keras.optimizers.Adam(lr=0.1), loss="categorical_crossentropy", metrics=["accuracy"])
    model.fit(x=train_data, y=train_labels, epochs=10, batch_size=100, verbose=True)
    model.save("network")

    loss, acc = model.evaluate(test_data, test_labels)
    print("testare:loss", loss, "acc:", acc)


if __name__ == '__main__':
    train_data, train_labels = extract_scores(file="Data/agr_en_train.csv")
    test_data, test_labels = extract_scores(file="Data/agr_en_dev.csv")
    neural_network(input_size=7, train_data=train_data, train_labels=train_labels, test_data=test_data, test_labels=test_labels)
