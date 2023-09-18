from utils import cp_words,score_dict
from getpass import getpass
MAX_TRIES = 5
words = score_dict().sorted_words
answer = getpass(prompt='Wordle answer:\t')

def word_input(guesses):
    word = input("Guess {}:\t".format(guesses))
    while word not in words:
        print("That is not a recognized word. Please retry.")
        word = input("Guess {}:\t".format(guesses))
    return word

guesses = 1
word = word_input(guesses)

while word != answer and guesses <= MAX_TRIES:
    hints = cp_words(word,answer)
    print(hints)
    guesses += 1
    word = word = word_input(guesses)

if word == answer:
    print('🟩'*5)
    print("You guessed it in {} tries".format(guesses))

else:
    print("You failed! The answer is {}".format(answer))
