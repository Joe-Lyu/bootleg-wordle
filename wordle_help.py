from utils import score_dict
from wordle_core import rank_words
sorted_words = score_dict().sorted_words

def convert_input_to_hint():
    hint = input("Wordle colors:\t").upper()
    while not len(hint) == 5 and set(hint).issubset(set(('G','Y','?'))): 
        print("Wrong format, please re-enter")
        hint = input("Wordle colors:\t").upper()
    hint = hint.replace('G','🟩')
    hint = hint.replace('Y','🟨')
    hint = hint.replace('?','⬜')
    return hint

def input_guess():
    guess = input("Your choice:\t")
    while guess not in sorted_words:
        print("Wrong format, please re-enter")
        guess = input("Your choice:\t")
    return guess


print('Best guesses:\t', sorted_words[:5])
guess = input_guess()
hint = convert_input_to_hint()
filtered_sorted_words = sorted_words
while hint != '🟩'*5:
    filtered_sorted_words = rank_words(filtered_sorted_words,
                                       hint,
                                       guess)
    if len(filtered_sorted_words) == 1:
        print("Only possible answer is: \t"+filtered_sorted_words[0])
        break
    print('Best guesses:\t', filtered_sorted_words[:5])
    guess = input_guess()
    hint = convert_input_to_hint()

