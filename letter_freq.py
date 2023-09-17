import matplotlib.pyplot as plt
import pickle
SCORE_FRAC = 0.5 #cannot be 1

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
sorted_words = list(scoredict.keys())

sorted_words = [sorted_words[i] for i in range(len(sorted_words)-1,-1,-1)]

with open('sorted_words.txt','w') as f:
    f.write('\n'.join(sorted_words))

