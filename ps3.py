# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : <your name>
# Collaborators : <your collaborators>
# Time spent    : <total time>

import math
import random
import string
import collections

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10, '*':0
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
	

# (end of helper code)
# -----------------------------------

#
# Problem #1: Scoring a word
#
def get_word_score(word, n):
    
    w = word.lower()
    score = 0
    s = 7*len(word) - 3*(n - len(word))
    for characters in w:
        score += SCRABBLE_LETTER_VALUES[characters]
    if s <= 1:
        s = 1
    return score*s
    

#
# Make sure you understand how this function works and what it does!
#
def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    
    for letter in hand.keys():
        for j in range(hand[letter]):
             print(letter, end=' ')      # print all on the same line
    print()                              # print an empty line

#
# Make sure you understand how this function works and what it does!
# You will need to modify this for Problem #4.
#
def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    
    hand={'*':1}
    num_vowels = int(math.ceil(n / 3))

    for i in range(num_vowels - 1):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1
    
    for i in range(num_vowels, n):    
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1
    
    return hand


def update_hand(hand, word):
    
    new_hand = hand.copy()
    w = word.lower()
    frequencies = collections.Counter(w)
    repeat = {}
    for key, value in frequencies.items():
        if value >= 1:
            repeat[key] = value
    for item in hand:
        if item in repeat:
            new_hand[item] = hand[item] - repeat[item]
        if new_hand[item] < 0:
            new_hand[item] = 0
    return new_hand
            




def is_valid_word(word, hand, word_list):
    
    b = False
    w = word.lower()
    s = list(w)
    frequencies = collections.Counter(w)
    repeat = {}
    if w in word_list:
        for key, value in frequencies.items():
         if value >= 1:
            repeat[key] = value
        for item in repeat:
            if item in hand:
                if repeat[item] <= hand[item]:
                    b = True
                else:
                    return False
            else:
                return False
                
    else:
        for letters in s:
            if letters == '*':
                for l in VOWELS:
                    c = s.copy()
                    n = s.index(letters)
                    c[n] = l
                    f = "".join(c)
                    if f in word_list:
                        
                        for key, value in frequencies.items():
                            if value >= 1:
                                repeat[key] = value
                        for item in repeat:
                            if item in hand:
                                if repeat[item] <= hand[item]:
                                    b = True
                                
                                
    return b
   

#
# Problem #5: Playing a hand
#
def calculate_handlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """
    l = 0
    if hand != {}:
     for letters in hand:
        l += 1
    return l
    
    

def play_hand(hand, word_list):

    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    
    * The user may input a word.

    * When any word is entered (valid or invalid), it uses up letters
      from the hand.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing two 
      exclamation points (the string '!!') instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      returns: the total score for the hand
      
    """
    word = ""
    score = 0
    new = hand.copy()
    while calculate_handlen(new) > 0:
        display_hand(new)
        word = input("Enter word, or !! to indicate that you are finished: ")
        if word == '!!':
            print("Total score: " + str(score) + " points")
            break
        elif is_valid_word(word, new, word_list) == True:
            score += get_word_score(word, calculate_handlen(new))
            print("" + word + " earned " + str(get_word_score(word, calculate_handlen(new))) + " points. Total: "+ str(score)+ " points")
        else:
            print("That is not a valid word. Please choose another word.")
        new = update_hand(new, (word)).copy()
        if calculate_handlen(new) == 0:
         print("Ran out of letters")
         break
    return score

def substitute_hand(hand, letter):
    
    if letter in hand:
        #num = hand.index[letter]
        l = VOWELS.join(CONSONANTS)
        new = hand.copy()
        x = random.choice(l)
        new.pop(letter)
        new[x] = hand[letter]
        
    else:
        print("Letter not in hand")
    return new
    
       
    
def play_game(word_list):
    """
    Allow the user to play a series of hands

    * Asks the user to input a total number of hands

    * Accumulates the score for each hand into a total score for the 
      entire series
 
    * For each hand, before playing, ask the user if they want to substitute
      one letter for another. If the user inputs 'yes', prompt them for their
      desired letter. This can only be done once during the game. Once the
      substitue option is used, the user should not be asked if they want to
      substitute letters in the future.

    * For each hand, ask the user if they would like to replay the hand.
      If the user inputs 'yes', they will replay the hand and keep 
      the better of the two scores for that hand.  This can only be done once 
      during the game. Once the replay option is used, the user should not
      be asked if they want to replay future hands. Replaying the hand does
      not count as one of the total number of hands the user initially
      wanted to play.

            * Note: if you replay a hand, you do not get the option to substitute
                    a letter - you must play whatever hand you just had.
      
    * Returns the total score for the series of hands

    word_list: list of lowercase strings
    """
    num = int(input("Enter total number of hands: "))
    t = False
    score = 0
    
    while num > 0:
     if t == False:
        hand = deal_hand(HAND_SIZE)
        display_hand(hand)
        b = input("Would you like to substitute a letter? ").lower()
        if b == "yes":
            letter = input("Which letter would you like to replace: ").lower()
            new = substitute_hand(hand, letter)
            score += play_hand(new, word_list)
            num -= 1
        else:
            score += play_hand(hand, word_list)
            num -= 1
        if num != 0:
         c = input("Would you like to replay the hand? ").lower()
        else:
            break
        if c == "yes":
            t = True
        else:
            t = False
        
     else:
        display_hand(hand)
        
        score += play_hand(hand, word_list)
        num -= 1
        if num != 0:
         c = input("Would you like to replay the hand? ").lower()
        else:
            break
        if c == "yes":
            t = True
        else:
            t = False
     
    print("----------------")
    print("Total score over all hands: " + str(score))
    #print("play_game not implemented.") # TO DO... Remove this line when you implement this function
    


#
# Build data structures used for entire session and play game
# Do not remove the "if __name__ == '__main__':" line - this code is executed
# when the program is run directly, instead of through an import statement
#

if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
    
