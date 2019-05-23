from API.scripts.reading_functions import read_data, read_lemmas
from nltk.wsd import lesk
import copy

punct_mark = ".,!@#$%^&*()[]{}?/:;-\n\""


def get_synonyms(sent, ambiguous):
    try:
        synonyms = lesk(sent, ambiguous).lemmas()
    except:
        return []
    return set(lemma.name() for lemma in synonyms if '_' not in str(lemma.name()) and ambiguous != str(lemma.name()))


def get_sentence_score(sentence, scores, lemma_dex):
    processed_sentence = sentence
    score_NAG = 0
    score_CAG = 0
    score_OAG = 0
    for chr in punct_mark:
        processed_sentence = processed_sentence.replace(chr, " ")
    nr_words = 0
    for word in processed_sentence.split(' '):
        # todo: logica asta mai poate fi schimbata
        try:
            if word.strip() != "" and word != ' ':
                nr_words += 1
                score_NAG += scores[lemma_dex[word]][0]
                score_CAG += scores[lemma_dex[word]][1]
                score_OAG += scores[lemma_dex[word]][2]
        except:
            pass
    return score_NAG / nr_words, score_CAG / nr_words, score_OAG / nr_words


def compute_sentence_scores(data, scores, lemma_dex, output_sentence_score):
    fd = open(output_sentence_score, "w", encoding="UTF-8")
    index = 0
    for sentence in [data_label[0] for data_label in data]:
        nag, cag, oag = get_sentence_score(sentence, scores, lemma_dex)
        fd.write(str(index) + "," + str(nag) + "," + str(cag) + "," + str(oag) + "\n")
        index += 1
    fd.close()


def compute_word_scores(input_data, input_lemmas, output_word_scores):
    data, dex = read_data(input_data)
    lemma_dex = read_lemmas(file_name=input_lemmas)
    scores = dict()
    for word in set(lemma_dex.values()):
        scores[word] = [0] * 3

    for sent, label in data:
        processed_sentence = sent
        for chr in punct_mark:
            processed_sentence = processed_sentence.replace(chr, " ")
        for word in processed_sentence.split(' '):
            if word.strip() != "" and word != ' ':
                synonyms = get_synonyms(sent=sent, ambiguous=word)
                for synonym in synonyms:
                    if synonym not in scores:
                        scores[synonym] = [0] * 3
                index = 2
                if label == "NAG":
                    index = 0
                elif label == "CAG":
                    index = 1
                scores[lemma_dex[word]][index] += 1
                for synonym in synonyms:
                    scores[synonym][index] += 1

    for word in scores:
        absolute_scores = copy.copy(scores[word])
        try:
            scores[word][0] = scores[word][0] / sum(absolute_scores)
            scores[word][1] = scores[word][1] / sum(absolute_scores)
            scores[word][2] = scores[word][2] / sum(absolute_scores)
        except:
            pass

    fd = open(output_word_scores, "w", encoding="UTF-8")
    for word in scores:
        fd.write("{},{},{},{}\n".format(word, scores[word][0], scores[word][1], scores[word][2]))
    fd.close()


if __name__ == '__main__':
    compute_word_scores(input_data="Data/agr_en_train.csv", input_lemmas="Outputs/lemmas.csv",
                        output_word_scores="Outputs/word_scores.csv")
