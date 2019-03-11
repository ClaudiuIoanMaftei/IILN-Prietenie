import nltk
from nltk.corpus import wordnet as wn

# nltk.download("wordnet")
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')


# def get_pos_doc(sentences: list, word):
#     # returns something
#     for sentence in sentences:
#
#     return

sentence = "The WordNet corpus reader gives access to the Open Multilingual WordNet"
words = nltk.word_tokenize(sentence)
print([result[1] for result in nltk.pos_tag(words)])
pos = []
for result in nltk.pos_tag(words):
    if result[1] in ["JJ", "JJR", "JJS"]:
        pos.append("a")
    elif result[1] in ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ", "MD"]:
        pos.append("v")
    elif result[1] in ["RB", "RBR", "RBS", "RP", "WRB"]:
        pos.append("r")
    else:
        pos.append("n")
# print(pos)
zipped = zip(words, pos)

for content in zipped:
    print(content)
    synsets = wn.synsets(content[0], pos=content[1])
    if synsets:
        # if "V" in tags[1] and "v" in str(stuff).split(".")[1]:
        print("\t", synsets[0])
        hyponyms = synsets[0].hyponyms()
        print("\t\tHYPO:", hyponyms)
        hypernyms = synsets[0].hypernyms()
        print("\t\tHYPER:", hypernyms)
