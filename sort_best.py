import json
import os
from PIL import Image
import imagehash
from consts import HASHTAG_LABELS
import time

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

hashtag_labels = ['#coleraalegria', '#desenhospelademocracia', '#designativista', '#mariellepresente']

def get_date(name):
    return name[:10]
    
def calculate_score(file):
    with open(file) as json_file:
        data = json.load(json_file)
        score = data['node']['edge_liked_by']['count'] + 0*data['node']['edge_media_to_comment']['count']
        return score

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
    cutoff = 20
    hash1 = imagehash.average_hash(Image.open(image1))
    hash2 = imagehash.average_hash(Image.open(image2))
    if hash1 - hash2 < cutoff:
        return True
    return False


print("")
print("##################")
print("Sorting images by score")
print("##################")
print("")

for hashtag_label in HASHTAG_LABELS:
    arr = os.listdir("./" + hashtag_label + "/")
    for index in range(len(arr)):
        if arr[index].endswith('.json'):
            path = './' + hashtag_label + '/' + arr[index]
            score = calculate_score(path)
            date = get_date(arr[index])
            if date in highest_scores:
                if hashtag_label in highest_scores[date]:
                    if is_new_image(highest_scores[date][hashtag_label], 'path'):
                        if score > highest_scores[date][hashtag_label]['best']['score']:
                            highest_scores[date][hashtag_label]['3rd_best']['path'] = highest_scores[date][hashtag_label]['2nd_best']['path']
                            highest_scores[date][hashtag_label]['3rd_best']['score'] = highest_scores[date][hashtag_label]['2nd_best']['score']
                            highest_scores[date][hashtag_label]['2nd_best']['path'] = highest_scores[date][hashtag_label]['best']['path']
                            highest_scores[date][hashtag_label]['2nd_best']['score'] = highest_scores[date][hashtag_label]['best']['score']
                            highest_scores[date][hashtag_label]['best']['path'] = path
                            highest_scores[date][hashtag_label]['best']['score'] = score
                        elif score > highest_scores[date][hashtag_label]['2nd_best']['score']:
                            highest_scores[date][hashtag_label]['3rd_best']['path'] = highest_scores[date][hashtag_label]['2nd_best']['path']
                            highest_scores[date][hashtag_label]['3rd_best']['score'] = highest_scores[date][hashtag_label]['2nd_best']['score']
                            highest_scores[date][hashtag_label]['2nd_best']['path'] = path
                            highest_scores[date][hashtag_label]['2nd_best']['score'] = score
                        elif score > highest_scores[date][hashtag_label]['3rd_best']['score']:
                            highest_scores[date][hashtag_label]['3rd_best']['path'] = path
                            highest_scores[date][hashtag_label]['3rd_best']['score'] = score
                else:
                    highest_scores[date][hashtag_label] = {'best':     {'path': path, 'score': score},
                                                           '2nd_best': {'path': None, 'score': 0},
                                                           '3rd_best': {'path': None, 'score': 0}}
            else:
                highest_scores[date] = {hashtag_label: ''}
                highest_scores[date][hashtag_label] = {'best':     {'path': path, 'score': score},
                                                       '2nd_best': {'path': None, 'score': 0},
                                                       '3rd_best': {'path': None, 'score': 0}}

t1 = time.time()
counter = 0
for date in highest_scores:
    counter += 1
    if not counter%10:
        print(counter)

    flag_first = False
    highest_scores[date]['top_3'] = {}
    hashtags = list(highest_scores[date].keys())[:]
    for hashtag_label in hashtags:
        if not flag_first:
            highest_scores[date]['top_3'] = deepcopy(highest_scores[date][hashtag_label])
            flag_first = True
        else:
            for classification in ['best', '2nd_best', '3rd_best']:
                path_new = None
                path1 = None
                path2 = None
                path3 = None
                if highest_scores[date][hashtag_label][classification]['path'] != None:
                    path_new = highest_scores[date][hashtag_label][classification]['path'].replace('json', 'jpg')
                    if not os.path.isfile(path_new):
                        path_new = path_new.replace('BRT', 'BRT_1')
                if highest_scores[date]['top_3']['best']['path'] != None:
                    path1 = highest_scores[date]['top_3']['best']['path'].replace('json', 'jpg')
                    if not os.path.isfile(path1):
                        path1 = path1.replace('BRT', 'BRT_1')
                if highest_scores[date]['top_3']['2nd_best']['path'] != None:
                    path2 = highest_scores[date]['top_3']['2nd_best']['path'].replace('json', 'jpg')
                    if not os.path.isfile(path2):
                        path2 = path2.replace('BRT', 'BRT_1')
                if highest_scores[date]['top_3']['3rd_best']['path'] != None:
                    path3 = highest_scores[date]['top_3']['3rd_best']['path'].replace('json', 'jpg')
                    if not os.path.isfile(path3):
                        path3 = path3.replace('BRT', 'BRT_1')
                if (not are_similar_images(path1, path_new) and not are_similar_images(path2, path_new) and not are_similar_images(path3, path_new)):
                    score = highest_scores[date][hashtag_label][classification]['score']
                    if score > highest_scores[date]['top_3']['best']['score']:
                        highest_scores[date]['top_3']['3rd_best']['path'] = highest_scores[date]['top_3']['2nd_best']['path']
                        highest_scores[date]['top_3']['3rd_best']['score'] = highest_scores[date]['top_3']['2nd_best']['score']
                        highest_scores[date]['top_3']['2nd_best']['path'] = highest_scores[date]['top_3']['best']['path']
                        highest_scores[date]['top_3']['2nd_best']['score'] = highest_scores[date]['top_3']['best']['score']
                        highest_scores[date]['top_3']['best']['path'] = path_new
                        highest_scores[date]['top_3']['best']['score'] = score
                    elif score > highest_scores[date]['top_3']['2nd_best']['score']:
                        highest_scores[date]['top_3']['3rd_best']['path'] = highest_scores[date]['top_3']['2nd_best']['path']
                        highest_scores[date]['top_3']['3rd_best']['score'] = highest_scores[date]['top_3']['2nd_best']['score']
                        highest_scores[date]['top_3']['2nd_best']['path'] = path_new
                        highest_scores[date]['top_3']['2nd_best']['score'] = score
                    elif score > highest_scores[date]['top_3']['3rd_best']['score']:
                        highest_scores[date]['top_3']['3rd_best']['path'] = path_new
                        highest_scores[date]['top_3']['3rd_best']['score'] = score


                        
os.system('rm -rf best')
os.system('mkdir -p best')
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
    os.system('mkdir -p best/' + day)
    for hashtag_label in highest_scores[day]:
        if highest_scores[day][hashtag_label]['best']['score'] > h_s: #s
            h_s = highest_scores[day][hashtag_label]['best']['score'] #
            nome = highest_scores[day][hashtag_label]['best']['path'] #
        os.system('mkdir -p best/' + day + '/' + hashtag_label + '/1')
        os.system('mkdir -p best/' + day + '/' + hashtag_label + '/2')
        os.system('mkdir -p best/' + day + '/' + hashtag_label + '/3')
        slash = find_index_second_slash(highest_scores[day][hashtag_label]['best']['path'])
        os.system('cp ' + highest_scores[day][hashtag_label]['best']['path'][:slash] + '*' + highest_scores[day][hashtag_label]['best']['path'][slash:-6] + '* ./best/' + day + '/' + hashtag_label + '/1')
        if highest_scores[day][hashtag_label]['2nd_best']['path'] != None:
            slash = find_index_second_slash(highest_scores[day][hashtag_label]['2nd_best']['path'])
            os.system('cp ' + highest_scores[day][hashtag_label]['2nd_best']['path'][:slash] + '*' + highest_scores[day][hashtag_label]['2nd_best']['path'][slash:-6] + '* ./best/' + day + '/' + hashtag_label + '/2')
            if highest_scores[day][hashtag_label]['3rd_best']['path'] != None:
                slash = find_index_second_slash(highest_scores[day][hashtag_label]['3rd_best']['path'])
                os.system('cp ' + highest_scores[day][hashtag_label]['3rd_best']['path'][:slash] + '*' + highest_scores[day][hashtag_label]['3rd_best']['path'][slash:-6] + '* ./best/'  + day + '/' + hashtag_label + '/3')

print(str(h_s) + ' ' + nome)
print("")
print("Most popular images are in ./best")
print("")
