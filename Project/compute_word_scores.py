from tokens_and_lemmas_module import read
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
        if word.strip() != "" and word != ' ':
            nr_words += 1
            score_NAG += scores[lemma_dex[word]][0]
            score_CAG += scores[lemma_dex[word]][1]
            score_OAG += scores[lemma_dex[word]][2]
    return score_NAG/nr_words, score_CAG/nr_words, score_OAG/nr_words


def compute_word_scores():
    data, dex = read("Data/agr_en_train.csv")
    fd = open("Outputs/lemmas.csv", "r", encoding="UTF-8")

    lemma_dex = dict()
    line = fd.readline().strip()
    while line:
        if line.split(',')[1] != '':
            lemma_dex[line.split(',')[0]] = line.split(',')[1]
        line = fd.readline().strip()
    fd.close()

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
        scores[word][0] = scores[word][0] / sum(absolute_scores)
        scores[word][1] = scores[word][1] / sum(absolute_scores)
        scores[word][2] = scores[word][2] / sum(absolute_scores)

    fd = open("Outputs/word_scores.csv", "w", encoding="UTF-8")
    for word in scores:
        fd.write("{},{},{},{}\n".format(word, scores[word][0], scores[word][1], scores[word][2]))
    fd.close()


if __name__ == '__main__':
    compute_word_scores()