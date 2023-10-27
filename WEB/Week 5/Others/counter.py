mylist = ['angel', 'stock', ]
word1 = 'marsh'
word2 = 'range'


def count_words_at_url(word):
    counter = 0
    for i in range(len(word)):
        for im in mylist:
            if word[i] in im:
                counter += 1
    return counter

print(count_words_at_url(word1))
print(count_words_at_url(word3))
