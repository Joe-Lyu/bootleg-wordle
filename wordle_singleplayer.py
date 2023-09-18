import random
from wordle_core import main
from utils import score_dict
sd = score_dict()
words = sd.sorted_words
answer = random.choice(words)
main(answer)