import nltk

from nltk.stem import WordNetLemmatizer
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
wordnet_lemmatizer = WordNetLemmatizer()

file="agr_en_train.csv"
text = open(file, "r", encoding="UTF-8").read()
data = text.split("facebook_corpus_msr_")
data = [(txt.split(",", 1)[1].strip().rsplit(",", 1)[0].replace("\"","").lower(), txt.split(",", 1)[1].strip().rsplit(",", 1)[1]) for txt in data if txt != ""]
data= [x[0] for x in data]

for sentence in data:
    tokens=nltk.word_tokenize(sentence)
    print(tokens)
    pos=nltk.pos_tag(tokens)
    print(pos)
    lemmas=[wordnet_lemmatizer.lemmatize(word, pos="v") for word in tokens]
    print(lemmas)
print(data)