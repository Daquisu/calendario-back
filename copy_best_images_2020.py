import os

for day in os.listdir('./best'):
    if (day[:4] == '2020'):
        for hashtag in os.listdir('./best/' + day):
            if hashtag.startswith('#'):
                for classification in os.listdir('./best/' + day + '/' + hashtag):
                    for f in os.listdir('./best/' + day + '/' + hashtag + '/' + classification):
                        if f.endswith('.jpg'):
                            os.system('cp ./best/' + day + '/' + hashtag + '/' + classification + '/' + f + ' ./top_6_diario_2020')