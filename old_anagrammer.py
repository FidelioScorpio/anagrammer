#! /usr/bin/python3
import sys
if sys.version_info <= (3, 0):
    print("This has been rewritten for Python 3. It will not run in Python 2.")
    sys.exit(0)

import enchant
MINIMUM_WORD_LENGTH = 2
#d = enchant.Dict("en_GB")
d = enchant.Dict("en_US")
def main():
    global MINIMUM_WORD_LENGTH
    # GB or US
    print("GB or US dictionary?")
    string = input().upper()
    if string == "GB":
        d = enchant.Dict("en_GB")
    elif string != "US":
        print ("woops, try again later ;p")
        return 1
    maxORexact = True
    print("Enter the number of letters wanted:\n  (prepend and 'e' to get only that exact number of characters, or type 'all' to get all characters)")
    string = input()
    if string[0] == "e":
        maxORexact = False
        string = string[1:]
    try:
        letters = int(string)
    except ValueError:
        if string == "all" and maxORexact:
            letters = 0
        else:
            print ("woops, try again later ;p")
            return 1
    
    if maxORexact and letters > 0:
        print("Minimum characters in a word:")
        string = input()
        try:
            MINIMUM_WORD_LENGTH = int(string)
        except ValueError:
            print ("woops, try again later ;p")
            return 1

    print("String to pick letters from: ")
    string = input()
    if letters == 0:
        letters = len(string)
    if len(string) < letters:
        print("woops, try again later ;p")
        return
    arr = recursive_dictionary_check(string, "", letters, set(), maxORexact)
    print("\n", end="")
    print(arr)

def recursive_dictionary_check(string, chars_chosen, letters, arr, maxORexact):
    #letters is either 'maxLetters' or 'exactLetters'
    #maxORexact is a bool. True when max is wanted
    if len(chars_chosen) == 0:
        print("|" + " "*len(string) + "|\r|", end="")
    for i in range(0, len(string)):
        if len(chars_chosen) == 0:
            print(".", end="")
            sys.stdout.flush()
        new_chars_chosen = chars_chosen + string[i]
        if not maxORexact: #exact
            if len(new_chars_chosen) == letters:
                #if the string is the length we want, check the dictionary for it
                if d.check(new_chars_chosen):
                    arr.add(new_chars_chosen)
            else:
                #recursive call with:
                #'string' being string without the chosen character
                #'chars_chosen' being chars_chosen with the new character added
                arr = recursive_dictionary_check(string[:i] + string[i+1:], new_chars_chosen, letters, arr, maxORexact)
        else: #max
            if d.check(new_chars_chosen):
                arr.add(new_chars_chosen)
            if len(new_chars_chosen) < letters:
                arr = recursive_dictionary_check(string[:i] + string[i+1:], new_chars_chosen, letters, arr, maxORexact)
    return arr

def rec_max_check(remaining_chars, chars_chosen, max_letters, output_set):
    if chars_chosen and len(chars_chosen) > MINIMUM_WORD_LENGTH and d.check(chars_chosen):
        output_set.add(chars_chosen)
    if len(chars_chosen) == max_letters: #no characters remaining
        return output_set
    #otherwise, pick a char
    for i in range(0, len(remaining_chars)):
        output_set.update(rec_max_check(remaining_chars[:i] + remaining_chars[i+1:], chars_chosen + remaining_chars[i], max_letters, set()))
    return output_set

def rec_ex_check(remaining_chars, chars_chosen, exact_letters, output_set):
    if len(chars_chosen) == exact_letters:
        if d.check(chars_chosen):
            output_set.add(chars_chosen)
        return output_set
    #otherwise, pick a char
    for i in range(0, len(remaining_chars)):
        output_set.update(rec_ex_check(remaining_chars[:i] + remaining_chars[i+1:], chars_chosen + remaining_chars[i], exact_letters, set()))
    return output_set

#main
if __name__ == "__main__":
    main()

    #s = "fosjinzotkop"
    #numLetters = 7
