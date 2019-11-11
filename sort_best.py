import json
import os
import copy

highest_scores = {}

hashtag_labels = ['#coleraalegria', '#desenhospelademocracia', '#designativista', '#mariellepresente']

def get_date(name):
    return name[:10]
    
def calculate_score(file):
    with open(file) as json_file:
        data = json.load(json_file)
        score = data['node']['edge_liked_by']['count'] + 2*data['node']['edge_media_to_comment']['count']
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

print("")
print("##################")
print("Sorting images by score")
print("##################")
print("")

for hashtag_label in hashtag_labels:
    highest_scores[hashtag_label] = {}
    arr = os.listdir("./" + hashtag_label + "/")
    for index in range(len(arr)):
        if arr[index].endswith('.json'):
            path = './' + hashtag_label + '/' + arr[index]
            score = calculate_score(path)
            date = get_date(arr[index])
            if date in highest_scores[hashtag_label]:
                if is_new_image(highest_scores[hashtag_label][date], 'path'):
                    if score > highest_scores[hashtag_label][date]['best']['score']:
                        highest_scores[hashtag_label][date]['3rd_best'] = copy.deepcopy(highest_scores[hashtag_label][date]['2nd_best'])
                        highest_scores[hashtag_label][date]['2nd_best'] = copy.deepcopy(highest_scores[hashtag_label][date]['best'])
                        highest_scores[hashtag_label][date]['best']['path'] = path
                        highest_scores[hashtag_label][date]['best']['score'] = score
                    elif score > highest_scores[hashtag_label][date]['2nd_best']['score']:
                        highest_scores[hashtag_label][date]['3rd_best'] = copy.deepcopy(highest_scores[hashtag_label][date]['2nd_best'])
                        highest_scores[hashtag_label][date]['2nd_best']['path'] = path
                        highest_scores[hashtag_label][date]['2nd_best']['score'] = score
                    elif score > highest_scores[hashtag_label][date]['3rd_best']['score']:
                        highest_scores[hashtag_label][date]['3rd_best']['path'] = path
                        highest_scores[hashtag_label][date]['3rd_best']['score'] = score
            else:
                highest_scores[hashtag_label][date] = {'best':     {'path': path, 'score': score},
                                        '2nd_best': {'path': None, 'score': 0},
                                        '3rd_best': {'path': None, 'score': 0}}
os.system('rm -rf best')
os.system('mkdir -p best')

print("")
print("##################")
print("Copying best images from each day")
print("##################")
print("")
h_s = 0
nome = ''
print(highest_scores)
for hashtag_label in hashtag_labels:
    os.system('mkdir -p best/' + hashtag_label)
    for day in highest_scores[hashtag_label]:
        if highest_scores[hashtag_label][day]['best']['score'] > h_s:
            h_s = highest_scores[hashtag_label][day]['best']['score']
            nome = highest_scores[hashtag_label][day]['best']['path']
        os.system('mkdir -p best/' + hashtag_label + '/' + day + '/1')
        os.system('mkdir -p best/' + hashtag_label + '/' + day + '/2')
        os.system('mkdir -p best/' + hashtag_label + '/' + day + '/3')
        slash = find_index_second_slash(highest_scores[hashtag_label][day]['best']['path'])
        os.system('cp ' + highest_scores[hashtag_label][day]['best']['path'][:slash] + '*' + highest_scores[hashtag_label][day]['best']['path'][slash:-5] + '* ./best/' + hashtag_label + '/' + day + '/1')
        if highest_scores[hashtag_label][day]['2nd_best']['path'] != None:
            slash = find_index_second_slash(highest_scores[hashtag_label][day]['2nd_best']['path'])
            os.system('cp ' + highest_scores[hashtag_label][day]['2nd_best']['path'][:slash] + '*' + highest_scores[hashtag_label][day]['2nd_best']['path'][slash:-5] + '* ./best/' + hashtag_label + '/' + day + '/2')
            if highest_scores[hashtag_label][day]['3rd_best']['path'] != None:
                slash = find_index_second_slash(highest_scores[hashtag_label][day]['3rd_best']['path'])
                os.system('cp ' + highest_scores[hashtag_label][day]['3rd_best']['path'][:slash] + '*' + highest_scores[hashtag_label][day]['3rd_best']['path'][slash:-5] + '* ./best/'  + hashtag_label + '/' + day + '/3')

print(str(h_s) + ' ' + nome)
print("")
print("Most popular images are in ./best")
print("")
