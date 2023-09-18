import time

import pandas as pd
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By

name = []
rating = []
genre = []
artist = []
year = []

# retrieve the links to each review
def getReviewLinks():
    # load/parse url
    driver = webdriver.Chrome()
    driver.get('https://pitchfork.com/reviews/albums/')

    # scroll until the end of the page to account for infinite scroll
    time.sleep(3)
    last_height = driver.execute_script('return document.body.scrollHeight')
    while True:
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(3)

        next_height = driver.execute_script('return document.body.scrollHeight')
        if next_height == last_height:
            break

        last_height = next_height

    # store links to each album review into reveiwLinks
    reviewLinks = []
    links = driver.find_elements(By.CLASS_NAME, 'review__link')
    for link in links:
        href = (link.get_attribute('href'))
        reviewLinks.append(href)

    driver.quit()
    return reviewLinks

# retrieve review data from each review link
def getReviewData():
    links = getReviewLinks()

    for link in links:
        print(link)
        doc = BeautifulSoup(requests.get(link).text, "html.parser")

        checkFind(doc, name, 'h1', 'BaseWrap-sc-gjQpdd BaseText-ewhhUZ SplitScreenContentHeaderHed-lcUSuI iUEiRd fnwdMb fTtZlw')
        checkFind(doc, artist, 'div', 'BaseWrap-sc-gjQpdd BaseText-ewhhUZ SplitScreenContentHeaderArtist-ftloCc iUEiRd jqOMmZ kRtQWW')
        checkFind(doc, rating, 'div', 'SplitScreenContentHeaderScoreBox-kpzQIE ZdQbv')
        checkFind(doc, genre, 'p', 'BaseWrap-sc-gjQpdd BaseText-ewhhUZ InfoSliceValue-tfmqg iUEiRd dcTQYO fkSlPp')
        checkFind(doc, year, 'time', 'SplitScreenContentHeaderReleaseYear-UjuHP huwRqr')


# checks for valid data before appending to array
def checkFind(doc, arr, htmlElement, htmlClass):
    data = doc.find(htmlElement, htmlClass)
    if data is not None:
        if htmlClass == 'BaseWrap-sc-gjQpdd BaseText-ewhhUZ SplitScreenContentHeaderHed-lcUSuI iUEiRd fnwdMb fTtZlw' or htmlClass == 'SplitScreenContentHeaderReleaseYear-UjuHP huwRqr':
            arr.append(data.text)

        if htmlClass == 'BaseWrap-sc-gjQpdd BaseText-ewhhUZ SplitScreenContentHeaderArtist-ftloCc iUEiRd jqOMmZ kRtQWW' or htmlClass == 'BaseWrap-sc-gjQpdd BaseText-ewhhUZ InfoSliceValue-tfmqg iUEiRd dcTQYO fkSlPp':
            arr.append(data.string)

        if (htmlClass == 'SplitScreenContentHeaderScoreBox-kpzQIE ZdQbv'):
            arr.append(data.text[:3])

    else:
        arr.append('N/A')

# format data as a pandas DataFrame and export it
def exportData():
    getReviewData()
    albumTable = {'name': name, 'artist': artist, 'rating': rating, 'genre': genre, 'year' : year}
    abumDf = pd.DataFrame(albumTable)
    abumDf.to_csv("/Users/alexlong/IdeaProjects/Pitchfork_Quiz/AlbumData.csv")

exportData()
