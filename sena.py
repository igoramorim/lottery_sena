from bs4 import BeautifulSoup
import requests
from collections import deque
from collections import Counter


base_url = 'https://www.terra.com.br/noticias/loterias/mega-sena/?sorteio='

def get_last_game_txt():
    try:
        with open('sena.txt', 'r') as f:
            # get the last 7 lines in the txt file
            # [0] is to get the first line of the seven last lines
            # that is the number of the last game saved in the file
            # all the games saved in the file start with *
            # delete the * so we have only the number of the game
            return deque(f, 7)[0].replace('*', '')
    except:
        print('Error opening file')


def get_last_game_site():
    try:
        r = requests.get(base_url)
        soup = BeautifulSoup(r.content, 'html.parser')
        # get the number of the last game in the site
        game_number = soup.find('input', {'id': 'contest_input'})
        return game_number['value']
    except:
        print('Error opening ' + url)


def update_games(start, final):
    print('\nUpdating games...')
    while start < final:
        start += 1
        url = base_url + str(start)

        try:
            r = requests.get(url)
            soup = BeautifulSoup(r.content, 'html.parser')
            box_numbers = soup.find_all('div', {'class': 'bol_box'})

            print('Game: ' + str(start))

            with open('sena.txt', 'a') as f:
                f.write('*' + str(start) + '\n')
                for numbers in box_numbers:
                    # get the numbers of the game
                    # index: 1 3 5 7 9 11
                    for i in range(1, 12, 2):
                        f.write(numbers.contents[i].text + '\n')
        except:
            print('\nError opening url or file')
            pass

    print('File updated')


def get_all_numbers():
    numbers = []
    try:
        with open('sena.txt', 'r') as f:
            for line in f:
                # dont get the lines that start with *
                # get only the lines with numbers
                if not line[0] == '*':
                    numbers.append(int(line))
    except:
        print('Error opening file')

    return numbers


def main():
    last_game_txt = int(get_last_game_txt())
    last_game_site = int(get_last_game_site())

    if last_game_txt < last_game_site:
        update_games(last_game_txt, last_game_site)

    all_numbers = get_all_numbers()

    count = Counter(all_numbers)
    freq = count.most_common(60)
    print('Number\tTimes chosen')
    for number in freq:
         print('{}\t{}'.format(number[0], number[1]))


if __name__ == '__main__':
    main()
