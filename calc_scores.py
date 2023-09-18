import matplotlib.pyplot as plt
import pandas as pd
SCORE_FRAC = 0.8 #cannot be 1

def calc_decay(v,l):
    return v*(SCORE_FRAC**l - 1)/(SCORE_FRAC-1)

with open('dict.txt','r') as f:
    wordlist = f.read().split('\n')
wordlist = ' '.join(wordlist).split(' ')
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
wordle_word_list = []
for word in wordlist:
    if len(word) == 5:
        wordle_word_list.append(word)

for word in wordle_word_list:
    for letter in word:
            if letter not in letterdict:
                letterdict[letter] = 1
            else:
                letterdict[letter] += 1

letterdict = dict(sorted(letterdict.items(), key=lambda item: item[1]))
plt.pie(letterdict.values(),labels=letterdict.keys())
#plt.show()
scoredict = {}
for word in wordle_word_list:
    scoredict[word] = eval_freq(word)

scoredict = dict(sorted(scoredict.items(), key=lambda item: item[1]))
letters = list(scoredict.keys())
scores = list(scoredict.values())
letters.reverse()
scores.reverse()
score_df = pd.DataFrame.from_dict({"letter": letters,
                                   "score": scores})

score_df.to_csv('scores.csv')
