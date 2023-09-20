from utils import cp_words,score_dict

all_words = score_dict().all_words
sorted_words = score_dict().sorted_words

answer = input("Wordle answer:\t")

guess = all_words[0]

filtered_sorted_words = all_words
while guess != answer:
    print(guess)
    print(cp_words(guess,answer))
    hints = cp_words(guess,answer)
    new_filter = []
    for sw in filtered_sorted_words:
        conds = True
        for i in range(5):
            if hints[i] == '🟩':
                conds = conds and sw[i] == guess[i]
            elif hints[i] == '🟨':
                conds = conds and guess[i] in sw and sw[i] != guess[i]
            elif guess[i] not in guess[:i]:
                conds = conds and guess[i] not in sw
        if conds:
            new_filter.append(sw)
    
    filtered_sorted_words = new_filter
    guess = filtered_sorted_words[0]

print(guess+'\n'+cp_words(guess,answer))