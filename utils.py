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

        self.DF = DF.sort_values('freq').reset_index()
        self.sorted_words = list(self.DF.loc[self.DF['class']=='La']['word'])
        self.vocab = len(self.sorted_words)
        self.easy_words = self.sorted_words[self.vocab//3*2:]
        self.medium_words = self.sorted_words[self.vocab//3:self.vocab//3*2]
        self.hard_words = self.sorted_words[:self.vocab//3]
        self.DF = DF.sort_values(['alt_score']).reset_index()
        self.all_words = list(self.DF['word'])

    
    def get_score(self,word):
        assert word in self.all_words, "Word is not in Wordle dictionary"
        row = self.DF.loc[self.DF['word']==word]
        return list(row['score'])[-1]
    
    def get_freq(self,word):
        assert word in self.all_words, "Word is not in Wordle dictionary"
        row = self.DF.loc[self.DF['word']==word]
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
    

        
