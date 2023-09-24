from utils import cp_words, score_dict
from wordle_core import rank_words, filter_words_unsorted, get_score_using_cross_entropy


# # Global setting for debug mode
# DEBUG_MODE = False
#
# def verbose_decorator(func):
#     """run the function """
#     def wrapper(*args, **kwargs):
#         debug = kwargs.pop("verbose", DEBUG_MODE)  # Use the global setting as the default
#         if debug:
#             result = func(*args, **kwargs)
#             return result
#         return lambda x:x
#     return wrapper
# print = verbose_decorator(print)

def main_solve(answer, alg, rubric, verbose=True): #silence output for multiprocessing
    sd = score_dict()
    all_words = sd.all_words
    alt_all_words = sd.alt_all_words
    sorted_words = sd.sorted_words

    guess = alt_all_words[0] if alg != 'score' else all_words[
        0]  # TODO:optimize the fist guess as the one with biggest xent.

    filtered_sorted_words = all_words
    step_cnt = 0
    while guess != answer:
        step_cnt += 1

        if verbose:
            print(f" step: {step_cnt}")
            print(guess)
            print(cp_words(guess, answer))

        hints = cp_words(guess, answer)
        if (rubric == "xent"):
            filtered_sorted_words = filter_words_unsorted(filtered_sorted_words,
                                                                 hints,
                                                                 guess)
            guess = max(filtered_sorted_words, key=lambda w: get_score_using_cross_entropy(w, filtered_sorted_words))

        else:
            filtered_sorted_words = rank_words(filtered_sorted_words,
                                               hints,
                                               guess,
                                               alg=alg, rubric=rubric)
            guess = filtered_sorted_words[0]
    step_cnt += 1
    if verbose:
        print(guess + '\n' + cp_words(guess, answer))
        print(f"total step: {step_cnt}")
    return step_cnt


if __name__ == '__main__':
    answer = input("Wordle answer:\t")
    alg = input("Use alt_score? Y/n\t")
    if alg == 'n':
        alg = 'score'
    else:
        alg = 'alt_score'
    step_xent = main_solve(answer, alg, rubric="xent")
    step_stdev = main_solve(answer, alg, rubric="stdev")
    print(f"using xent has step:{step_xent}, using stdev has step:{step_stdev}")
