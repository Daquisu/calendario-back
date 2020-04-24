#%%
import json
import os
from PIL import Image
import imagehash
from consts import HASHTAG_LABELS
import time
import pandas as pd
import numpy as np
from api import get_metadata

def deepcopy(org):
    '''
    much, much faster than deepcopy, for a dict of the simple python types.
    '''
    out = dict().fromkeys(org)
    for k,v in org.items():
        try:
            out[k] = v.copy()   # dicts, sets
        except AttributeError:
            try:
                out[k] = v[:]   # lists, tuples, strings, unicode
            except TypeError:
                out[k] = v      # ints
 
    return out

highest_scores = {}

def get_date(name):
    return name[:10]

def get_year_and_month(day):
    return day[:7]

def get_year(day):
    return day[:4]
    
def calculate_score(file):
    try:
        with open(file) as json_file:
            data = json.load(json_file)
            score = data['node']['edge_liked_by']['count'] + 0*data['node']['edge_media_to_comment']['count']
            return score
    except:
        return 0

def is_new_image(highest_scores_day, ending):
    for classification in ['best', '2nd_best', '3rd_best']:
        if highest_scores_day[classification]['path'] == None:
            return True
        if highest_scores_day[classification]['path'].endswith(ending):
            return False    
    return True

def find_index_second_slash(path):
    n_slash = 0
    for index in range(len(path)):
        if path[index] == '/':
            n_slash += 1
        if n_slash == 2:
            return index+1

def are_similar_images(image1, image2):
    if image1 == None or image2 == None:
        return False
    cutoff = 15
    hash1 = imagehash.average_hash(Image.open(image1))
    hash2 = imagehash.average_hash(Image.open(image2))
    if hash1 - hash2 < cutoff:
        return True
    return False

def get_path_to_compare_images(path):
    if path == None:
        return None
    else:
        path_new = path.replace('json', 'jpg')
        if not os.path.isfile(path_new):
            path_new = path_new.replace('BRT', 'BRT_1')
        return path_new

print("")
print("##################")
print("Sorting images by score")
print("##################")
print("")
t1 = time.time()
post_information_dict = {'path': [], 'score': [], 'date': [], 'hashtag': []}
used_dates = []
for hashtag_label in HASHTAG_LABELS:
    arr = os.listdir("./" + hashtag_label + "/")
    for index in range(len(arr)):
        if arr[index].endswith('.json'):
            path = './' + hashtag_label + '/' + arr[index]
            score = calculate_score(path)
            date = get_date(arr[index])
            post_information_dict['path'].append(get_path_to_compare_images(path))
            post_information_dict['score'].append(score)
            post_information_dict['date'].append(date)
            post_information_dict['hashtag'].append(hashtag_label)
            if date not in used_dates:
                used_dates.append(date)

post_information_df = pd.DataFrame(data=post_information_dict)
post_information_df = post_information_df.sort_values(ascending = False, by=['score'])
hashtag_and_top = HASHTAG_LABELS[:]
hashtag_and_top.append('top_3')
n_days = 0
for date in used_dates:
    if date == '2020-04-12':
        print('Oi')
    n_days += 1
    print('Days = ', n_days, 'Total time =', time.time()-t1)
    bool_date_array = post_information_df['date'] == date
    highest_scores[date] = {}
    for hashtag in hashtag_and_top:
        if hashtag != 'top_3':
            bool_hashtag_array = post_information_df['hashtag'] == hashtag
        else:
            bool_hashtag_array = np.ones(len(post_information_df.index), dtype=bool)
        classification = 1
        index_counter = 0
        while classification != 4 and index_counter < len(post_information_df[bool_date_array & bool_hashtag_array].index):
            if index_counter == 0:
                highest_scores[date][hashtag] = {'best':     {'path': None, 'score': 0},
                                                 '2nd_best': {'path': None, 'score': 0},
                                                 '3rd_best': {'path': None, 'score': 0}}
            path = post_information_df[bool_date_array & bool_hashtag_array].iloc[index_counter].path
            score = post_information_df[bool_date_array & bool_hashtag_array].iloc[index_counter].score
            if classification == 3:
                if not are_similar_images(highest_scores[date][hashtag]['best']['path'], path) and not are_similar_images(highest_scores[date][hashtag]['2nd_best']['path'], path):
                   highest_scores[date][hashtag]['3rd_best']['path'] = path
                   highest_scores[date][hashtag]['3rd_best']['score'] = score
                   classification += 1
            if classification == 2:
                if not are_similar_images(highest_scores[date][hashtag]['best']['path'], path):
                    highest_scores[date][hashtag]['2nd_best']['path'] = path
                    highest_scores[date][hashtag]['2nd_best']['score'] = score
                    classification += 1
            if classification == 1:
                highest_scores[date][hashtag]['best']['path'] = path
                highest_scores[date][hashtag]['best']['score'] = score
                classification += 1
            index_counter += 1
                      
os.system('rm -rf best_updating')
os.system('mkdir -p best_updating')
print(highest_scores) #
print("")
print("##################")
print("Copying best images from each day")
print("##################")
print("")
print("Total time = ", time.time()-t1)
print("")
h_s = 0 #
nome = '' #
for day in highest_scores:
    year_and_month = get_year_and_month(day)
    os.system('mkdir -p best_updating/' + day)
    for hashtag_label in highest_scores[day]:
        if highest_scores[day][hashtag_label]['best']['score'] > h_s: #s
            h_s = highest_scores[day][hashtag_label]['best']['score'] #
            nome = highest_scores[day][hashtag_label]['best']['path'] #
        os.system('mkdir -p best_updating/' + day + '/' + hashtag_label + '/1')
        os.system('mkdir -p best_updating/' + day + '/' + hashtag_label + '/2')
        os.system('mkdir -p best_updating/' + day + '/' + hashtag_label + '/3')
        slash = find_index_second_slash(highest_scores[day][hashtag_label]['best']['path'])
        os.system('cp ' + highest_scores[day][hashtag_label]['best']['path'][:slash] + '*' + highest_scores[day][hashtag_label]['best']['path'][slash:-6] + '* ./best_updating/' + day + '/' + hashtag_label + '/1')
        if highest_scores[day][hashtag_label]['2nd_best']['path'] != None:
            slash = find_index_second_slash(highest_scores[day][hashtag_label]['2nd_best']['path'])
            os.system('cp ' + highest_scores[day][hashtag_label]['2nd_best']['path'][:slash] + '*' + highest_scores[day][hashtag_label]['2nd_best']['path'][slash:-6] + '* ./best_updating/' + day + '/' + hashtag_label + '/2')
            if highest_scores[day][hashtag_label]['3rd_best']['path'] != None:
                slash = find_index_second_slash(highest_scores[day][hashtag_label]['3rd_best']['path'])
                os.system('cp ' + highest_scores[day][hashtag_label]['3rd_best']['path'][:slash] + '*' + highest_scores[day][hashtag_label]['3rd_best']['path'][slash:-6] + '* ./best_updating/'  + day + '/' + hashtag_label + '/3')

os.system('rm -rf best')
os.system('mv best_updating best')

print(str(h_s) + ' ' + nome)
print("")
print("Most popular images are in ./best")
print("")
del highest_scores

print("##################")
print('Creating files for end point "download_month"')
print("##################")
t1 = time.time()
os.system('rm -rf jsons_updating')
os.system('mkdir -p jsons_updating')

number_to_str = {'1': 'best', '2': '2nd_best', '3': '3rd_best'}
super_json = {}
script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
print(script_dir)
for day in os.listdir('./best'):
    year_and_month = get_year_and_month(day)
    if get_year(day) not in os.listdir('./jsons_updating'):
        os.system('mkdir -p ./jsons_updating/' + get_year(day))
    if year_and_month not in super_json:
        super_json[year_and_month] = {}
    if day not in super_json[year_and_month]:
        super_json[year_and_month][day] = {}
        super_json[year_and_month][day]['images'] = {}
        super_json[year_and_month][day]['used_tags'] = []
        index = 0
    for hashtag in sorted(os.listdir('./best/' + day)):
        if hashtag == 'top_3':
            super_json[year_and_month][day][hashtag] = {}
        else:
            super_json[year_and_month][day]['images'][hashtag] = {}
        for classification in ['2', '3', '1']:
            if hashtag == 'top_3':
                paths = []
            else:
                paths = {}
            for f in sorted(os.listdir('./best/' + day + '/' + hashtag + '/' + classification)):
                if f.endswith('.jpg'):
                    if hashtag[0] == '#':
                        paths[index] = './best/' + day + '/' + 'HASHTAG' + hashtag[1:] + '/' + classification + '/' + f
                        index += 1
                    else:
                        paths.append('./best/' + day + '/' + hashtag + '/' + classification + '/' + f)
                if f.endswith('.json'):
                    if not hashtag.startswith('top_3'):
                        super_json[year_and_month][day]['images'][hashtag][number_to_str[classification]] = deepcopy(get_metadata(day, hashtag, classification, f))
                        for tag in super_json[year_and_month][day]['images'][hashtag][number_to_str[classification]]['tags']:
                            if tag not in super_json[year_and_month][day]['used_tags']:
                                super_json[year_and_month][day]['used_tags'].append(tag)
                        super_json[year_and_month][day]['images'][hashtag][number_to_str[classification]]['paths'] = paths
                    else:
                        super_json[year_and_month][day][hashtag][number_to_str[classification]] = deepcopy(get_metadata(day, hashtag, classification, f))
                        super_json[year_and_month][day][hashtag][number_to_str[classification]]['paths'] = paths
            super_json[year_and_month][day]['used_tags'].sort()


for year_and_month in super_json:
    rel_path = 'jsons_updating' + '/' + get_year(year_and_month) + '/' + year_and_month + '.json'
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path, 'w+') as f:
        json.dump(super_json[year_and_month], f)

os.system('rm -rf jsons_download_month')
os.system('mv jsons_updating jsons_download_month')

print("")
print("Files created")
print("")

print("Total time = ", time.time()-t1)
