word_list = set()
file = open("raw_word_list.txt", "r")
for line in file:
    word = line[1:6]
    word_list.add(word)
    # print(word)
file.close()
word_list = list(word_list)
# print(len(word_list))
word_list.sort()
for word in word_list:
    print(word)   