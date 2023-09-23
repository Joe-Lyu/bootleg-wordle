import random

from utils import score_dict
from wordle_solver import main_solve

TEST_SIZE = 2000
if __name__ == '__main__':
    print(f"test_size = {TEST_SIZE}")

    # construct the testing set
    sd = score_dict()
    all_words = sd.all_words
    alt_all_words = sd.alt_all_words
    sorted_words = sd.sorted_words
    test_words = random.sample(all_words, TEST_SIZE)


    cnt,step_xent,step_stdev=0,0,0
    for wd in test_words:
        cnt+=1
        print(f"test# {cnt} test_word = {wd}")
        step_xent += main_solve(wd, 'alt_score', rubric="xent")
        step_stdev += main_solve(wd, 'alt_score', rubric="stdev")
        print(f"using xent has step:{step_xent/cnt}, using stdev has step:{step_stdev/cnt}")


