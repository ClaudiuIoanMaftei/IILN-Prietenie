from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
from tokens_and_lemmas_module import read


def get_sentiments_score(text):
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


def compute_sentiments():
    data_msg, dex = read(file="Data/agr_en_train.csv")
    data_msg = [data[0] for data in data_msg]
    fd = open("Outputs/sentimente.txt", "w+")
    for message_index in range(6000, len(data_msg)):
        polarity, subjectivity, classification, positive, negative = get_sentiments_score(data_msg[message_index])
        fd.write(str(message_index) + ' ' + str(polarity) + ' ' + str(subjectivity) + ' ' + str(classification) + ' ' + str(positive) + ' ' + str(negative) + '\n')


if __name__ == '__main__':
    compute_sentiments()
