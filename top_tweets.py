import twitter
import datetime
import json
import os
import nltk
import unicodedata
from unidecode import unidecode
from LeitorDeTweets import semelhancaDeTweets

def deEmojify(inputString):
    returnString = ""

    for character in inputString:
        try:
            if (character in ['á', 'Á', 'ã', 'Ã', 'â',
                              'Â', 'à', 'À', 'é', 'É',
                              'ê', 'Ê', 'í', 'Í', 'ó',
                              'Ó', 'õ', 'Õ', 'ô', 'Ô',
                              'ú', 'Ú', 'ü', 'Ü', 'ç',
                              'Ç']):
                returnString += character
            else:
                character.encode("ascii")
                returnString += character
        except UnicodeEncodeError:
            replaced = unidecode(str(character))
            if replaced != '':
                returnString += replaced
            else:
                try:
                     unicodedata.name(character)
                except ValueError:
                     returnString += "x"

    return returnString

def remove_at_start(text):
    if (text.startswith('@') or text.startswith('>@')):
        space1 = text.find(' ')
        return text[space1: ]
    elif (text.startswith('> @')):
        space2 = text[2:].find(' ')
        return text[(space2 + 2): ]
    return text

today = datetime.date.today()
time_diff = datetime.timedelta(hours=3)   # importante mudar caso horário de verão
today -= time_diff
today_year_month = today.strftime("%Y-%m")
def get_tweets(year_and_month = today_year_month):
    USERS = ['brpolitico', 'CNNBrasil', 'TheInterceptBr', 'canalmeio',
         'elpais_brasil', 'MidiaNINJA', 'OGloboPolitica', 'UOL',
         'folha', 'Estadao']
    MONTH_NUMBER = {'Jan':  1,  'Feb':  2, 'Mar':  3,
                    'Apr':  4,  'May':  5, 'Jun':  6,
                    'Jul':  7,  'Aug':  8, 'Sep':  9,
                    'Oct': 10,  'Nov': 11, 'Dec': 12}
    REMOVED_WORDS = ['BREAKING NEWS: ', 'URGENTE: ', 'EDITORIAL: ', 'CHECAMOS',
                     'Assine BR Politico', 'FOTOS:', 'EXCLUSIVO:']
    REMOVED_ENDS = ['  ', ' ', '.', ',']
    PROFILE_TO_PERSON = {'@jairbolsonaro': 'Bolsonaro',
                         '@felipeneto' : 'Felipe Neto',
                         '@Anitta': 'Anitta',
                         '&gt;': '>'}
    REMOVED_STARTS = ['https://', 't.co']
    api = twitter.Api(consumer_key='EewCgZYFsFqiM8mCYwvNB6zwd',
                    consumer_secret='NIH5nfXj1Lrffvfc7Dt0iDlyoeTqs4uXHsaAtgAaCO1QNF03so',
                    access_token_key='1259568388034252800-Ia2yCymONbioYnVHi40nnMYXNubvm0',
                    access_token_secret='6lXZiB5zyOcYZdqyDcfJMID0QWWR35B0Mg0Bz4eXabSP4',
                    tweet_mode = 'extended')

    tweets_list = []
    fav_rt_counts = []
    # passo 1 pegar os tweets do dia
    today = datetime.date.today()
    today_year_month = today.strftime("%Y-%m")
    if (today_year_month == year_and_month):
        for user in USERS:
            statuses = api.GetUserTimeline(screen_name=user, count=200)
            for tweet in statuses:
                month = MONTH_NUMBER[tweet.created_at[4:7]]
                day = int(tweet.created_at[8:10])
                year = int(tweet.created_at[-4:])
                tweet_date = datetime.date(year, month, day) - time_diff
                if (tweet_date == today):
                    tweets_list.append(tweet)


        # passo 2 separar os tweets por quantidade de fav + rt
        for tweet in tweets_list:
            fav_rt_counts.append(tweet.favorite_count  + tweet.retweet_count)
        sorted_tweets_list = [tweet for _, tweet in sorted(zip(fav_rt_counts,tweets_list), key=lambda pair: pair[0], reverse=True)]

        # passo 3 limpar os tweets para texto e quantidade de fav / rt
        clean_tweets_list = [{'author': tweet.user.screen_name, 'favorite_count': tweet.favorite_count, 'retweet_count': tweet.retweet_count, 'original_text': tweet.full_text} for tweet in sorted_tweets_list]       

        # passo 5 salvar o json
        # cria a pasta para o mês caso não exista
        if(year_and_month not in os.listdir('./top_tweets/raw')):
            os.system('mkdir ./top_tweets/raw/' + year_and_month)
        with open('./top_tweets/raw/' + year_and_month + '/' + today.strftime("%Y-%m-%d") + '.json', 'w') as fp:
            json.dump(clean_tweets_list, fp)

        # passo 6
        # cria um json com apenas 10 tweets, sendo cada tweet de um perfil
        for year_and_month in os.listdir('./top_tweets/raw/'):
            if year_and_month not in os.listdir('./top_tweets/processed/'):
                os.system('mkdir ./top_tweets/processed/' + year_and_month)
            for j_file in os.listdir('./top_tweets/raw/' + year_and_month + '/'):
                if (j_file not in os.listdir('./top_tweets/processed/' + year_and_month + '/') or
                    j_file == today.strftime("%Y-%m-%d") + '.json'):
                    users_used = []
                    processed_tweets = []
                    may_tweets = 0
                    with open('./top_tweets/raw/' + year_and_month + '/' + j_file) as fp:
                        tweets_list = json.load(fp)
                    textosDoDia = []
                    for tweet in tweets_list:
                        tweet['frases'] = nltk.sent_tokenize(tweet['original_text'])
                        for sentence in tweet['frases']:
                            textosDoDia.append(sentence)
                    for tweet in tweets_list:
                        if year_and_month != '2020-05':
                            if (tweet['author'] not in users_used):
                                tweet['text'] = tweet['original_text'][:]
                                url_start_index = tweet['text'].find('https://')
                                if (url_start_index != -1):
                                    url_end_index = tweet['text'][url_start_index:].find(' ')
                                    if (url_end_index != -1):
                                        tweet['url'] = tweet['text'][url_start_index:url_start_index + url_end_index]
                                    else:
                                        tweet['url'] = tweet['text'][url_start_index:]
                                else:
                                    tweet['url'] = ''
                                tweet['text'] = tweet['text'].replace('\n', ' ')
                                for removed_word in REMOVED_WORDS:
                                    tweet['text'] = tweet['text'].replace(removed_word, '')
                                for profile in PROFILE_TO_PERSON:
                                    tweet['text'] = tweet['text'].replace(profile, PROFILE_TO_PERSON[profile])
                                for removed_start in REMOVED_STARTS:
                                    tweet['text'] = ' '.join(word for word in tweet['text'].split(' ') if not word.startswith(removed_start))
                                tweet['text'] = remove_at_start(tweet['text'])
                                for removed_end in REMOVED_ENDS:
                                    if (tweet['text'].endswith(removed_end)):
                                        tweet['text'] = tweet['text'][:-1*len(removed_end)]
                                if (len(deEmojify(tweet['text'])) < 140 and
                                    len(deEmojify(tweet['text'])) > 0 and
                                    not tweet['text'].endswith('...') and
                                    not tweet['text'].startswith('Acompanhe') and
                                    not tweet['text'].startswith('Veja') and
                                    not tweet['text'].startswith('RT ') and
                                    not tweet['text'].startswith('Segue ') and
                                    'Príncipe' not in tweet['text']):
                                    are_similar = False
                                    for top_tweet in processed_tweets:
                                        if (semelhancaDeTweets(tweet, top_tweet, textosDoDia) > 0.25):
                                            are_similar = True
                                    if not are_similar:
                                        users_used.append(tweet['author'])
                                        tweet['text'] = deEmojify(tweet['text'])
                                        processed_tweets.append(tweet)
                            if (len(users_used) == len(USERS)):
                                with open('./top_tweets/processed/' + year_and_month + '/' + j_file, 'w') as output:
                                    json.dump(processed_tweets, output)
                                    break
                            elif (tweet == tweets_list[len(tweets_list)-1]):
                                users_round2 = []
                                for tweet_round2 in tweets_list:
                                    if (tweet_round2['author'] not in users_round2 and
                                        tweet_round2 not in processed_tweets):
                                        tweet_round2['text'] = tweet_round2['original_text'][:]
                                        url_start_index = tweet_round2['text'].find('https://')
                                        if (url_start_index != -1):
                                            url_end_index = tweet_round2['text'][url_start_index:].find(' ')
                                            if (url_end_index != -1):
                                                tweet_round2['url'] = tweet_round2['text'][url_start_index:url_start_index + url_end_index]
                                            else:
                                                tweet_round2['url'] = tweet_round2['text'][url_start_index:]
                                        tweet_round2['text'] = tweet_round2['text'].replace('\n', ' ')
                                        for removed_word in REMOVED_WORDS:
                                            tweet_round2['text'] = tweet_round2['text'].replace(removed_word, '')
                                        for profile in PROFILE_TO_PERSON:
                                            tweet_round2['text'] = tweet_round2['text'].replace(profile, PROFILE_TO_PERSON[profile])
                                        for removed_start in REMOVED_STARTS:
                                            tweet_round2['text'] = ' '.join(word for word in tweet_round2['text'].split(' ') if not word.startswith(removed_start))
                                        tweet_round2['text'] = remove_at_start(tweet_round2['text'])
                                        for removed_end in REMOVED_ENDS:
                                            if (tweet_round2['text'].endswith(removed_end)):
                                                tweet_round2['text'] = tweet_round2['text'][:-1*len(removed_end)]
                                        if (len(deEmojify(tweet_round2['text'])) < 140 and
                                            len(deEmojify(tweet_round2['text'])) > 0 and
                                            not tweet_round2['text'].endswith('...') and
                                            not tweet_round2['text'].startswith('Acompanhe') and
                                            not tweet_round2['text'].startswith('Veja') and
                                            not tweet_round2['text'].startswith('RT ') and
                                            not tweet_round2['text'].startswith('Segue ') and
                                            'Príncipe' not in tweet_round2['text']): 
                                            are_similar = False
                                            for top_tweet in processed_tweets:
                                                if (semelhancaDeTweets(tweet, top_tweet, textosDoDia) > 0.25):
                                                    are_similar = True
                                            if not are_similar:
                                                users_round2.append(tweet_round2['author'])
                                                tweet_round2['text'] = deEmojify(tweet_round2['text'])
                                                processed_tweets.append(tweet_round2)
                                    if (len(users_used) + len(users_round2) == len(USERS)):
                                        with open('./top_tweets/processed/' + year_and_month + '/' + j_file, 'w') as output:
                                            json.dump(processed_tweets, output)
                                            break
                        else:
                            if (may_tweets < 30):
                                if (len(tweet['text']) < 140 and
                                    len(tweet['text']) > 0): 
                                    may_tweets += 1
                                    tweet['text'] = deEmojify(tweet['text'])
                                    processed_tweets.append(tweet)
                            else:
                                with open('./top_tweets/processed/' + year_and_month + '/' + j_file, 'w') as output:
                                    json.dump(processed_tweets, output)


def clean_old_json():
    REMOVED_WORDS = ['- via', 'BREAKING NEWS: ', 'URGENTE: ', 'EDITORIAL: ', 'RT ', '-via', '; ouça']
    REMOVED_STARTS = ['https://', 't.co', '>@', '@', '&gt;@', '(via']

    for f in os.listdir('./top_tweets/2020-05/'):
        print('./top_tweets/2020-05/' + f)
        with open ('./top_tweets/2020-05/' + f, 'r') as j_file:
            data = json.load(j_file)
            for tweet_index in range(len(data)):
                text = data[tweet_index]['text']
                for removed_word in REMOVED_WORDS:
                    text = text.replace(removed_word, '')
                for removed_start in REMOVED_STARTS:
                    text = ' '.join(word for word in text.split(' ') if not word.startswith(removed_start))
                data[tweet_index]['text'] = text
            with open ('./top_tweets/2020-05/' + f + '2', 'w+') as fp:
                json.dump(data, fp)
        os.system('rm ' + './top_tweets/2020-05/' + f )
        os.system('mv ' + './top_tweets/2020-05/' + f + '2 ' + './top_tweets/2020-05/' + f)

if (__name__ == '__main__'):
    get_tweets()