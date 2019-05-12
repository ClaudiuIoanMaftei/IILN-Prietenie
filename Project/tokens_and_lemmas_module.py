import nltk
from nltk.stem import WordNetLemmatizer


def read(file):
    dex = dict()
    text = open(file, "r", encoding="UTF-8").read()
    data = text.split("facebook_corpus_msr_")
    data = [(txt.split(",", 1)[1].strip().rsplit(",", 1)[0].replace("\"", "").lower(), txt.split(",", 1)[1].strip().rsplit(",", 1)[1]) for txt in data if txt != ""]
    punct_mark = ".,!@#$%^&*()[]{}?/:;-\n\""
    for x in data:
        for chr in punct_mark:
            x = (x[0].replace(chr, " "), x[1])
        for word in x[0].split(" "):
            if word != "":
                if word in dex:
                    dex[word] += 1
                else:
                    dex[word] = 1

    return data, dex


def compute_tokens_and_lemmas():
    wordnet_lemmatizer = WordNetLemmatizer()
    msg_data, dex = read("Data/agr_en_train.csv")
    fd = open('Outputs/tokens.csv', 'w', encoding="UTF-8")
    for sentence, label in msg_data:
        tokens = nltk.word_tokenize(sentence)
        for token in tokens:
            if str(token) is not ',':
                fd.write(str(token) + ',')
        fd.write("\n")
    with open("Outputs/lemmas.csv", "w", encoding="UTF-8") as f:
        for word in dex:
            f.write(word)
            f.write(',')
            f.write(wordnet_lemmatizer.lemmatize(word))
            f.write('\n')


if __name__ == '__main__':
    compute_tokens_and_lemmas()
