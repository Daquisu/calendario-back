import instaloader
from consts import HASHTAG_LABELS

hashtag_labels = []
for hashtag_label in HASHTAG_LABELS:
    hashtag_labels.append(hashtag_label[1:])

authors = ['crisvector', '_bijari']

def post_with_hashtag(post):
    flag = False
    for hashtag_label in hashtag_labels:
        if hashtag_label in post.caption_hashtags:
            flag = True
    return flag

L = instaloader.Instaloader(compress_json=False, download_comments=False, download_videos=False,
                                filename_pattern='{date_local}_BRT')
for author in authors:
    L.download_profile(author, post_filter=post_with_hashtag)
