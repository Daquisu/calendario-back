import json
import os
import copy
from PIL import Image
import imagehash
from consts import HASHTAG_LABELS

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
    cutoff = 15
    hash1 = imagehash.average_hash(Image.open(image1))
    hash2 = imagehash.average_hash(Image.open(image2))
    if hash1 - hash2 < cutoff or hash2 - hash1 < cutoff:
        return True
    return False


print("")
print("##################")
print("Sorting images by score")
print("##################")
print("")

for hashtag_label in HASHTAG_LABELS:
    highest_scores[hashtag_label] = {}
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
                            highest_scores[date][hashtag_label]['3rd_best'] = copy.deepcopy(highest_scores[date][hashtag_label]['2nd_best'])
                            highest_scores[date][hashtag_label]['2nd_best'] = copy.deepcopy(highest_scores[date][hashtag_label]['best'])
                            highest_scores[date][hashtag_label]['best']['path'] = path
                            highest_scores[date][hashtag_label]['best']['score'] = score
                        elif score > highest_scores[date][hashtag_label]['2nd_best']['score']:
                            highest_scores[date][hashtag_label]['3rd_best'] = copy.deepcopy(highest_scores[date][hashtag_label]['2nd_best'])
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

for day in highest_scores:
    flag_first = False
    highest_scores[day]['top_3'] = {}
    for hashtag_label in highest_scores[day]:
        if not flag_first:
            highest_scores[date]['top_3'] = copy.deepcopy(highest_scores[day][hashtag_label])
            flag_first = True
        else:
            for classification in ['best', '2nd_best', '3rd_best']:
                if highest_scores[date]['top_3']['best']['path'] != None:
                    path1 = highest_scores[date]['top_3']['best']['path'].replace('json', 'jpg')
                if highest_scores[date]['top_3']['2nd_best']['path'] != None:
                    path2 = highest_scores[date]['top_3']['2nd_best']['path'].replace('json', 'jpg')
                if highest_scores[date]['top_3']['3rd_best']['path'] != None:
                    path3 = highest_scores[date]['top_3']['3rd_best']['path'].replace('json', 'jpg')
                if highest_scores[date][hashtag_label][classification]['path'] != None:
                    path_new = highest_scores[date][hashtag_label][classification]['path'].replace('json', 'jpg')
                if (are_similar_images(path1, path_new) and are_similar_images(path2, path_new) and are_similar_images(path3, path_new)):
                    new_score = highest_scores[date][hashtag_label]['best']['score']
                    if new_score > highest_scores[date]['top_3']['3rd_best']['score']:
                        if new_score > highest_scores[date]['top_3']['2nd_best']['score']:
                            highest_scores[date]['top_3']['3rd_best'] = copy.deepcopy(highest_scores[date]['top_3']['2nd_best'])
                            if new_score > highest_scores[date]['top_3']['best']['score']:
                                highest_scores[date]['top_3']['2nd_best'] = copy.deepcopy(highest_scores[date]['top_3']['best'])
                                highest_scores[date]['top_3']['best'] = copy.deepcopy(highest_scores[date][hashtag_label]['best'])
                            else:
                                highest_scores[date]['top_3']['2nd_best'] = copy.deepcopy(highest_scores[date][hashtag_label]['best'])
                        else:
                            highest_scores[date]['top_3']['3rd_best'] = copy.deepcopy(highest_scores[date][hashtag_label]['best'])
            
                        

os.system('rm -rf best')
os.system('mkdir -p best')
print(highest_scores) #
print("")
print("##################")
print("Copying best images from each day")
print("##################")
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
        os.system('cp ' + highest_scores[day][hashtag_label]['best']['path'][:slash] + '*' + highest_scores[day][hashtag_label]['best']['path'][slash:-5] + '* ./best/' + day + '/' + hashtag_label + '/1')
        if highest_scores[day][hashtag_label]['2nd_best']['path'] != None:
            slash = find_index_second_slash(highest_scores[day][hashtag_label]['2nd_best']['path'])
            os.system('cp ' + highest_scores[day][hashtag_label]['2nd_best']['path'][:slash] + '*' + highest_scores[day][hashtag_label]['2nd_best']['path'][slash:-5] + '* ./best/' + day + '/' + hashtag_label + '/2')
            if highest_scores[day][hashtag_label]['3rd_best']['path'] != None:
                slash = find_index_second_slash(highest_scores[day][hashtag_label]['3rd_best']['path'])
                os.system('cp ' + highest_scores[day][hashtag_label]['3rd_best']['path'][:slash] + '*' + highest_scores[day][hashtag_label]['3rd_best']['path'][slash:-5] + '* ./best/'  + day + '/' + hashtag_label + '/3')

print(str(h_s) + ' ' + nome)
print("")
print("Most popular images are in ./best")
print("")
