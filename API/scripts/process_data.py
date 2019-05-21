from API.Scripts.compute_word_scores import compute_word_scores, compute_sentence_scores
from API.Scripts.punctuation_module import compute_punctuation
from API.Scripts.tokens_and_lemmas_module import compute_tokens_and_lemmas
from API.Scripts.upper_lower_module import compute_upper_lower
from API.Scripts.train_model import read_word_scores, read_lemmas
from API.Scripts.reading_functions import read_data


def process_data(input_data, test_data):
    # nltk.download('movie_reviews')
    # nltk.download('punkt')
    # nltk.download('averaged_perceptron_tagger')
    # nltk.download('wordnet')
    file_type = "_train.csv" if test_data is False else "_test.csv"
    print("compute_tokens_and_lemmas started!")
    if test_data is False:
        compute_tokens_and_lemmas(input_file="Data/agr_en_train.csv", output_token_file="Outputs/tokens.csv", output_lemmas_file="Outputs/lemmas.csv")
    print("compute_tokens_and_lemmas ended!")

    print("compute_word_scores started!")
    if test_data is False:
        compute_word_scores(input_data="Data/agr_en_train.csv", input_lemmas="Outputs/lemmas.csv", output_word_scores="Outputs/word_scores.csv")
    print("compute_word_scores ended!")


    print("compute_upper_lower started!")
    compute_upper_lower(input_data=input_data, output_data="Outputs/upper_lower" + file_type)
    print("compute_upper_lower ended!")

    print("compute_punctuation started!")
    compute_punctuation(input_data=input_data, output_data="Outputs/punctuations" + file_type)
    print("compute_punctuation ended!")

    print("compute_sentence_scores started!")
    scores = read_word_scores(file_name="Outputs/word_scores.csv")
    lemma_dex = read_lemmas(file_name="Outputs/lemmas.csv")
    data, dex = read_data(file=input_data)
    compute_sentence_scores(data=data, scores=scores, lemma_dex=lemma_dex, output_sentence_score="Outputs/sentence_scores" + file_type)
    print("compute_sentence_scores ended!")

    print("compute_sentiments started!")
    # don't run this unless you're willing to wait until the heat death of the universe
    # compute_sentiments(input_data=input_data, output_data="Outputs/sentiments" + file_type)
    print("compute_sentiments ended!")


if __name__ == '__main__':
    process_data(input_data="Data/agr_en_train.csv", test_data=False)
    process_data(input_data="Data/agr_en_dev.csv", test_data=True)