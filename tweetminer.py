from selenium import webdriver
from bs4 import BeautifulSoup
import datetime
import time
import csv
import json
import re


class TweetMiner:
    curTime = datetime.datetime.now()
    today = curTime.strftime("%Y-%m-%d")
    defaultTimeFrom = (curTime-datetime.timedelta(days=10)
                       ).strftime("%Y-%m-%d")

    def __init__(self, webdriverPath):
        self.driver = webdriver.Chrome(
            webdriverPath)  # initialize webdriver to allow Selenium access to browser for automation

    # Function to remove trailing and leading whitespaces, newline characters, and multiple continuous spaces

    def cleanText(self, txtToClean):
        # Strip links
        txtToClean = re.sub(
            r"[-a-zA-Z0-9@:%_\+.~#?&//=]{2,256}\.[a-z]{2,4}\b(\/[-a-zA-Z0-9@:%_\+.~#?&//=]*)?", "", txtToClean)
        txtToClean = re.sub(
            r'^https?:\/\/.*[\r\n]*', '', txtToClean, flags=re.MULTILINE)
        # Remove hashtags and mentions
        txtToClean = re.sub(r"\s([#@][\w_-]+)", "", txtToClean)
        # Remove hashtags and mentions from beginning
        txtToClean = re.sub("#", "", txtToClean)
        txtToClean = re.sub("@", "", txtToClean)
        # Remove trailing and leading whitespaces
        txtToClean.strip()
        # Remove all punctuation
        txtToClean = re.sub(r'[^\w\s]', "", txtToClean)
        # Remove all digits
        txtToClean = re.sub(r"\d+", "", txtToClean)
        # Remove all extra spaces, tabs and newlines
        txtToClean = " ".join(txtToClean.split())

        return txtToClean

    # Function to write to JSON file
    def writeToFile(self, listToWrite):
        with open('tweets.json', 'w') as f:
            json.dump(listToWrite, f)
        f.close()

    # Function to search posts, scrape information and create JSON object
    def searchPosts(self, keyword, hashtag=True, timeFrom=defaultTimeFrom, timeTo=today, scrollNum=20):
        tweetData = []
        prefix = ""

        # Prefix keyword with a hashtag in the url if required
        if hashtag:
            prefix = "%23"  # ASCII for hashtag

        self.driver.get(
            "https://twitter.com/search?l=&q=" + prefix + keyword + "%20since%3A"+timeFrom+"%20until%3A"+timeTo+"&src=typd")

        # Scroll the webbrowser to the end to load more tweets
        scroll = "window.scrollTo(0,document.body.scrollHeight)"

        # Number of times to scroll
        for i in range(scrollNum):
            self.driver.execute_script(scroll)
            # Wait a few seconds after each scroll to allow enough time to load the new tweets
            time.sleep(3)

        page = BeautifulSoup(self.driver.page_source,
                             'html.parser')

        self.driver.quit()

        tweets = page.find_all("div", class_="tweet")

        for tweet in tweets:
            tweetText = tweet.find(
                "p", class_="TweetTextSize").get_text().lower()

            tweetText = self.cleanText(tweetText)

            tweetTime = tweet.find(
                "span", class_="_timestamp").get('data-time')

            tweetContent = {
                "tweet": tweetText, "timestamp": tweetTime}
            tweetData.append(tweetContent)

        print(len(tweetData))
        self.writeToFile(tweetData)


# Sample object:
#
# tweetminer = TweetMiner("path/to/your/webdriver")
# tweetminer.searchPosts("london", true, "2017-01-01", "2019-01-01", 1000000)
#
#
tweetminer = TweetMiner("/Users/ajmalaboobacker/dev/twitter-bot/chromedriver")
tweetminer.searchPosts("trump", True, "2017-01-01", "2019-01-01", 1)
