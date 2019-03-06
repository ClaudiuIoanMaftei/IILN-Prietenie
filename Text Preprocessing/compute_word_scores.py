# CODE FOR CREATING LEMMATIZATION FILE
import sys
sys.path.insert(0, '../Initial/')
from todo import read
data, dex = read("../Data/agr_en_dev.csv")

fd = open("Outputs/lemmatization.txt", "w", encoding="UTF-8")

for word in dex:
    fd.write("{}    {}\n".format(word, word))
