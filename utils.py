import pandas as pd
#🟩🟨⬜
def cp_words(word,answer):
    assert len(word) == len(answer) == 5, """mismatched word length, attempted word {} with length {}, 
                                            answer {} with length {}, should be both 5""".format(word,len(word),answer,len(answer))
    hint = ["⬜"]*5
    word = list(word)
    answer = list(answer)
    for i in range(5):
        if word[i] == answer[i]:
            hint[i] = '🟩'
            word[i],answer[i] = '_','_'
    for i in range(5):
        char = word[i]
        if char != '_':
            for j in range(5):
                if answer[j] == char:
                    hint[i] = '🟨'
                    answer[j] = '_'
    return ''.join(hint)

            


    return hint

DF = pd.read_csv('scores.csv',index_col=0)
class score_dict:
    def __init__(self,DF=DF):
        self.DF = DF
        self.sorted_words = list(DF['letter'])
    
    def get_score(self,word):
        assert word in self.sorted_words, "Word is not in Wordle dictionary"
        row = self.DF.loc[self.DF['letter']==word]
        return list(row['score'])[-1]
        
