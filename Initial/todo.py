#take into account lower vs upper letters
#take into account punctuation marks
#convert words to lemma
#nr de aparitii
#label words as NAG OAG CAG
#emotion label API
#attempt semantical labeling of words, not lexical

# dex={"a":1, "b":2}
# print(sorted([(x,dex[x]) for x in dex.keys()],reverse=True, key=lambda item: item[1]))

# import keras, os
import numpy as np
# from keras.layers import InputLayer, Dropout, Dense


def read(file):
    data = list()
    dex = dict()
    text = open(file, "r", encoding="UTF-8").read()
    data = text.split("facebook_corpus_msr_")
    data = [(txt.split(",", 1)[1].strip().rsplit(",", 1)[0].replace("\"","").lower(), txt.split(",", 1)[1].strip().rsplit(",", 1)[1]) for txt in data if txt != ""]
    punct_mark = ".,!@#$%^&*()[]{}?/:;-\n\""
    for x in data:
        for chr in punct_mark:
            x = (x[0].replace(chr, " "),x[1])
        for word in x[0].split(" "):
            if word != "":
                if word in dex:
                    dex[word] += 1
                else:
                    dex[word] = 1

    return data, dex

def neural_network(input_size, train_data, train_labels,test_data,test_labels):
    if os.path.isfile("network"):
        model=keras.models.load_model("network")
    else:
        model = keras.models.Sequential()
        model.add(InputLayer((input_size,)))
        model.add(Dropout(0.25))
        model.add(Dense(6000, activation="sigmoid"))
        model.add(Dropout(0.25))
        model.add(Dense(1000, activation="sigmoid"))
        # model.add(Dropout(0.25))
        # model.add(Dense(12000, activation="sigmoid"))
        model.add(Dense(3, activation="softmax"))
        model.compile(optimizer=keras.optimizers.Adam(lr=0.1), loss="categorical_crossentropy", metrics=["accuracy"])
        model.fit(x=train_data, y=train_labels, epochs=3, batch_size=25, verbose=True)
        model.save("network")

    loss, acc = model.evaluate(test_data, test_labels)
    print("testare:loss",loss,"acc:",acc)


def get_lists(data, dex):
    train_labels = [x[1] for x in data]
    aux = list()
    for item in train_labels:
        if item == "NAG":
            aux.append([1, 0, 0])
        elif item == "CAG":
            aux.append([0, 1, 0])
        else:
            aux.append([0, 0, 1])
    train_labels = aux
    train_data = list()
    for text in [x[0] for x in data]:
        train_data.append([text.count(word) for word in dex.keys()])

    train_data = np.array(train_data)
    train_labels = np.array(train_labels)

    return train_data,train_labels

if __name__ == '__main__':
    msg_test_data,dex=read("agr_en_dev.csv")
    test_data, test_labels=get_lists(msg_test_data,dex)

    msg_train_data,dex=read("agr_en_train.csv")
    train_data, train_labels=get_lists(msg_train_data,dex)
    neural_network(len(dex.keys()), train_data, train_labels,test_data,test_labels)









# print(sorted([(x, dex[x]) for x in dex.keys()], reverse=True, key = lambda item:item[1]))
