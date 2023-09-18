import pandas as pd
import Player
import random

def playGame():
    # read AlbumData csv file
    albumData = pd.read_csv('/Users/alexlong/IdeaProjects/Pitchfork_Quiz/AlbumData.csv')

    # User options
    print('Welcome to the Pitchfork Quiz!\n')
    print('Choose the following options:')
    print('1: Play by artist')
    print('2: Play by genre')
    print('3: Play by year')
    print('4: Play by random')
    print('5 Quit\n')

    # Prompt user for valid input
    while True:
        choice = input('Enter a choice: ')
        if choice == '1':
            gamemodeData = playArtist(albumData)
        elif choice == '2':
            gamemodeData = playGenre(albumData)
        elif choice == '3':
            gamemodeData = playYear(albumData)
        elif choice == '4':
            gamemodeData = albumData
        elif choice == '5':
            print('Thanks for playing!')
            exit()
        else:
            print('Please enter a valid choice\n')
            continue

        playQuiz(gamemodeData)

        # Prompt user for valid end game input
        print('Would you like to play again?')
        while True:
            choice = input('Yes or No?')
            if choice.capitalize() == 'Yes':
                break
            elif choice.capitalize() == 'No':
                print('Thanks for playing!')
                exit()
            else:
                print('Please select a valid choice\n')
                continue;

# filter AlbumData DataFrame by particular artist
# return modified DataFrame
def playArtist(albumData):
    while True:
        artist = input('Enter an artist: ').title()
        print('\n', end='')

        if artist not in albumData['artist'].unique():
            print('Please enter a valid artist\n')
            continue
        else:
            break

    artistData = albumData[albumData['artist']].reset_index()[['name', 'rating']]
    return artistData

# filter AlbumData DataFrame by particular genre
# return modified DataFrame
def playGenre(albumData):
    while True:
        genre = input('Enter a genre: ').capitalize()
        print('\n', end='')

        if genre not in albumData['genre'].unique():
            print('Please enter a valid genre\n')
            continue
        else:
            break

    genreData = albumData[albumData['genre'].str.contains(genre)].reset_index()[['name', 'rating']]
    return genreData

# filter AlbumData DataFrame by particular year
# return modified DataFrame
def playYear(albumData):
    while True:
        year = input('Enter a year: ')
        print('\n', end='')

        if year not in albumData['year'].unique():
            print('Please enter a valid year\n')
            continue
        else:
            break

    yearData = albumData[albumData['year']].reset_index()[['name', 'rating']]
    return yearData

# User starts w/ 0 points and 3 lives
# Game ends when they have 0 lives
def playQuiz(gamemodeData):
    player = Player.Player()

    while player.getLives() != 0:
        albumIndices = random.sample(range(0, len(gamemodeData.index) - 1), 2)

        album1 = gamemodeData.iloc[albumIndices[0]]
        album2 = gamemodeData.iloc[albumIndices[1]]

        print('Which album has the higher Pitchfork score?')

        while True:
            choice = input('0: ' + album1.iloc[0] + ' or ' + '1: ' + album2.iloc[0] + '? ')
            if choice == '0':
                choiceManager(album1, album2, player)
                break
            elif choice == '1':
                choiceManager(album2, album1, player)
                break
            else:
                print('Please enter a valid choice\n')

    print('Thanks for playing!')
    print(player.__str__())
    print('\n')

# Compares the album socres of user input
def choiceManager(yourChoice, otherChoice, player):
    if yourChoice.iloc[1] >= otherChoice.iloc[1]:
        print('\nCorrect!')
        player.increaseScore()
        print('You have ' + str(player.getScore()) + ' points!\n')
    else:
        print('\nWrong!')
        player.decreaseLife()
        print('You have ' + str(player.getLives()) + ' lives left!\n')

playGame()