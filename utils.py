import pandas as pd
import random
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



DF = pd.read_csv('scores.csv',index_col=0)
class score_dict:
    def __init__(self,DF=DF):

        self.sorted_words = list(DF['letter'])
        self.DF = DF.sort_values('freq').reset_index()
        self.easy_words = list(self.DF.iloc[2*len(self.DF)//3:]['letter'])
        self.medium_words = list(self.DF.iloc[len(self.DF)//3:2*len(self.DF)//3]['letter'])
        self.hard_words = list(self.DF.iloc[:len(self.DF)//3]['letter'])
    
    def get_score(self,word):
        assert word in self.sorted_words, "Word is not in Wordle dictionary"
        row = self.DF.loc[self.DF['letter']==word]
        return list(row['score'])[-1]
    
    def get_freq(self,word):
        assert word in self.sorted_words, "Word is not in Wordle dictionary"
        row = self.DF.loc[self.DF['letter']==word]
        return list(row['freq'])[-1]
    
    def get_difficulty(self,difficulty='random'):
        self.DF.sort_values('freq')
        if difficulty =='random':
            return random.choice(self.sorted_words)
        elif difficulty == 'easy':
            return random.choice(self.easy_words)
        elif difficulty == 'medium':
            return random.choice(self.medium_words)
        elif difficulty == 'hard':
            return random.choice(self.hard_words)
        else:
            raise ValueError("invalid difficulty param")
    

        
