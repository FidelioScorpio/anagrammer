#!/usr/local/bin/python3
import enchant
import argparse

DEBUG = False

parser = argparse.ArgumentParser(description="Enter a word to anagram")
parser.add_argument("-w --word", type=str, dest="word", help=" The word to anagram")
parser.add_argument("-l --anylen", action=argparse.BooleanOptionalAction, default=False, dest="anylen", help="Is it OK for a shorter word to be found?")
parser.add_argument("-v --verbose", action=argparse.BooleanOptionalAction, dest="verbose", default=False, help="If anylen is true, display all shorter options (-l minimum is 3 letters)")
parser.add_argument("-t --tabulate", action=argparse.BooleanOptionalAction, dest="tabulate", default=False, help="If anylen is true, displays options in a table (more intensive)")
parser.add_argument("-us --us_dict", action=argparse.BooleanOptionalAction, dest="us_dict", default=False, help="Use a US dictionary instead of GB")
args = vars(parser.parse_args())
#print(args)


word = args["word"]
anylen = args["anylen"]
verbose = args["verbose"]
tabulate = args["tabulate"]

d = enchant.Dict("en_US") if us_dict else enchant.Dict("en_GB")
posslen = 0
poss = set()
valids = set()

def choose(available, complete):
    if DEBUG:
        print("DEBUG: testing characters '{}'".format(complete))
    if (len(available) == 0):
        valid(complete)
    else:
        if anylen and len(complete) > 0: # and len(complete) > posslen:
            valid(complete)
        for i in range(len(available)):
            choose(available[0:i] + available[i+1:len(available)], complete + available[i])

def valid(w):
    global posslen
    # Check that the word is in the dictionary and not already in the valids list
    if d.check(w):
        if anylen:
            if w not in poss:
                poss.add(w)
                if len(w) > posslen:
                    posslen = len(w)
        elif w not in valids:
            print(w) # Print as we go when not anylen - get results faster
            valids.add(w)
        if DEBUG:
            print("DEBUG: word '{}' already in valids? {}".format(w, w in valids))

def print_tabulate(words):
    # Aim is to print out the words list in a pretty table
    dicty = dict()
    for w in words:
        ln = len(w)
        if ln in dicty.keys():
            dicty[ln].append(w)
        else:
            dicty[ln] = [w]
    # print(dicty) <- This is good

    max_col = posslen
    row = 0
    title_text = "-"
    text = ""
    done = False
    all_lets = set(dicty.keys())
    while not done:
        done = True
        for num_let in range(1, posslen + 1):
            if num_let not in dicty.keys():
                # This number of letters has no words at all
                continue
            if not verbose and num_let < 3:
                continue
            if len(dicty[num_let]) <= row:
                # This number of letters has no more rows to print
                text += "|  " + " "*num_let
                continue
            if row == 0:
                title_text += "-" * (num_let + 3)
            text += "| {} ".format(dicty[num_let][row])
            done = False
            if len(dicty[num_let]) == row + 1:
                if DEBUG: print("DEBUG: after word {}, removing {} num_let, all_lets is '{}'".format(dicty[num_let][row], num_let, all_lets))
                all_lets.remove(num_let)
                if len(all_lets) == 0:
                    if DEBUG: print("DEBUG: done is set true")
                    done = True
        text += "|\n"
        row += 1
    print("{0}\n{1}{0}".format(title_text, text))

def main():
    if word is None or anylen is None or verbose is None:
        parser.print_help()
        return
    else:
        print("Anagramming with word '{}' and {} words of shorter length ({}tabulated)".format(word, "accepting" if anylen else "rejecting", "" if tabulate else "not " ))

    choose(word, "");
    if posslen > 0: # Could be 'if anylen', but this ensures that there is a word in poss
        if tabulate:
            print_tabulate(poss)
        else:
            for w in poss:
                if verbose or ( len(w) == posslen or (posslen > 2 and len(w) >  2) ):
                    print(w)


if __name__ == "__main__":
    main()

