import unittest
from unittest.mock import patch, MagicMock
import platform
import io
import sys
import mw_hangman

class TestGetWordOfTheDay(unittest.TestCase):

    @patch('requests.get')
    def test_get_word_of_the_day_success(self, mock_get):
        """Test successful retrieval and parsing of the word."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '<html><body><h2 class="word-header-txt">example</h2></body></html>'
        mock_get.return_value = mock_response

        word = mw_hangman.get_word_of_the_day('fake_url')
        self.assertEqual(word, 'example')
        mock_get.assert_called_once_with('fake_url', timeout=10)

    @patch('requests.get')
    def test_get_word_of_the_day_request_exception(self, mock_get):
        """Test handling of a network request exception."""
        mock_get.side_effect = mw_hangman.requests.RequestException("Test error")
        
        saved_stderr = sys.stderr
        try:
            sys.stderr = io.StringIO()
            word = mw_hangman.get_word_of_the_day('fake_url')
            self.assertIsNone(word)
            self.assertIn("Error: Could not fetch the URL", sys.stderr.getvalue())
        finally:
            sys.stderr = saved_stderr

    @patch('requests.get')
    def test_get_word_of_the_day_parsing_failure(self, mock_get):
        """Test handling of missing HTML element."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '<html><body><h1>No word here</h1></body></html>'
        mock_get.return_value = mock_response

        saved_stderr = sys.stderr
        try:
            sys.stderr = io.StringIO()
            word = mw_hangman.get_word_of_the_day('fake_url')
            self.assertIsNone(word)
            self.assertIn("Could not find the word on the page", sys.stderr.getvalue())
        finally:
            sys.stderr = saved_stderr

    @patch('requests.get')
    def test_get_word_of_the_day_unexpected_parsing_error(self, mock_get):
        """Test handling of an unexpected error during parsing."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '<html><body><h2 class="word-header-txt">word</h2></body></html>'
        mock_get.return_value = mock_response

        with patch('mw_hangman.BeautifulSoup', side_effect=Exception("Parsing failed")):
            saved_stderr = sys.stderr
            try:
                sys.stderr = io.StringIO()
                word = mw_hangman.get_word_of_the_day('fake_url')
                self.assertIsNone(word)
                self.assertIn("An error occurred during parsing", sys.stderr.getvalue())
            finally:
                sys.stderr = saved_stderr


class TestPlayGame(unittest.TestCase):

    @patch('mw_hangman.clear_screen')
    @patch('builtins.input')
    @patch('sys.stdout')
    def test_play_game_win(self, mock_stdout, mock_input, mock_clear):
        """Test a full game scenario where the user wins."""
        word = "cat"
        # Simulate user inputs: 'c', 'a', 't'
        mock_input.side_effect = ['c', 'a', 't']
        
        mw_hangman.play_game(word)
        
        # Check if the final "WELL DONE" message is printed
        output = "".join(call[0][0] for call in mock_stdout.write.call_args_list)
        self.assertIn("WELL DONE", output)

    @patch('mw_hangman.clear_screen')
    @patch('builtins.input')
    @patch('sys.stdout')
    def test_play_game_loss(self, mock_stdout, mock_input, mock_clear):
        """Test a full game scenario where the user loses."""
        word = "dog"
        # Simulate 6 wrong guesses + 1 final input to end loop
        mock_input.side_effect = ['a', 'b', 'c', 'e', 'f', 'g', 'h']
        
        mw_hangman.play_game(word)
        
        output = "".join(call[0][0] for call in mock_stdout.write.call_args_list)
        self.assertIn("YOU'VE BEEN HANGED", output)

    @patch('mw_hangman.clear_screen')
    @patch('builtins.input')
    @patch('sys.stdout')
    def test_play_game_invalid_and_repeated_input(self, mock_stdout, mock_input, mock_clear):
        """Test that invalid and repeated inputs are handled correctly."""
        word = "test"
        # Simulate invalid, repeated, and finally correct inputs
        mock_input.side_effect = ['aa', '', 't', 't', 'e', 's']
        
        mw_hangman.play_game(word)
        
        output = "".join(call[0][0] for call in mock_stdout.write.call_args_list)
        self.assertIn("Invalid input", output)
        self.assertIn("You have already guessed that letter", output)
        self.assertIn("WELL DONE", output)


class TestMainExecution(unittest.TestCase):

    @patch('mw_hangman.get_word_of_the_day', return_value='testword')
    @patch('mw_hangman.play_game')
    def test_main_success(self, mock_play_game, mock_get_word):
        """Test the main function when a word is successfully retrieved."""
        saved_stdout = sys.stdout
        try:
            sys.stdout = io.StringIO()
            mw_hangman.main()
            mock_get_word.assert_called_once_with(mw_hangman.MERRIAM_WEBSTER_WOD_URL)
            mock_play_game.assert_called_once_with('testword')
            self.assertIn("Fetching the Word of the Day...", sys.stdout.getvalue())
        finally:
            sys.stdout = saved_stdout

    @patch('mw_hangman.get_word_of_the_day', return_value=None)
    @patch('sys.exit')
    def test_main_failure(self, mock_exit, mock_get_word):
        """Test the main function when word retrieval fails."""
        saved_stderr = sys.stderr
        saved_stdout = sys.stdout
        try:
            sys.stderr = io.StringIO()
            sys.stdout = io.StringIO()
            mw_hangman.main()
            mock_get_word.assert_called_once_with(mw_hangman.MERRIAM_WEBSTER_WOD_URL)
            mock_exit.assert_called_once_with(1)
            self.assertIn("Could not start the game", sys.stderr.getvalue())
        finally:
            sys.stderr = saved_stderr
            sys.stdout = saved_stdout


class TestHelpers(unittest.TestCase):

    @patch('os.system')
    def test_clear_screen(self, mock_os_system):
        """Test that clear_screen calls the correct os command."""
        current_os = platform.system()
        expected_cmd = 'cls' if current_os == 'Windows' else 'clear'
        
        mw_hangman.clear_screen()
        mock_os_system.assert_called_once_with(expected_cmd)


if __name__ == '__main__':
    unittest.main()
