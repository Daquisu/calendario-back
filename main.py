from datetime import datetime
import instaloader

hashtag_labels = ['designativista', 'mariellepresente', 'desenhospelademocracia',
                  'coleraalegria', 'elenao']

hashtag_label = 'mariellepresente'

def post_from_today(post):
    now =  datetime.now()
    today = datetime(now.year, now.month, now.day)
    return post.date_local >= today

def post_from_this_year(post):
    return post.date_local >= datetime(2019, 1, 1)

# L.download_hashtag(hashtag_label, post_filter=filter_today)
        
def download_image(hashtag_label, patience_max, filter):
    L = instaloader.Instaloader(compress_json=False, download_comments=False)
    posts = L.get_hashtag_posts(hashtag_label)
    patience = 0
    for post in posts: 
        if filter(post):
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

download_today(hashtag_label)

# TODOS
# - Filtrar datetime
# - Integrar c/ classificador
# - Guarda tudo

# FIRULAS
# - apagar arquivo zip
# - guardar nome de usuário do autor
