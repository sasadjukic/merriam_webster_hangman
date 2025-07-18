# Merriam-Webster Hangman

A classic command-line hangman game with a twist! This project scrapes the official Merriam-Webster "Word of the Day" to use as the puzzle for the game.

## Features

- **Dynamic Puzzles:** Fetches a new word from Merriam-Webster's "Word of the Day" page each day.
- **Interactive Gameplay:** A clean, user-friendly command-line interface for playing the game.
- **Robust Error Handling:** Gracefully handles potential network or website parsing issues.
- **Well-Tested:** Includes a comprehensive test suite with high code coverage.

## Technology Stack

- **Python 3**
- **Libraries:**
  - `requests` for making HTTP requests to the Merriam-Webster website.
  - `BeautifulSoup4` for web scraping and parsing HTML.
  - `coverage` for test coverage analysis.

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/merriam_webster_hangman.git
    cd merriam_webster_hangman
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

To start the game, simply run the `mw_hangman.py` script:

```bash
python3 mw_hangman.py
```

The game will fetch the Word of the Day and the hangman puzzle will begin.

## Running Tests

This project uses Python's built-in `unittest` framework. To run the tests and see a coverage report, execute the following command from the project root:

```bash
coverage run -m unittest test_mw_hangman.py && coverage report -m
```