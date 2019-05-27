def read_data(file):
    dex = dict()
    data = list()
    with open(file, "r") as fd:
        for line in fd:
            splitted_line = line.strip().split(',')
            # id = splitted_line[0]
            tag = splitted_line[-1]
            message = ""
            for sequence in range(1, len(splitted_line) - 1):
                message += splitted_line[sequence] + ","
            message = message[:-1]
            data.append((message, tag))
    punct_mark = ".,!@#$%^&*()[]{}?/:;-\n\""
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


def read_word_scores(file_name):
    file = open(file_name, 'r', encoding="UTF-8")
    word_scores = dict()
    line = file.readline().strip()
    while line:
        word, score_NAG, score_CAG, score_OAG = line.split(',')[0], float(line.split(',')[1]), float(
            line.split(',')[2]), float(line.split(',')[3])
        word_scores[word] = [score_NAG, score_CAG, score_OAG]
        line = file.readline().strip()
    file.close()
    return word_scores


def read_lemmas(file_name):
    file = open(file_name, 'r', encoding="UTF-8")
    lemmas = dict()
    line = file.readline().strip()
    while line:
        lemmas[line.split(',')[0]] = line.split(',')[1]
        line = file.readline().strip()
    file.close()
    return lemmas


def read_punctuations(file_name):
    file = open(file_name, 'r', encoding="UTF-8")
    pairs = dict()
    line = file.readline().strip()
    while line:
        pairs[int(line.split(',')[0])] = float(line.split(',')[1])
        line = file.readline().strip()
    file.close()
    return pairs


def read_upper_lower(file_name):
    file = open(file_name, 'r', encoding="UTF-8")
    pairs = dict()
    line = file.readline().strip()
    while line:
        pairs[int(line.split(',')[0])] = float(line.split(',')[1])
        line = file.readline().strip()
    file.close()
    return pairs


def read_sentiments(file_name):
    file = open(file_name, 'r', encoding="UTF-8")
    sentiments = dict()
    line = file.readline().strip()
    while line:
        index, polarity, subjectivity, classification, positive, negative = int(line.split(',')[0]), float(
            line.split(',')[1]), float(line.split(',')[2]), \
                                                                            line.split(',')[3], float(
            line.split(',')[4]), float(line.split(',')[5])
        sentiments[index] = [polarity, subjectivity, classification, positive, negative]
        line = file.readline().strip()
    file.close()
    return sentiments


def read_sentence_scores(file_name):
    file = open(file_name, 'r', encoding="UTF-8")
    sentence_scores = dict()
    line = file.readline().strip()
    while line:
        index, score_NAG, score_CAG, score_OAG = int(line.split(',')[0]), float(line.split(',')[1]), float(
            line.split(',')[2]), float(line.split(',')[3])
        sentence_scores[index] = [score_NAG, score_CAG, score_OAG]
        line = file.readline().strip()
    file.close()
    return sentence_scores


if __name__ == '__main__':
    a, b = read_data("../test/input.txt")
    print(a)
    print(b)
