import nltk
from nltk.stem import WordNetLemmatizer
from API.scripts.reading_functions import read_data


def compute_tokens_and_lemmas(input_file, output_token_file, output_lemmas_file):
    wordnet_lemmatizer = WordNetLemmatizer()
    msg_data, dex = read_data(input_file)
    fd = open(output_token_file, 'w', encoding="UTF-8")
    for sentence, label in msg_data:
        tokens = nltk.word_tokenize(sentence)
        for token in tokens:
            if str(token) is not ',':
                fd.write(str(token) + ',')
        fd.write("\n")
    with open(output_lemmas_file, "w", encoding="UTF-8") as f:
        for word in dex:
            f.write(word)
            f.write(',')
            f.write(wordnet_lemmatizer.lemmatize(word))
            f.write('\n')


if __name__ == '__main__':
    compute_tokens_and_lemmas(input_file="../test/input.txt", output_token_file="../test/test_tokens.csv", output_lemmas_file="../test/test_lemmas.csv")
