from API.scripts.sentiments_module import get_sentiments_score
from API.scripts.compute_word_scores import get_sentence_score
from API.scripts.reading_functions import read_lemmas, read_word_scores, read_data
from API.scripts.punctuation_module import get_punctuation_score
from API.scripts.upper_lower_module import get_upper_lower_score
from keras.models import load_model
import numpy as np


def compute_prediction(sentences_data, words_scores_data, lemmas_data, output_data):
    data, dex = read_data(sentences_data)
    sentences = list()
    for tuple_data in data:
        sentences.append(tuple_data[0])
    word_scores = read_word_scores(file_name=words_scores_data)
    lemma_dex = read_lemmas(file_name=lemmas_data)
    inputs = list()
    for sentence in sentences:
        # pe undeva pe aici nu proceseaza bine (cred)
        score_NAG, score_CAG, score_OAG = get_sentence_score(sentence=sentence, scores=word_scores, lemma_dex=lemma_dex)
        polarity, subjectivity, classification, positive, negative = get_sentiments_score(text=sentence)
        punctuation_score = get_punctuation_score(sentence=sentence)
        upper_lower_score = get_upper_lower_score(sentence=sentence)
        inputs.append([score_NAG, score_CAG, score_OAG, polarity, subjectivity, punctuation_score, upper_lower_score])

    model = load_model('../model/network.h5')
    inputs = np.array(inputs)
    outputs = model.predict(inputs)
    with open(output_data, "w") as fd:
        for output, sentence in zip(outputs, sentences):
            maxim = max(output)
            if output[0] == maxim:
                label = "NAG"
            elif output[1] == maxim:
                label = "CAG"
            else:
                label = "OAG"
            fd.write(sentence + "," + label + "," + str(output) + "\n")
    return


if __name__ == '__main__':
    print("Prediction module.")
    print(compute_prediction("../test/input.txt", "../test/result_words.csv","../test/result_lemmas.csv","../test/result.txt"))
