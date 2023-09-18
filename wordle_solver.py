from utils import cp_words,score_dict

sorted_words = score_dict().sorted_words

answer = input("Wordle answer:\t")

word = sorted_words[0]

filtered_sorted_words = sorted_words
while word != answer:
    print(word)
    print(cp_words(word,answer))
    hints = cp_words(word,answer)
    new_filter = []
    for sw in filtered_sorted_words:
        conds = True
        for i in range(5):
            if hints[i] == '🟩':
                conds = conds and sw[i] == word[i]
            elif hints[i] == '🟨':
                conds = conds and word[i] in sw and sw[i] != word[i]
            elif hints[i] not in hints[:i]:
                conds = conds and word[i] not in sw
        if conds:
            new_filter.append(sw)
    
    filtered_sorted_words = new_filter
    word = filtered_sorted_words[0]

print(word+'\n'+cp_words(word,answer))