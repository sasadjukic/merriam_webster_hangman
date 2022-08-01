

import hangman_graphic, requests
from bs4 import BeautifulSoup

url = 'https://www.merriam-webster.com/word-of-the-day'
respond = requests.get(url)
soup = BeautifulSoup(respond.text, 'html.parser')

find_word = soup.find('h1')
word = find_word.text
lst = []

for letter in word:
    lst.append(letter)

display_list = []

for index in range(len(lst)):
    display_list.append('_')

missed_words = []
wrong_guess = 0
game_check = True
while game_check:

    choice = input('enter a letter: ')

    if choice not in lst:
        wrong_guess += 1
        print(hangman_graphic.graphics[wrong_guess])
        missed_words.append(choice)
        print(f'The letters you already missed are: {missed_words}')
        if wrong_guess == 6:
            print('You\'ve been hanged. Better luck next time')
            print(f'The word you needed to guess was {word.upper()}')
            break


    for index in range(len(lst)):
        if choice == lst[index]:
            display_list[index] = choice

    print('\n')
    print(display_list)

    if '_' not in display_list:
        print('\n')
        print(f'Well Done. The final word is {word.upper()}. You have solved the puzzle')
        game_check = False
