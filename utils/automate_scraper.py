import schedule
import time
from tweet_scraper import tweet_scraper
airlines = [ 'Fly Nas', 'Fly Adeal', 'Fly Dubai', 'Air Arabia', 'Ajazerah Airways' ]
#automate the task each 10 hours
for airline in airlines:
    schedule.every(10).hours.do(lambda _: tweet_scraper(airline))

while True:
    schedule.run_pending()
    time.sleep(60) # wait one minute
