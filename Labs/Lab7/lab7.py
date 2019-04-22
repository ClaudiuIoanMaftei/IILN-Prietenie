from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
import nltk


# nltk.download('movie_reviews')
# nltk.download('punkt')

def read(file):
    data = list()
    dex = dict()
    text = open(file, "r", encoding="UTF-8").read()
    data = text.split("facebook_corpus_msr_")
    # data = [(txt.split(",", 1)[1].strip().rsplit(",", 1)[0].replace("\"","").lower(), txt.split(",", 1)[1].strip().rsplit(",", 1)[1]) for txt in data if txt != ""]
    # punct_mark = ".,!@#$%^&*()[]{}?/:;-\n\""
    # for x in data:
    #     for chr in punct_mark:
    #         x = (x[0].replace(chr, " "),x[1])
    #     for word in x[0].split(" "):
    #         if word != "":
    #             if word in dex:
    #                 dex[word] += 1
    #             else:
    #                 dex[word] = 1

    return data


def compute_sentiments(text):
    sent = TextBlob(text)
    # The polarity score is a float within the range [-1.0, 1.0]
    # where negative value indicates negative text and positive
    # value indicates that the given text is positive.
    polarity = sent.sentiment.polarity
    # The subjectivity is a float within the range [0.0, 1.0] where
    # 0.0 is very objective and 1.0 is very subjective.
    subjectivity = sent.sentiment.subjectivity

    sent = TextBlob(text, analyzer=NaiveBayesAnalyzer())
    classification = sent.sentiment.classification
    positive = sent.sentiment.p_pos
    negative = sent.sentiment.p_neg
    # neutral       = sent.sentiment.p_net

    if abs(polarity) <= 0.33333333:
        classification = "net"

    return polarity, subjectivity, classification, positive, negative


data = read(file="agr_en_train.csv")
fd = open("sentimente.txt", "w+")
for message_index in range(6000, len(data)):
    polarity, subjectivity, classification, positive, negative = compute_sentiments(data[message_index])
    fd.write(str(message_index) + ' ' + str(polarity) + ' ' + str(subjectivity) + ' ' + str(classification) + ' ' + str(positive) + ' ' + str(negative) + '\n')
    print(str(message_index) + ' ' + str(polarity) + ' ' + str(subjectivity) + ' ' + str(classification) + ' ' + str(positive) + ' ' + str(negative) + '\n')
    print(message_index)
