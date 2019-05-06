from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree
import nltk
from Chunking import chunking
import json

# nltk.download('maxent_ne_chunker')
# nltk.download('words')

texts = chunking.read("../Data/agr_en_train.csv")

def get_continuous_chunks(text):
    # chunked = ne_chunk(pos_tag(word_tokenize(text)))
    # print(chunked)
    continuous_chunk = set()
    # current_chunk = []
    # for i in chunked:
    #     if type(i) == Tree:
    #         print(i.leaves())
    #         current_chunk.append(" ".join([token for token, pos in i.leaves()]))
    #     elif current_chunk:
    #         # print(current_chunk)
    #         named_entity = " ".join(current_chunk)
    #         if named_entity not in continuous_chunk:
    #             continuous_chunk.append(named_entity)
    #         current_chunk = []
    #     else:
    #         continue
    # ------------------------------------------------------------------------------
    for sent in nltk.sent_tokenize(text):
        for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
            if hasattr(chunk, 'label'):
                continuous_chunk.add((chunk.label(), ' '.join(c[0] for c in chunk)))
    return list(continuous_chunk)


# text = "WASHINGTON -- In the wake of a string of abuses by New York police officers in the 1990s, Loretta E. Lynch, the top federal prosecutor in Brooklyn, spoke forcefully about the pain of a broken trust that African-Americans felt and said the responsibility for repairing generations of miscommunication and mistrust fell to law enforcement."
# print(get_continuous_chunks(text))

dictionary = dict()
with open("ner.txt","w",encoding="UTF-8") as fd:
    for text in texts:
        result = get_continuous_chunks(text)
        if result:
            for res in result:
                if res[0] in dictionary.keys():
                    dictionary[res[0]] += 1
                else:
                    dictionary[res[0]] = 1
            fd.write(str(result)+"\n")

print("Number of categories:", len(dictionary.keys()))
for key in dictionary.keys():
    print("For {}: {}".format(key, dictionary[key]))
