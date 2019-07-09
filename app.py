from selenium import webdriver
from bs4 import BeautifulSoup
import datetime
import time
import re
import csv
import json


class TweetScraper:
    curTime = datetime.datetime.now()
    today = curTime.strftime("%Y-%m-%d")
    defaultTimeFrom = (curTime-datetime.timedelta(days=10)
                       ).strftime("%Y-%m-%d")

    def __init__(self):
        self.driver = webdriver.Chrome(
            "/Users/ajmalaboobacker/dev/twitter-bot/chromedriver")

    # Function to strip all hashtags, mentions and links in the tweet text
    def stripLinks(self, tagToClean):
        links = tagToClean.find_all("a")
        for link in links:
            link.decompose()
        return tagToClean

    # Function to remove trailing and leading whitespaces, newline characters, and multiple continuous spaces
    def cleanText(self, txtToClean):
        # Remove trailing and leading whitespaces
        txtToClean.strip()

        # Remove all extra spaces, tabs and newlines
        txtToClean = " ".join(txtToClean.split())

        return txtToClean

    def writeToFile(self, listToWrite):
        with open('test.json', 'w') as f:
            json.dump(listToWrite, f)
        f.close()

    def searchPosts(self, keyword, hashtag=True, timeFrom=defaultTimeFrom, timeTo=today):
        tweetData = []
        prefix = ""

        # Prefix keyword with a hashtag in the url if required
        if hashtag:
            prefix = "%23"  # ASCII for hashtag

        self.driver.get(
            "https://twitter.com/search?l=&q=" + prefix + keyword + "%20since%3A"+timeFrom+"%20until%3A"+timeTo+"&src=typd")

        scroll = "window.scrollTo(0,document.body.scrollHeight)"
        for i in range(20):
            self.driver.execute_script(scroll)
            time.sleep(3)

        page = BeautifulSoup(self.driver.page_source, 'html.parser')

        self.driver.quit()

        tweets = page.find_all("div", class_="tweet")

        for tweet in tweets:
            tweetText = tweet.find("p", class_="TweetTextSize")

            tweetText = self.stripLinks(tweetText)
            tweetText = self.cleanText(tweetText.get_text())

            tweetTime = tweet.find(
                "span", class_="_timestamp").get('data-time')

            tweetContent = {
                "tweet": tweetText, "timestamp": tweetTime}
            tweetData.append(tweetContent)

        self.writeToFile(tweetData)
