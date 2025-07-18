"""
A command-line Hangman game that fetches the "Word of the Day" from
Merriam-Webster's website.
"""
import os
import sys
import platform
import requests
from bs4 import BeautifulSoup
import hangman_graphic

# Constants
MERRIAM_WEBSTER_WOD_URL = 'https://www.merriam-webster.com/word-of-the-day'
MAX_WRONG_GUESSES = 6

def clear_screen():
    """Clears the console screen."""
    command = 'cls' if platform.system() == 'Windows' else 'clear'
    os.system(command)

def get_word_of_the_day(url: str) -> str | None:
    """
    Fetches the Word of the Day from the given Merriam-Webster URL.

    Args:
        url: The URL of the Merriam-Webster Word of the Day page.

    Returns:
        The word of the day as a string, or None if it cannot be retrieved.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes
    except requests.RequestException as e:
        print(f'Error: Could not fetch the URL: {e}', file=sys.stderr)
        return None

    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        word_element = soup.find('h2', class_='word-header-txt')
        if word_element and word_element.text:
            return word_element.text.strip().lower()
        else:
            print('Error: Could not find the word on the page. The website structure might have changed.', file=sys.stderr)
            return None
    except Exception as e:
        print(f'Error: An error occurred during parsing: {e}', file=sys.stderr)
        return None

def play_game(word: str):
    """
    Starts and manages a game of Hangman with an improved UI.

    Args:
        word: The word to be guessed.
    """
    word_letters = set(word)
    guessed_letters = set()
    missed_letters = set()
    wrong_guesses = 0
    message = ''

    while wrong_guesses < MAX_WRONG_GUESSES:
        clear_screen()

        # Display header
        print('=' * 40)
        print('      MERRIAM-WEBSTER HANGMAN')
        print('=' * 40)

        # Display game state
        print(hangman_graphic.graphics[wrong_guesses])
        
        display_word = ' '.join([letter if letter in guessed_letters else '_' for letter in word])
        print(f'Word: {display_word}\n')

        if missed_letters:
            print(f"Missed letters: {', '.join(sorted(missed_letters))}")
        
        # Check for win condition
        if '_' not in display_word:
            print('\n' + '=' * 40)
            print(f" WELL DONE! The word was '{word.upper()}'.")
            print('=' * 40)
            return

        # Display any messages from the previous turn
        if message:
            print(f'\n{message}')
            message = ''

        # Get user input
        guess = input('Enter a letter: ').lower().strip()

        # Input validation
        if len(guess) != 1 or not guess.isalpha():
            message = 'Invalid input. Please enter a single letter.'
            continue
        
        if guess in guessed_letters or guess in missed_letters:
            message = 'You have already guessed that letter. Try another one.'
            continue

        # Process the guess
        if guess in word_letters:
            guessed_letters.add(guess)
            message = f"Good guess! '{guess}' is in the word."
        else:
            missed_letters.add(guess)
            wrong_guesses += 1
            message = f"Sorry, '{guess}' is not in the word."

    # Game over (loss)
    clear_screen()
    print('=' * 40)
    print('      MERRIAM-WEBSTER HANGMAN')
    print('=' * 40)
    print(hangman_graphic.graphics[wrong_guesses])
    print('\n' + '=' * 40)
    print(' YOU HAVE BEEN HANGED! Better luck next time.')
    print(f" The word you needed to guess was '{word.upper()}'.")
    print('=' * 40)

def main():
    """
    Main function to run the Hangman game.
    """
    print('Fetching the Word of the Day...', file=sys.stdout)
    word = get_word_of_the_day(MERRIAM_WEBSTER_WOD_URL)
    if word:
        play_game(word)
    else:
        print('Could not start the game because a word could not be retrieved.', file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
