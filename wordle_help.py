from utils import score_dict
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
    new_filter = []
    for sw in filtered_sorted_words:
        conds = True
        for i in range(5):
            if hint[i] == '🟩':
                conds = conds and sw[i] == guess[i]
            elif hint[i] == '🟨':
                conds = conds and guess[i] in sw and sw[i] != guess[i]
            elif guess[i] not in guess[:i]:
                conds = conds and guess[i] not in sw
        if conds:
            new_filter.append(sw)
    
    filtered_sorted_words = new_filter
    if len(filtered_sorted_words) == 1:
        print("Only possible answer is: \t"+filtered_sorted_words[0])
        break
    print('Best guesses:\t', filtered_sorted_words[:5])
    guess = input_guess()
    hint = convert_input_to_hint()

