from wordle_functions import (get_indices, get_letter_frequency, get_score, get_word_guessed, word_list)

WORD_LENGTH = 5

# prepare word list
possible_words = word_list.copy()

# prepare domain
inside_word = {}
confirmed_char = {}
not_inside_word = []
unknown = list(char for char in "abcdefghijklmnopqrstuvwxyz")
unknown_indexes = list(range(WORD_LENGTH))

# play game
while len(possible_words) > 1:

    # prepare letter frequency
    letter_frequency = get_letter_frequency(possible_words)

    # get useful words
    useful_words = []
    max_useful_score = 0
    for word in word_list:
        useful_score = 0

        if word in possible_words:
            useful_score += 1

        for char in unknown:
            if char in word and char not in inside_word.keys():
                useful_score += letter_frequency[char]
            if char in word and char in inside_word.keys():
                useful_score += (letter_frequency[char] / 100)
        
        if useful_score == max_useful_score:
            useful_words.append(word)
        if useful_score > max_useful_score:
            max_useful_score = useful_score
            useful_words = [word]
    
    # suggest useful words
    print("\nNumber of useful words:", len(useful_words))
    print("I suggest using a word from this list", useful_words[:10])

    # obtain word guessed by the user
    word_guessed = get_word_guessed()
    
    # obtain score of word guessed by the user
    score = get_score()
    
    # learn about word
    for i in range(5):
        char = word_guessed[i]
        if score[i] == "n":
            if char in inside_word.keys() and len(inside_word[char]) != WORD_LENGTH:
                continue
            not_inside_word.append(char)
            if char in unknown:
                unknown.remove(char)
            continue

        if char not in inside_word.keys():
            inside_word[char] = unknown_indexes.copy()
        
        if score[i] == "y":
            if char not in confirmed_char.keys():
                confirmed_char[char] = []
            confirmed_char[char].append(i)
            if char in unknown:
                unknown.remove(char)
            for char_inner in inside_word.keys():
                if i in inside_word[char_inner]:
                    inside_word[char_inner].remove(i)
            if i in unknown_indexes:
                unknown_indexes.remove(i)

        if score[i] == "m":
            if i in inside_word[char]:
                inside_word[char].remove(i)

    # for debugging
    # print(inside_word)
    # print(confirmed_char)

    # infer about char position
    check = True
    while(check):
        check = False
        for char in inside_word.keys():
            if len(inside_word[char]) != 1:
                continue
            if char in confirmed_char.keys():
                continue
            check = True

            # if there is only 1 position left
            i = inside_word[char][0]
            if char not in confirmed_char.keys():
                confirmed_char[char] = []
            confirmed_char[char].append(i)
            if char in unknown:
                unknown.remove(char)
            for char_inner in inside_word.keys():
                if i in inside_word[char_inner]:
                    inside_word[char_inner].remove(i)
            break

    # for debugging
    # print(inside_word)
    # print(confirmed_char)

    # remove wrongly guessed word from possible words
    if score != "yyyyy" and word_guessed in possible_words:
        possible_words.remove(word_guessed)

    # update possible words
    for word_i in range(len(possible_words)-1, -1, -1):
        word = possible_words[word_i]
        is_possible = True

        for char in word:
            # if wrong char is in word
            if char in not_inside_word:
                is_possible = False
                break
        
        # if char has a fixed position
        for char in confirmed_char.keys():
            for char_i in confirmed_char[char]:
                if word[char_i] != char:
                    is_possible = False
                    break
        
        # if char that is supposed to be there is not there
        for char in inside_word.keys():
            if char not in word:
                is_possible = False
                break
            for char_i in range(WORD_LENGTH):
                if word[char_i] != char:
                    continue
                if char_i in inside_word[char]:
                    continue
                if char in confirmed_char.keys() and char_i not in confirmed_char[char]:
                    is_possible = False
                    break
        
        # remove word if not possible
        if not is_possible:
            possible_words.pop(word_i)
    
    # remove bad words
    if len(possible_words) <= 20:
        to_remove_indices = get_indices(possible_words)
        for i in to_remove_indices:
            possible_words.pop(i)
    
    print("\nNumber of remaining possible words:", len(possible_words))
    if len(possible_words) <= 20:
        print(possible_words)

    # remove confirm wrong chars based on remaining words
    possible_char = set()
    for word in possible_words:
        for char in word:
            possible_char.add(char)
    for char in unknown:
        if char not in possible_char:
            unknown.remove(char)
            not_inside_word.append(char)

if len(possible_words) == 0:
    print("Did you make an error somewhere? >< Try again!")