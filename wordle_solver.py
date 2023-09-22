from utils import cp_words,score_dict
from wordle_core import rank_words
all_words = score_dict().all_words
sorted_words = score_dict().sorted_words

answer = input("Wordle answer:\t")

guess = all_words[0]

filtered_sorted_words = all_words
while guess != answer:
    print(guess)
    print(cp_words(guess,answer))
    hints = cp_words(guess,answer)
    filtered_sorted_words = rank_words(filtered_sorted_words,
                                       hints,
                                       guess)
    guess = filtered_sorted_words[0]

print(guess+'\n'+cp_words(guess,answer))