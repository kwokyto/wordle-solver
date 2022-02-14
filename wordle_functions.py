word_list = []
file = open("word_list/word_list.txt", "r")
for line in file:
    word_list.append(line[:5])
file.close()

def valid_indices(indices, length):
    indices_list = set()
    for string in indices.split():
        if not string.isnumeric() and string != "-1":
            return False
        indices_list.add(int(string))

    indices_list = list(indices_list)
    if len(indices_list) <= 0:
        return False

    indices_list.sort()
    if indices_list[-1] >= length:
        return False
    if indices_list[0] < -1:
        return False
    return True

def get_indices(possible_words):
    print("\nThere are 20 or less remaining possibilities, are there any words in the list that you know are definitely wrong?")
    count = 0
    print(possible_words)
    for word in possible_words:
        print("[", count, "] ", word, sep="")
        count += 1
    indices = input("Enter all indices of words that are clearly wrong. (e.g 0 4 8 10) If there are none, enter -1.\n")
    while not valid_indices(indices, len(possible_words)):
        print("\nThis is not a valid input.")
        indices = input("Enter all indices of words that are clearly wrong. (e.g 0 4 8 10) If there are none, enter -1.\n")        

    indices_list = []    
    for string in indices.split():
        indices_list.append(int(string))
    indices_list.sort(reverse=True)
    if len(indices_list) == 1 and indices_list[0] == -1:
        indices_list = []
    return indices_list
    

def valid_word(word):
    if len(word) != 5:
        return False
    if word not in word_list:
        return False
    return word.isalpha()

def get_word_guessed():
    word_guessed = input("\nWhat is the word that you guessed?\n").lower()
    while (not valid_word(word_guessed)):
        print("\nThat is not a valid 5 letter word.")
        word_guessed = input("What is the word that you guessed?\n").lower()
    return word_guessed

def valid_score(score):
    if len(score) != 5:
        return False
    for x in score:
        if x not in ["y", "n", "m"]:
            return False
    return True

def get_score():
    score = input("\nEnter the score of each letter, y for yes (green), n for no (grey), m for maybe (yellow). (e.g. nymny)\n").lower()
    while (not valid_score(score)):
        print("\nThis is not a valid score.")
        score = input("Enter the score of each letter, y for yes (green), n for no (grey), m for maybe (yellow). (e.g. nymny)\n").lower()
    return score

# def get_letter_frequency(possible_words):
#     long_string = ""
#     for word in possible_words:
#         long_string += word
    
#     letter_frequency = {}
#     for char in "abcdefghijklmnopqrstuvwxyz":
#         letter_frequency[char] = long_string.count(char) / len(long_string)
    
#     return letter_frequency

def get_letter_frequency(possible_words):
    letter_frequency = {}
    for char in "abcdefghijklmnopqrstuvwxyz":
        letter_frequency[char] = 0
    
    for word in possible_words:
        for char in word:
            letter_frequency[char] += 1
    
    return letter_frequency
