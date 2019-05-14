from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
from reading_functions import read_data


def get_sentiments_score(text):
    sent = TextBlob(text)
    polarity = sent.sentiment.polarity
    subjectivity = sent.sentiment.subjectivity
    sent = TextBlob(text, analyzer=NaiveBayesAnalyzer())
    classification = sent.sentiment.classification
    positive = sent.sentiment.p_pos
    negative = sent.sentiment.p_neg

    if abs(polarity) <= 0.33333333:
        classification = "net"

    return polarity, subjectivity, classification, positive, negative


def compute_sentiments(input_data, output_data):
    data_msg, dex = read_data(file=input_data)
    data_msg = [data[0] for data in data_msg]
    for message_index in range(2160, len(data_msg)):
        fd = open(output_data, "a")
        polarity, subjectivity, classification, positive, negative = get_sentiments_score(data_msg[message_index])
        fd.write(str(message_index) + ',' + str(polarity) + ',' + str(subjectivity) + ',' + str(classification) + ',' + str(positive) + ',' + str(negative) + '\n')
        print(message_index)
        fd.close()

if __name__ == '__main__':
    compute_sentiments(input_data="Data/agr_en_dev.csv", output_data="Outputs/sentiments_train.csv")
