import pandas as pd
import random

def cp_words(word, answer):
    """
    Compare the guessed word to the answer and provide hints based on matching characters.

    Args:
        word (str): The guessed word.
        answer (str): The correct word.

    Returns:
        str: A hint string containing symbols 🟩 (for correct letters in the correct position),
             🟨 (for correct letters in the wrong position), or ⬜ (for incorrect letters).
    """
    assert len(word) == len(answer) == 5, """mismatched word length, attempted word {} with length {}, 
                                            answer {} with length {}, should be both 5""".format(word, len(word), answer, len(answer))
    hint = ["⬜"] * 5
    word = list(word)
    answer = list(answer)
    for i in range(5):
        if word[i] == answer[i]:
            hint[i] = '🟩'
            word[i], answer[i] = '_', '_'
    for i in range(5):
        char = word[i]
        if char != '_':
            for j in range(5):
                if answer[j] == char:
                    hint[i] = '🟨'
                    answer[j] = '_'
    return ''.join(hint)


DF = pd.read_csv('scores.csv', index_col=0)

class score_dict:
    """
    Class to handle word data from a DataFrame, including word scores, frequencies, and difficulties.

    Attributes:
        DF (DataFrame): DataFrame sorted by word frequency.
        sorted_words (list): List of words classified as 'La', sorted by frequency.
        vocab (int): Number of words in sorted_words.
        easy_words (list): Bottom third of sorted_words.
        medium_words (list): Middle third of sorted_words.
        hard_words (list): Top third of sorted_words.
        all_words (list): List of all words sorted by score in descending order.
        alt_DF (DataFrame): DataFrame sorted by 'alt_score'.
        alt_all_words (list): List of all words sorted by 'alt_score' in ascending order.
    """
    def __init__(self, DF=DF):
        self.DF = DF.sort_values('freq').reset_index()
        self.sorted_words = list(self.DF.loc[self.DF['class'] == 'La']['word'])
        self.vocab = len(self.sorted_words)
        self.easy_words = self.sorted_words[self.vocab // 3 * 2:]
        self.medium_words = self.sorted_words[self.vocab // 3:self.vocab // 3 * 2]
        self.hard_words = self.sorted_words[:self.vocab // 3]
        self.DF = DF.sort_values(['score'], ascending=[False]).reset_index()
        self.all_words = list(self.DF['word'])
        self.alt_DF = DF.sort_values(['alt_score'], ascending=[True])
        self.alt_all_words = list(self.alt_DF['word'])

    def get_score(self, word):
        """
        Retrieve the score of a word.

        Args:
            word (str): The word whose score is to be fetched.

        Returns:
            float: Score of the word.
        """
        assert word in self.all_words, "Word is not in Wordle dictionary"
        row = self.DF.loc[self.DF['word'] == word]
        return list(row['score'])[-1]

    def get_freq(self, word):
        """
        Retrieve the frequency of a word.

        Args:
            word (str): The word whose frequency is to be fetched.

        Returns:
            int: Frequency of the word.
        """
        assert word in self.all_words, "Word is not in Wordle dictionary"
        row = self.DF.loc[self.DF['word'] == word]
        return list(row['freq'])[-1]

    def get_difficulty(self, difficulty='random'):
        """
        Retrieve a word based on the specified difficulty.

        Args:
            difficulty (str, optional): Difficulty level (choices: 'random', 'easy', 'medium', 'hard'). Defaults to 'random'.

        Returns:
            str: A word of the specified difficulty.
        """
        self.DF.sort_values('freq')
        if difficulty == 'random':
            return random.choice(self.sorted_words)
        elif difficulty == 'easy':
            return random.choice(self.easy_words)
        elif difficulty == 'medium':
            return random.choice(self.medium_words)
        elif difficulty == 'hard':
            return random.choice(self.hard_words)
        else:
            raise ValueError("invalid difficulty param")
