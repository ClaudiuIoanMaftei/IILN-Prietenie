from tokens_and_lemmas_module import read

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

def compute_punctuation():
    data_msg, dex = read(file="Data/agr_en_train.csv")
    data_msg = [data[0] for data in data_msg]
    fd = open("Outputs/punctuations.csv", "w+")
    for message_index in range(0, len(data_msg)):
        score = get_punctuation_score(data_msg[message_index])
        fd.write(str(message_index) + ',' +str(score) +  '\n')

if __name__ == '__main__':
    compute_punctuation()
