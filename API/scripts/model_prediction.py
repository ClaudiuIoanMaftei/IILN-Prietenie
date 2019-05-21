from API.Scripts.sentiments_module import get_sentiments_score
from API.Scripts.compute_word_scores import get_sentence_score
from API.Scripts.reading_functions import read_lemmas, read_word_scores
from API.Scripts.punctuation_module import get_punctuation_score
from API.Scripts.upper_lower_module import get_upper_lower_score
from keras.models import load_model
import numpy as np

if __name__ == '__main__':
    sentences = ["We have to kill all the Palestinians unless they are resigned to live here as slaves.",
    "The Palestinians are beasts walking on two legs.",
    "We have to kill all the Palestinians unless they are resigned to live here as slaves.",
    "Now that Trump is president, I'm going to shoot you and all the blacks I can find.","Fucking faggots!",
     "You shit Jew, I'm going to kill you,", "Wipe out the Jews.", "Women are like grass, they need to be beaten/cut regularly."]


    word_scores = read_word_scores(file_name="Outputs/word_scores.csv")
    lemma_dex = read_lemmas(file_name="Outputs/lemmas.csv")
    inputs = list()
    for sentence in sentences:
        score_NAG, score_CAG, score_OAG = get_sentence_score(sentence=sentence, scores=word_scores, lemma_dex=lemma_dex)
        polarity, subjectivity, classification, positive, negative = get_sentiments_score(text=sentence)
        punctuation_score = get_punctuation_score(sentence=sentence)
        upper_lower_score = get_upper_lower_score(sentence=sentence)
        inputs.append([score_NAG, score_CAG, score_OAG, polarity, subjectivity, punctuation_score, upper_lower_score])

    model = load_model('model/network.h5')
    inputs = np.array(inputs)
    outputs = model.predict(inputs)
    for output, sentence in zip(outputs, sentences):
        maxim = max(output)
        if output[0] == maxim:
            label = "NAG"
        elif output[1] == maxim:
            label = "CAG"
        else:
            label = "OAG"
        print(sentence)
        print(label)
        print(output, '\n')
