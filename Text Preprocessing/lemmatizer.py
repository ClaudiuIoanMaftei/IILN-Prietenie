import nltk

from nltk.stem import WordNetLemmatizer
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('wordnet')
wordnet_lemmatizer = WordNetLemmatizer()

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

msg_test_data,dex=read("../Data/agr_en_train.csv")
print("boop")
with open("Outputs/lemmas.txt","w", encoding="UTF-8") as f:
    for word in dex:
        f.write(word)
        f.write('\t')
        f.write(wordnet_lemmatizer.lemmatize(word))
        f.write('\n')