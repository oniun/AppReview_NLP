"""
Google Play App Review Crawler. ver1.0
1. 7 categories & top_grossing, top_free, top_paid app reviews
2. Using mongoDB as a storage
3. Developed for NLP
"""

import os
import time
import re
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import pymongo
import json

BASEURL = 'https://play.google.com/store/apps/category/'
category = ['FINANCE', 'SHOPPING', 'SPORTS', 'VIDEO_PLAYERS','MEDICAL', 'TRAVEL_AND_LOCAL', 'NEWS_AND_MAGEZINES']
ENDURL = '/collection/topselling_free'

GROSSING = 'https://play.google.com/store/apps/collection/topgrossing'
FREE = 'https://play.google.com/store/apps/collection/topselling_free'
PAID = 'https://play.google.com/store/apps/collection/topselling_paid'

target_url = list()
for item in category:
    target_url.append(BASEURL + str(item) + ENDURL)

target_url.append(GROSSING)
target_url.append(FREE)
target_url.append(PAID)

def scrape_to_db(url):

    connection = pymongo.MongoClient('mongodb://{}:{}@13.125.31.93'.format(username, password))
    db = connection.app_review
    collection = db.reviews

    # PhantomJS driver실행
    driver = webdriver.PhantomJS('PhantomJS')

    # google play page를 띄움
    driver.get(url)

    SCROLL_PAUSE_TIME = 3
    # Get Scroll Height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        #scroll down to botton
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        #wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        #calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

        page_source = driver.page_source

        soup = BeautifulSoup(page_source, 'html.parser')
        rank = soup.select('div.id-card-list.card-list.two-cards > div > div > div.details > a.title')

    try:
        for num, item in enumerate(rank):
            adders = str(item).split()[3]
            adder = re.search('/[\w/?=.]+', adders)

            add_url = adder.group()

            # app name
            name = re.search('(?<=...)[\w ]+', str(item.get_text()).strip(" "))
            get_app = name.group()

            res2 = requests.get('http://play.google.com' + str(add_url))
            soup2 = BeautifulSoup(res2.content, 'html.parser')

            users = soup2.select('div.review-info > span.author-name')
            dates = soup2.select('div.review-info > span.review-date')
            rates = soup2.select('div.review-info > div.review-info-star-rating')
            reviews = soup2.select('div > div.review-body.with-review-wrapper')

            for user, date, review, rate in zip(users, dates, reviews, rates):

                get_user = user.get_text()
                get_date = date.get_text()

                m = re.search('\d\w\w', str(rate))
                m2 = re.search('\d', m.group())

                get_rate = m2.group()
                get_review = review.get_text().strip(" ").rstrip('전체 리뷰')

                post = {
                    "app": get_app, "date": get_date, "rate": get_rate,
                    "review": get_review, "user": get_user

                }

                collection.insert_one(post)

    except:
        print("Something Wrong")

    driver.close()
    driver.quit()
    connection.close()

    return "Mission Completed"

if __name__ == "__main__":
    for num, item in enumerate(target_url):
        scrape_to_db(item)
        print('the', num, 'th crawling is compeleted.')
