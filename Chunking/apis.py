from textblob import TextBlob
import retinasdk


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


lite_client = retinasdk.LiteClient("09A7CAA0-39A1-11E9-8F72-AF685DA1B20E")
data, dex = read("../Data/agr_en_train.csv")
print(len(data))
with open("result.txt", "w") as fd:
    count = 0
    for sentence in data:
        print(count)
        # print(count)
        # print(stuff[0])
        while 1:
            try:
                fd.write(str(lite_client.getKeywords(sentence[0].encode('utf_8')))+"\n")
                break
            except Exception as e:
                print(e)
                pass
        count += 1
