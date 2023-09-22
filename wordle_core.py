from utils import cp_words,score_dict
sd = score_dict()
words = sd.sorted_words
MAX_TRIES = 5

def word_input(guesses):
    word = input("Guess {}:\t".format(guesses))
    while word not in words:
        print("That is not a recognized word. Please retry.")
        word = input("Guess {}:\t".format(guesses))
    return word

def main(answer,MAX_TRIES = MAX_TRIES):
    guesses = 1
    word = word_input(guesses)

    while word != answer and guesses <= MAX_TRIES:
        hints = cp_words(word,answer)
        print(hints)
        guesses += 1
        word = word_input(guesses)

    if word == answer:
        print('🟩'*5)
        print("You guessed it in {} tries".format(guesses))

    else:
        print("You failed! The answer is {}".format(answer))

def rank_words(filtered_sorted_words,hint,guess,symbolset=True):
    if symbolset:
        symbols = ['🟩','🟨','⬜']
    else:
        symbols = ['G','Y','?']
    new_filter = []
    for sw in filtered_sorted_words:
        conds = True
        for i in range(5):
            if hint[i] == symbols[0]:
                conds = conds and sw[i] == guess[i]
            elif hint[i] == symbols[1]:
                conds = conds and guess[i] in sw and sw[i] != guess[i]
            elif guess[i] not in guess[:i] and guess[i] not in guess[i+1:]:
                conds = conds and guess[i] not in sw
            else:
                conds = conds and sw[i] != guess[i]
        if conds:
            new_filter.append(sw)
    return new_filter