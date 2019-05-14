from reading_functions import read_data

def get_punctuation_score(sentence):
    streaks=0
    total=0
    prev_char=""
    for char in sentence:
        if char in ",.!?":
            if char==prev_char: streaks+=1
            total += 1
        prev_char=char

    if total!=0: return streaks/total
    return 0

def compute_punctuation(input_data, output_data):
    data_msg, dex = read_data(file=input_data)
    data_msg = [data[0] for data in data_msg]
    fd = open(output_data, "w")
    for message_index in range(0, len(data_msg)):
        score = get_punctuation_score(data_msg[message_index])
        fd.write(str(message_index) + ',' +str(score) +  '\n')

if __name__ == '__main__':
    compute_punctuation(input_data="Data/agr_en_dev.csv", output_data="Outputs/punctuations_train.csv")
