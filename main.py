# pip install schedule   !!!!
import datetime as dt
from datetime import datetime
import instaloader
import schedule
import time
import os
import json
import re
from consts import HASHTAG_LABELS

hashtag_labels = []
for hashtag_label in HASHTAG_LABELS:
    hashtag_labels.append(hashtag_label[1:])

def post_from_today(post):
    now =  datetime.now()
    today = datetime(now.year, now.month, now.day)
    return post.date_local >= today

def post_from_this_year(post):
    return post.date_local >= datetime(2019, 1, 1)

def post_from_october(post):
    return post.date_local >= datetime(2019, 10, 1)

def post_from_last_7_days(post):
    return post.date_local >= datetime.now() - dt.timedelta(days=7)

def download_image(hashtag_label, patience_max, filter):
    L = instaloader.Instaloader(compress_json=False, download_comments=False, download_videos=False,
                                filename_pattern='{date_local}_BRT')
    posts = L.get_hashtag_posts(hashtag_label)
    patience = 0
    for post in posts: 
        if filter(post):
            patience = 0
            L.download_post(post, '#' + hashtag_label)
        else:
            patience += 1
            print(patience)
            if patience == patience_max:
                break

def download_today(hashtag_label, patience_max=20):
    download_image(hashtag_label, patience_max, post_from_today)
            
def download_year(hashtag_label, patience_max=1000):
    download_image(hashtag_label, patience_max, post_from_this_year)

def download_last_7_days(hashtag_label, patience_max=50):
    download_image(hashtag_label, patience_max, post_from_last_7_days)

# download all hashtags since 2019/01/01
def download_hashtags_year(hashtag_labels):
    for hashtag_label in hashtag_labels:
        download_year(hashtag_label)

def download_hashtags_last_7_days(hashtag_labels):
    for hashtag_label in hashtag_labels:
        download_last_7_days(hashtag_label)

# download all hashtags daily
def cronjob():
    for hashtag_label in hashtag_labels:
        schedule.every().day.at("13:45").do(download_today, hashtag_label)
    while True:
        if 'stop_.md' in os.listdir('./'):
            print("Cronjob stopped")
            break
        schedule.run_pending()
        time.sleep(60) # wait one minute

def start_cron():
    print("Cronjob started")
    os.system('rm -rf stop_.md')
    cronjob()

download_hashtags_year(['mariellepresente'])


# download_hashtags_last_7_days(hashtag_labels)

