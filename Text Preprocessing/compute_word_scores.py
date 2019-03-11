import sys, copy
sys.path.insert(0, '../Initial/')
from todo import read
data, dex = read("../Data/agr_en_train.csv")
fd = open("Outputs/lemmas.txt", "r", encoding="UTF-8")

lemma_dex = dict()
line = fd.readline().strip()
while line:
    try:
        lemma_dex[line.split('\t')[0]] = line.split('\t')[1]
    except:
        pass
    line = fd.readline().strip()
fd.close()

scores = dict()
for word in set(lemma_dex.values()):
    scores[word] = [0]*3

punct_mark = ".,!@#$%^&*()[]{}?/:;-\n\""
for x in data:
    for chr in punct_mark:
        x = (x[0].replace(chr, " "), x[1])
    for word in x[0].split(' '):
        if word.strip() != "" and word != ' ':
            try:
                if x[1] == "NAG":
                    scores[lemma_dex[word]][0] += 1
                elif x[1] == "CAG":
                    scores[lemma_dex[word]][1] += 1
                else:
                    scores[lemma_dex[word]][2] += 1
            except:
                pass

for word in scores:
    absolute_scores = copy.copy(scores[word])
    scores[word][0] = scores[word][0] / sum(absolute_scores)
    scores[word][1] = scores[word][1] / sum(absolute_scores)
    scores[word][2] = scores[word][2] / sum(absolute_scores)


fd = open("Outputs/scores.txt", "w", encoding="UTF-8")
for word in scores:
    fd.write("{} - ({},{},{})\n".format(word, scores[word][0], scores[word][1], scores[word][2]))
fd.close()
