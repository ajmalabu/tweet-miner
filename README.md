# tweet-miner

The script takes in a keyword and start and end dates to mine for tweets containing the given keyword, retrieves the tweets and the timestamp of the tweet, cleans the text (removes hashtags, mentions, links, tabs, newlines and extra spaces), and stores the tweet with it's corresponding posting time in a json file.

The function can also take a boolean parameter called "hashtag" (`true` by default) which is used to specify whether the given keyword is a hashtag or not.

## Instructions:

1. Install Google Chrome, if you don't already have it. Check "Customization" section below for instructions on setting up the script for other browsers.
2. Clone the folder and place it anywhere on your machine.
3. Add the following at the end of the file (Refer to "Sample Object" comment at the end of the file):
   - initialize object with the path to your webdriver as the parameter
   - call the "searchPosts" functions through the object with the desired parameters
4. Enter the folder via command line and activate the virtual environment via the command `source bin/activate`.
5. Run the program via command `python3 tweetminer.py`

## Customization:

1. To set up the script to work with other browsers:

   - **For Firefox:** Download the right version of geckodriver corresponding to your OS from https://github.com/mozilla/geckodriver/releases

   - **For Safari:** The driver is included by default on MacOS. Enable it by going to _Safari_ > _Preferences_ > _Advanced_ > Check _"Show Develop menu in menu bar"_. Then go to _Develop_ > _Allow Remote Automation_

   After performing any of the 2 above steps for your browser of choice, change **line 17** in **tweetminer.py** to "webdriver.Firefox(webdriverPath)" or "webdriver.Safari(webdriverPath)"

2. Default time frame to mine for tweets begins is the preceding 10 days. You can modify this time frame by passing the desired dates in the "YYYY-MM-DD" format as parameters in the "searchPosts" function call.
3. Increase/decrease the "scrollNum" parameter (default value = 20) to mine more/less tweets according to your needs. For example, I have the script running on an EC2 instance with the time frame set to the last 365 days, and the loop parameter set to 500,000.
