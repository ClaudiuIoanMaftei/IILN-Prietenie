from sentiments_module import get_sentiments_score
from compute_word_scores import get_sentence_score
from train_model import read_lemma_dex
from train_model import read_word_scores
from punctuation_module import get_punctuation_score
from upper_lower_module import get_upper_lower_score


sentence = "The quick brown fox jumps over the lazy dog."

word_scores = read_word_scores(file=open("Outputs/word_scores.csv", 'r', encoding="UTF-8"))
lemma_dex = read_lemma_dex(file=open("Outputs/lemmas.csv", 'r', encoding="UTF-8"))

score_NAG, score_CAG, score_OAG = get_sentence_score(sentence=sentence, scores=word_scores, lemma_dex=lemma_dex)
polarity, subjectivity, classification, positive, negative = get_sentiments_score(text=sentence)
punctuation_score = get_punctuation_score(sentence=sentence)
upper_lower_score = get_upper_lower_score(sentence=sentence)
