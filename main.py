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

def post_since_yesterday(post):
    now =  datetime.now()
    today = datetime(now.year, now.month, now.day)
    return post.date_local >= today

def post_from_this_year(post):
    return post.date_local >= datetime(2019, 1, 1)

def post_from_last_month(post):
    return post.date_local >= datetime.now() - dt.timedelta(days=30)

def post_from_last_7_days(post):
    return post.date_local >= datetime.now() - dt.timedelta(days=7)

def download_image(hashtag_label, patience_max, filter):
    L = instaloader.Instaloader(compress_json=False, download_comments=False, download_videos=False,
                                filename_pattern='{date_local}_BRT', max_connection_attempts=10,
                                 dirname_pattern='{target}')
    posts = L.get_hashtag_posts(hashtag_label)
    patience = 0
    counter = 0
    flag_first = True
    if not patience%1000:
        time.sleep(60)
    for post in posts: 
        if filter(post):
            patience = 0
            flag_first = False
            try:
                L.download_post(post, '#' + hashtag_label)
            except:
                pass
        else:
            if not flag_first:
                patience += 1
            print('Skipped', counter, 'posts')
            counter += 1
            if patience == patience_max:
                break

def download_image_eleicoes(hashtag_label, patience_max, filter):
    L = instaloader.Instaloader(compress_json=False, download_comments=False, download_videos=False,
                                filename_pattern='{date_local}_BRT', max_connection_attempts=8001,
                                 dirname_pattern='{target}_eleicoes')
    posts = L.get_hashtag_posts(hashtag_label)
    patience = 0
    counter = 0
    flag_first = True
    if not patience%1000:
        time.sleep(60)
    for post in posts: 
        if filter(post):
            patience = 0
            flag_first = False
            try:
                L.download_post(post, '#' + hashtag_label)
            except:
                pass
        else:
            if not flag_first:
                patience += 1
            print('Skipped', counter, 'posts')
            counter += 1
            if patience == patience_max:
                break

def download_since_yesterday(hashtag_label, patience_max=20):
    download_image(hashtag_label, patience_max, post_since_yesterday)
    os.system('python sort_best.py')
            
def download_year(hashtag_label, patience_max=1000):
    download_image(hashtag_label, patience_max, post_from_this_year)

def download_last_month(hashtag_label, patience_max=100):
    download_image(hashtag_label, patience_max, post_from_last_month)

def download_last_7_days(hashtag_label, patience_max=50):
    download_image(hashtag_label, patience_max, post_from_last_7_days)

# download all hashtags since 2019/01/01
def download_hashtags_year(hashtag_labels):
    for hashtag_label in hashtag_labels:
        download_year(hashtag_label)

def download_hashtags_last_month(hashtag_labels):
    for hashtag_label in hashtag_labels:
        download_last_month(hashtag_label)

def download_hashtags_last_7_days(hashtag_labels):
    for hashtag_label in hashtag_labels:
        download_last_7_days(hashtag_label, 50)
    os.system('python sort_best.py')

# download all hashtags daily
def cronjob():
    schedule.every().day.at("09:10").do(download_hashtags_last_7_days, hashtag_labels)
    schedule.every().day.at("17:10").do(download_hashtags_last_7_days, hashtag_labels)
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

def custom_data(post):
    return post.date_local >= datetime(2018, 10, 18) and post.date_local <= datetime(2018, 11, 18)
    
if __name__ == '__main__':
    download_hashtags_last_7_days(hashtag_labels)
    os.system('python sort_best.py')
    # for hashtag_label in ['coleraalegria']:
    #     download_image_eleicoes(hashtag_label, 100000 ,custom_data)


# download_hashtags_last_7_days(hashtag_labels)


