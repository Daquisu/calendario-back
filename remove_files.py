import os
import datetime

today_date = datetime.date.today()
last_month_date = today_date - datetime.timedelta(days=30)

for hashtag in ['#coleraalegria', '#desenhospelademocracia', '#mariellepresente', '#designativista']:
    file_names = []
    for day in os.listdir('./best'):
        if (hashtag in os.listdir('./best/' + day)):
            for classification in os.listdir('./best/' + day + '/' + hashtag):
                for f in os.listdir('./best/' + day + '/' + hashtag + '/' + classification):
                    file_names.append(f)
    
    if (file_names != []):
        for f in os.listdir('./' + hashtag):
            file_date = datetime.datetime.strptime(f[:10], "%Y-%m-%d").date()
            if (f not in file_names and file_date < last_month_date):
                os.system('rm ./' + hashtag + '/' + f)
            elif (file_date > last_month_date):
                print(f)
