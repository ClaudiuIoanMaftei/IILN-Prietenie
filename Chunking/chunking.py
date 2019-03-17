import json
import re

from textblob import TextBlob
import nltk


def read(file):
    dex = dict()
    text = open(file, "r", encoding="UTF-8").read()
    data = text.split("facebook_corpus_msr_")
    data = [(txt.split(",", 1)[1].strip().rsplit(",", 1)[0].replace("\"", "").lower(),
             txt.split(",", 1)[1].strip().rsplit(",", 1)[1]) for txt in data if txt != ""]
    punct_mark = ".,!@#$%^&*()[]{}\\?/:;-\n\""
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


# data, dex = read("../Data/agr_en_train.csv")
# reg_exp = "NP: {<DT>?<JJ>*<NN>}"
# with open("chunking.txt", "w") as fd:
#     for line in data:
#         try:
#             result = TextBlob(line[0])
#             # print("\t", result)
#             rp = nltk.RegexpParser(reg_exp)
#             print(type(rp.parse(result.tags)))
#             fd.write(str(rp.parse(result.tags))+"\n\n")
#         except:
#             pass
# dictionary = {}
# set_np = set()
# set_restul = set()
# for lin in data:
#     result = TextBlob(lin[0])
#     rp = nltk.RegexpParser(reg_exp)
#     copac = rp.parse(result.tags)
#     for ceva in copac:
#         if "NP" in str(ceva):
#             if str(ceva) not in dictionary.keys():
#                 dictionary[str(ceva)] = 1
#             else:
#                 dictionary[str(ceva)] += 1
#             set_np.add(str(ceva))
#         else:
#             set_restul.add(str(ceva))
# print("NPs:", len(set_np))
# print("restul:", len(set_restul))
# with open("chunking.txt", "r") as fd:
#     set_nouns = set()
#     print(fd.read().count("NP"))
#     for line in fd:
#         if "NP" in line:
        # set.add()
# with open("dictionary.txt", "w") as fd:
    # fd.write(json.dumps(dictionary, indent=4))
    # fd.write(json.dumps(sorted(dictionary.items(), key=lambda kv: kv[1]), indent=4))
data, dex = read("../Data/agr_en_train.csv")
reg_exp = r"""NP: {<DT>?<JJ|JJS>*<NN|NNS>}  
                  {<NNP>+}
              VB: {<MD>?<V.*><TO>?<V.*>?<IN>*}
                  """
test = "Diana Mihai Claudiu are to become the friends"
for index in range(10):
    result = TextBlob(data[index][0])
    rp = nltk.RegexpParser(reg_exp)
    print(str(rp.parse(result.tags)))
