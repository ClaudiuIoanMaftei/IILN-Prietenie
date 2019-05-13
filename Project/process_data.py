import nltk
from compute_word_scores import compute_word_scores
from punctuation_module import compute_punctuation
from sentiments_module import compute_sentiments
from tokens_and_lemmas_module import compute_tokens_and_lemmas
from upper_lower_module import compute_upper_lower

def process_data():
    # nltk.download('movie_reviews')
    # nltk.download('punkt')
    # nltk.download('averaged_perceptron_tagger')
    # nltk.download('wordnet')

    print("compute_tokens_and_lemmas started!")
    compute_tokens_and_lemmas()
    print("compute_tokens_and_lemmas ended!")
    print("compute_upper_lower started!")
    compute_upper_lower()
    print("compute_upper_lower ended!")
    print("compute_punctuation started!")
    compute_punctuation()
    print("compute_punctuation ended!")
    print("compute_word_scores started!")
    compute_word_scores()
    print("compute_word_scores ended!")
    print("compute_sentiments started!")
    # don't run this unless you're willing to wait until the heat death of the universe
    # compute_sentiments()
    print("compute_sentiments ended!")


if __name__ == '__main__':
    process_data()
