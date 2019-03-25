from nltk.wsd import lesk
from nltk.corpus import wordnet as wn

sent = 'I went to the bank to deposit my money'
ambiguous = 'bank'
res2 = lesk(sent, ambiguous)
# Synset('bank.v.04')
result = lesk(sent, ambiguous).definition()
print(result)

# sinonim = str(res2).split('\'')[1]
print(res2)
sinonim = res2.lemmas()
for lemma in sinonim:
    print(lemma, lemma.count())
# print(sinonim)
