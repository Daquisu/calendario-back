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

def download_image_eleicoes(hashtag_label, patience_max, filter):
    L = instaloader.Instaloader(compress_json=False, download_comments=False, download_videos=False,
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

    # for post in posts: 
    #     if filter(post):
    #         patience = 0
    #         flag_first = False
    #         try:
    #             L.download_post(post, '#' + hashtag_label)
    #         except:
    #             pass
    #     else:
    #         if not flag_first:
    #             patience += 1
    #         counter += 1
    #         if patience == patience_max:
    #             break

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
    schedule.every(2).hours.do(download_hashtags_last_7_days, hashtag_labels)
    schedule.every().day.at("00:00").do(remove_files)
    schedule.every(1).hours.do(get_tweets)
    #schedule.every().day.at("17:10").do(download_hashtags_last_7_days, hashtag_labels)
    while True:
        if 'stop_.md' in os.listdir('./'):
            print("Cronjob stopped")
            break
        schedule.run_pending()
        time.sleep(60) # wait one minute

def remove_files():
    today_date = dt.date.today()
    last_month_date = today_date - dt.timedelta(days=30)
# todo
    for hashtag in HASHTAG_LABELS:
        file_names = []
        for day in os.listdir('./best'):
            if (hashtag in os.listdir('./best/' + day)):
                for classification in os.listdir('./best/' + day + '/' + hashtag):
                    for f in os.listdir('./best/' + day + '/' + hashtag + '/' + classification):
                        file_names.append(f)
        
        if (file_names != []):
            for f in os.listdir('./' + hashtag):
                file_date = datetime.strptime(f[:10], "%Y-%m-%d").date()
                if (f not in file_names and file_date < last_month_date):
                    os.system('rm ./' + hashtag + '/' + f)
                elif (file_date > last_month_date):
                    print(f)

def start_cron():
    print("Cronjob started")
    os.system('rm -rf stop_.md')
    cronjob()

def custom_data(post):
    return (post.date_local >= datetime(2018, 10, 5) and post.date_local <= datetime(2018, 11, 6)) or post.date_local >= datetime(2018, 9, 29) and post.date_local < datetime(2018, 9, 30)
    
if __name__ == '__main__':
    download_hashtags_last_month(hashtag_labels)
    os.system('python sort_best.py')
    # for hashtag_label in ['mariellepresente', 'elenao']:
    #     download_image_eleicoes(hashtag_label, 100000 ,custom_data)


# download_hashtags_last_7_days(hashtag_labels)


