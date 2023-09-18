from getpass import getpass
from wordle_core import main
MAX_TRIES = 5

answer = getpass(prompt='Wordle answer:\t')

main(answer)