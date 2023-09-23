from utils import cp_words,score_dict
from wordle_core import rank_words
sd = score_dict()
all_words =sd.all_words
alt_all_words = sd.alt_all_words
sorted_words = sd.sorted_words

answer = input("Wordle answer:\t")
alg = input("Use alt_score? Y/n\t")
if alg == 'n':
    alg = 'score'
else:
    alg = 'alt_score'
guess = alt_all_words[0] if alg != 'score' else all_words[0]

filtered_sorted_words = all_words
while guess != answer:
    print(guess)
    print(cp_words(guess,answer))
    hints = cp_words(guess,answer)
    filtered_sorted_words = rank_words(filtered_sorted_words,
                                       hints,
                                       guess,
                                       alg=alg)
    guess = filtered_sorted_words[0]

print(guess+'\n'+cp_words(guess,answer))