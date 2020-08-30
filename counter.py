import glob
import os
from consts import HASHTAG_LABELS

files = []
for hashtag in HASHTAG_LABELS:
    for f in glob.glob('./' + hashtag + '/2020-03-1[34]*.txt'):
        flag = False
        with open(f) as txt_file:
            for line in txt_file:
                for hashtag in ['#racismo', '#homofobia']:
                    if not flag:
                        if hashtag in line.lower():
                            files.append(f[:-4]+'* ')
                            flag = True
                        
files = ''.join(files)
os.system('cp ' + files + './imagens\ 13-03\ e\ 14-03/2020')
