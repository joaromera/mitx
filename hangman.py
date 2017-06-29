# Implementacion de un juego de ahorcado segun la especificacion del curso MITx: 6.00.1x Introduction to Computer Science
# and Programming Using Python, en EDX.

import random
import string

WORDLIST_FILENAME = "hangmanWords.txt"

def loadWords():
    """
    Returns a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print "Loading word list from file..."
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r', 0)
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = string.split(line)
    print "  ", len(wordlist), "words loaded."
    return wordlist

def chooseWord(wordlist):
    """
    wordlist (list): list of words (strings)

    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = loadWords()

def isWordGuessed(secretWord, lettersGuessed):
    '''
    secretWord: string, the word the user is guessing
    lettersGuessed: list, what letters have been guessed so far
    returns: boolean, True if all the letters of secretWord are in lettersGuessed;
      False otherwise
    '''
    for i in range(len(secretWord)):
        if not (secretWord[i] in lettersGuessed):
            return False
            break
    return True



def getGuessedWord(secretWord, lettersGuessed):
    '''
    secretWord: string, the word the user is guessing
    lettersGuessed: list, what letters have been guessed so far
    returns: string, comprised of letters and underscores that represents
      what letters in secretWord have been guessed so far.
    '''
    progress = ''
    for i in range(len(secretWord)):
        if secretWord[i] in lettersGuessed:
            progress = progress + ' ' + secretWord[i] + ' '
        else:
            progress = progress + ' _ '
    return progress


def getAvailableLetters(lettersGuessed):
    '''
    lettersGuessed: list, what letters have been guessed so far
    returns: string, comprised of letters that represents what letters have not
      yet been guessed.
    '''
    import string
    available = ''
    for i in string.ascii_lowercase:
        if not (i in lettersGuessed):
            available = available + i
    return available

def hangman(secretWord):
    '''
    secretWord: string, the secret word to guess.

    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many
      letters the secretWord contains.

    * Ask the user to supply one guess (i.e. letter) per round.

    * The user should receive feedback immediately after each guess
      about whether their guess appears in the computers word.

    * After each round, you should also display to the user the
      partially guessed word so far, as well as letters that the
      user has not yet guessed.

    Follows the other limitations detailed in the problem write-up.
    '''
    print("Welcome to the game, Hangman!")
    print("I am thinking of a word that is " + str(len(secretWord)) + " letters long.")
    print("-------------")
    lettersGuessed = ''
    doubleCheck = ''
    for i in range(8):
        if isWordGuessed(secretWord, lettersGuessed):
            print("Good guess: " + str(getGuessedWord(secretWord, lettersGuessed)))
            print("-------------")
            print("Congratulations, you won!")
            break
        else:
            print("You have " + str(8 - i) + " guesses left.")
            print("Available letters: " + str(getAvailableLetters(lettersGuessed)))
            print("Please guess a letter: "),
            guess = raw_input()
            guessLower = guess.lower()
            lettersGuessed = lettersGuessed + guessLower
            while not isWordGuessed(secretWord, lettersGuessed):
                if guessLower in secretWord and not guessLower in doubleCheck:
                    doubleCheck = doubleCheck + guessLower
                    print("Good guess: " + str(getGuessedWord(secretWord, lettersGuessed)))
                    print("-------------")
                    print("You have " + str(8 - i) + " guesses left.")
                    print("Available letters: " + str(getAvailableLetters(lettersGuessed)))
                    print("Please guess a letter: "),
                    guess = raw_input()
                    guessLower = guess.lower()
                    lettersGuessed = lettersGuessed + guessLower
                elif guessLower in secretWord and guessLower in doubleCheck:
                    doubleCheck = doubleCheck + guessLower
                    print("Oops! You've already guessed that letter: " + str(getGuessedWord(secretWord, lettersGuessed)))
                    print("-------------")
                    print("You have " + str(8 - i) + " guesses left.")
                    print("Available letters: " + str(getAvailableLetters(lettersGuessed)))
                    print("Please guess a letter: "),
                    guess = raw_input()
                    guessLower = guess.lower()
                    lettersGuessed = lettersGuessed + guessLower
                elif not guessLower in secretWord and guessLower in doubleCheck:
                    doubleCheck = doubleCheck + guessLower
                    print("Oops! You've already guessed that letter: " + str(getGuessedWord(secretWord, lettersGuessed)))
                    print("-------------")
                    print("You have " + str(8 - i) + " guesses left.")
                    print("Available letters: " + str(getAvailableLetters(lettersGuessed)))
                    print("Please guess a letter: "),
                    guess = raw_input()
                    guessLower = guess.lower()
                    lettersGuessed = lettersGuessed + guessLower
                else:
                    doubleCheck = doubleCheck + guessLower
                    print("Oops! That letter is not in my word: " + str(getGuessedWord(secretWord, lettersGuessed)))
                    print("-------------")
                    break
    if not isWordGuessed(secretWord, lettersGuessed):
        print("Sorry, you ran out of guesses. The word was else.")

secretWord = chooseWord(wordlist).lower()
hangman(secretWord)
