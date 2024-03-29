def read(file):
    dex = dict()
    text = open(file, "r", encoding="UTF-8").read()
    data = text.split("facebook_corpus_msr_")
    data = [(txt.split(",", 1)[1].strip().rsplit(",", 1)[0].replace("\"", ""), txt.split(",", 1)[1].strip().rsplit(",", 1)[1]) for txt in data if txt != ""]
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


def get_upper_lower_score(sentence):
    total = 0
    upper = 0
    for char in sentence:
        if char.isalpha():
            total += 1
            if char.isupper(): upper += 1
    if total != 0: return upper / total
    return 0


def compute_upper_lower(input_data, output_data):
    data_msg, dex = read(file=input_data)
    data_msg = [data[0] for data in data_msg]
    fd = open(output_data, "w+")
    for message_index in range(0, len(data_msg)):
        score = get_upper_lower_score(data_msg[message_index])
        fd.write(str(message_index) + ',' + str(score) + '\n')


if __name__ == '__main__':
    compute_upper_lower(input_data="Data/agr_en_dev.csv", output_data="Outputs/upper_lower_train.csv")
