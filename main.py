from datetime import datetime
from itertools import dropwhile, takewhile

import instaloader

L = instaloader.Instaloader(compress_json=False, download_comments=False)

hashtag_label = 'designativista'

posts = L.get_hashtag_posts(hashtag_label)

# for post in takewhile(lambda p: p.date > UNTIL, dropwhile(lambda p: p.date > SINCE, posts)):
#     print(post.date)
#     L.download_post(post, '#urbanphotography')

today = datetime.today()
today_date = datetime(today.year, today.month, today.day)

for post in posts:
    if post.date_local < datetime(2019, 1, 1):
        print(post.date_local)
        print(today_date)
        paciency += 1
        if paciency == 100:
            break
    else:
        # print('comments:', post.comments, 'likes:', post.likes)
        L.download_post(post, '#' + hashtag_label)


# TODOS
# - Filtrar datetime
# - Integrar c/ classificador
# - Guarda tudo

# FIRULAS
# - apagar arquivo zip
# - guardar nome de usuário do autor
