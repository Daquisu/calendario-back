#testezin commit
import datetime as dt
from datetime import datetime
import instaloader
import schedule
import time
import os
import json
import re
import zipfile
import zlib
from consts import HASHTAG_LABELS
from top_tweets import get_tweets

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
                                filename_pattern='{date_local}_BRT', max_connection_attempts=8000,
                                 dirname_pattern='{target}')
    posts = L.get_hashtag_posts(hashtag_label)
    patience = 0
    counter = 0
    flag_first = True
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

def download_video(hashtag_label, patience_max, filter):
    L = instaloader.Instaloader(compress_json=False, download_comments=False, download_videos=True,
                                filename_pattern='{date_local}_BRT', max_connection_attempts=8000,
                                 dirname_pattern='{target}')
    posts = L.get_hashtag_posts(hashtag_label)
    patience = 0
    counter = 0
    flag_first = True
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
    L = instaloader.Instaloader(compress_json=False, download_comments=False, download_videos=True,
                                filename_pattern='{date_local}_BRT', max_connection_attempts=15000,
                                 dirname_pattern='{target}_eleicoes')
    posts = iter(L.get_hashtag_posts(hashtag_label))
    patience = 0
    counter = 0
    flag_first = True
    while(True):
        try:
            post = next(posts)
            if filter(post):
                patience = 0
                flag_first = False
                try:
                    L.download_post(post, '#' + hashtag_label)
                except Exception as e:
                    print(e)
                    pass
            else:
                if not flag_first:
                    patience += 1
                counter += 1
                if patience == patience_max:
                    break
        except StopIteration:
            print("End of posts")
            break
        except Exception as e:
            print(e)
            pass

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
        if (hashtag_label != 'projetemos'):
            download_last_7_days(hashtag_label, 50)
    for hashtag_label in ['projetemos']:
        download_video(hashtag_label, 50, post_from_last_7_days)
    os.system('python sort_best.py')

# download all hashtags daily
def cronjob():
    schedule.every(2).hours.do(download_hashtags_last_7_days, hashtag_labels)
    #schedule.every().day.at("00:00").do(remove_files)
    schedule.every(1).hours.do(get_tweets)
    #schedule.every().day.at("17:10").do(download_hashtags_last_7_days, hashtag_labels)
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
    return post.date_local >= datetime(2020, 3, 15)

def zip_non_used_files():
    for hashtag in HASHTAG_LABELS:
        path = f"./#{hashtag}"
        arqZip = zipfile.ZipFile(f"#{hashtag}ZIP.zip", "w", zipfile.ZIP_DEFLATED)
        for file in os.listdir(path):
            arqZip.write(os.path.join(path, str(file)), str(file))
            print(f"Zipping {str(file)}")
        arqZip.close()
    
if __name__ == '__main__':
    start_cron()