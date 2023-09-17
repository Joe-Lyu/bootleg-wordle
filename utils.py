def cp_words(word,answer):
    assert len(word) == len(answer) == 5, """mismatched word length, attempted word {} with length {}, 
                                            answer {} with length {}, should be both 5""".format(word,len(word),answer,len(answer))
    hint = ""
    for i in range(5):
        if word[i] == answer[i]:
            hint += '🟩'
        elif word[i] in answer:
            hint += '🟨'
        else:
            hint += '⬜'

    return hint