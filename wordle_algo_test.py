import random
from multiprocessing import Pool
from tqdm import tqdm
from utils import score_dict
from wordle_solver import main_solve
import pandas as pd
import time

TEST_SIZE = 2000

#define process for every word
def test_word(wd):
    return {'test_word':wd,
            'step_xent': main_solve(wd, 'alt_score', rubric="xent", verbose=False),
            'step_stdev': main_solve(wd, 'alt_score', rubric="stdev", verbose=False)}
    


if __name__ == '__main__':
    # print(f"test_size = {TEST_SIZE}") 
    # we use the entire 2315 words as test set because i have a good cpu >:)

    # construct the testing set
    sd = score_dict()
    all_words = sd.all_words
    alt_all_words = sd.alt_all_words
    sorted_words = sd.sorted_words
    # test_words = random.sample(all_words, TEST_SIZE)
    test_words = sorted_words

    start = time.time() 
    with Pool() as p:
        test_df = p.map(test_word,test_words)
    end = time.time()

    print(f"Time elapsed: {end-start}s")
    test_df = pd.DataFrame.from_dict(test_df)

    test_df.to_csv('algo_test.csv')

    # cnt,step_xent,step_stdev=0,0,0
    # for wd in test_words:
    #     cnt+=1
    #     print(f"test# {cnt} test_word = {wd}")
    #     step_xent += main_solve(wd, 'alt_score', rubric="xent")
    #     step_stdev += main_solve(wd, 'alt_score', rubric="stdev")
    #     print(f"using xent has step:{step_xent/cnt}, using stdev has step:{step_stdev/cnt}")
    



