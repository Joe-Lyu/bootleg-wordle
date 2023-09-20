from tqdm import tqdm
import pandas as pd
from wordfreq import word_frequency

SCORE_FRAC = 0.5 #cannot be 1

def calc_decay(v,l):
    return v*(SCORE_FRAC**l - 1)/(SCORE_FRAC-1)

with open('wordle-La.txt','r') as f:
    Lawordlist = f.read().split('\n')
with open('wordle-Ta.txt','r') as f:
    Tawordlist = f.read().split('\n')

wordlist = Lawordlist + Tawordlist

def eval_freq(word):
    letters = sorted(word)
    valuedict = {}
    L = list(letterdict.keys())
    for i in range(len(L)):
        valuedict[L[i]] = i+1
    counts = {}
    for l in letters:
        if l not in counts:
            counts[l] = 1
        else:
            counts[l] += 1
    score = 0
    for letter in counts:
        score += calc_decay(valuedict[letter],counts[letter]) 
    return score

letterdict = {}

for word in tqdm(Lawordlist):
    for letter in word:
            if letter not in letterdict:
                letterdict[letter] = 1
            else:
                letterdict[letter] += 1

letterdict = dict(sorted(letterdict.items(), key=lambda item: item[1]))
scoredict = {}
for word in tqdm(wordlist):
    scoredict[word] = eval_freq(word)

scoredict = dict(sorted(scoredict.items(), key=lambda item: item[1]))
letters = list(scoredict.keys())
scores = list(scoredict.values())
letters.reverse()
scores.reverse()

score_df = pd.DataFrame.from_dict({"word": letters,
                                   "score": scores})

score_df['freq'] = [word_frequency(word,'en') for word in letters]

classlist = []
for index,row in score_df.iterrows():
    if row['word'] in Lawordlist:
        classlist.append('La')
    else:
        classlist.append('Ta')
score_df['class'] = classlist
score_df.to_csv('scores.csv')
