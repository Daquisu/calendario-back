import re
import os
from consts import HASHTAG_LABELS
word_frequency = {}
words = []

for hashtag_label in HASHTAG_LABELS:
    print(hashtag_label)
    arr = os.listdir("./" + hashtag_label + "/")
    for index in range(len(arr)):
        if arr[index].endswith('.txt'):
            with open('./' + hashtag_label + '/' + arr[index]) as f:
                for line in f:
                    splitted_text = re.split('[ \(\)\[\]\{\}\\\|\$\,\.;:/?!"_*\n\t\r]', line.lower())
                    words.append(re.split(r'[`\-=~!#$%^&*()_+\[\]{};\'\\:"|<,./<>?•]', splitted_text))

for line in words:
    for word in line:
        if word != '':
            if word in word_frequency:
                word_frequency[word] += 1
            else:
                word_frequency[word] = 1

removed_words = []
for word in word_frequency:
    if word_frequency[word] < 100:
        removed_words.append(word)

for word in removed_words:
    del word_frequency[word]

for word in sorted(word_frequency, key=word_frequency.get, reverse=True):
    print (word, word_frequency[word])
