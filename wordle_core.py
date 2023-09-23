from utils import cp_words, score_dict
from itertools import permutations, combinations_with_replacement
from statistics import stdev

sd = score_dict()
words = sd.sorted_words
MAX_TRIES = 5


def word_input(guesses):
    """
    Prompt the user for a word guess.

    Args:
        guesses (int): The current guess attempt number.

    Returns:
        str: The word provided by the user that exists in the predefined word list.
    """
    word = input("Guess {}:\t".format(guesses))
    while word not in words:
        print("That is not a recognized word. Please retry.")
        word = input("Guess {}:\t".format(guesses))
    return word


def main(answer, MAX_TRIES=MAX_TRIES):
    """
    Run the Wordle game, comparing the user's guesses against the provided answer.

    Args:
        answer (str): The correct word that the user needs to guess.
        MAX_TRIES (int, optional): Maximum number of tries for the user to guess the word. Defaults to 5.
    """
    guesses = 1
    word = word_input(guesses)

    while word != answer and guesses <= MAX_TRIES:
        hints = cp_words(word, answer)
        print(hints)
        guesses += 1
        word = word_input(guesses)

    if word == answer:
        print('🟩' * 5)
        print("You guessed it in {} tries".format(guesses))
    else:
        print("You failed! The answer is {}".format(answer))


def rank_words(filtered_sorted_words, hint, guess, alg='alt_score', symbolset=True, recursive=True):
    """
    filter words based on given hints(outcome) and the chosen algorithm.

    Args:
        filtered_sorted_words (list): List of words filtered based on previous guesses and hints.
        hint (list): List of symbols indicating the status of previous guesses.
        guess (str): The previous word guess associate with the hint.
        alg (str, optional): The chosen ranking algorithm. Defaults to 'alt_score'.
        symbolset (bool, optional): Flag to use emoji symbols or plain text symbols. Defaults to True.
        recursive (bool, optional): Flag to perform recursive ranking. Defaults to True.

    Returns:
        list: A filtered list of words taht still satisfy the specified criteria (hint, guess).
    """
    if symbolset:
        symbols = ['🟩', '🟨', '⬜']
    else:
        symbols = ['G', 'Y', '?']
    new_filter = []
    for sw in filtered_sorted_words:
        conds = True
        for i in range(5):
            if hint[i] == symbols[0]:
                conds = conds and sw[i] == guess[i]
            elif hint[i] == symbols[1]:
                conds = conds and guess[i] in sw and sw[i] != guess[i]
            elif guess[i] not in guess[:i] and guess[i] not in guess[i + 1:]:
                conds = conds and guess[i] not in sw
            else:
                conds = conds and sw[i] != guess[i]
        if conds:
            new_filter.append(sw)
    if recursive and alg == 'alt_score':
        new_filter.sort(key=lambda w: get_remaining(w, new_filter))
    return new_filter


def get_remaining(guess, filtered_sorted_words=words):
    """
    Score the guess based on calculation of the remaining possible words.

    Args:
        guess (str): The current word guess.
        filtered_sorted_words (list, optional): List of words filtered based on previous guesses and hints. Defaults to the full word list.

    Returns:
        float: Score indicating the number of remaining possibilities based on the guess.
    """
    all_possible_hints = []
    for p in list(combinations_with_replacement(['G', 'Y', '?'], 5)):
        all_possible_hints += list(set(permutations(p)))
    possibilities_left = []
    for hint in all_possible_hints:
        possibilities_left.append(len(rank_words(filtered_sorted_words, hint, guess, symbolset=False, recursive=False)))
    score = stdev(possibilities_left) * sum(possibilities_left) / 1000
    return score
