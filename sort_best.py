import json
import os

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
        if highest_scores_day[classification]['path'] != None:
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
    arr = os.listdir("./" + hashtag_label + "/")
    for index in range(len(arr)):
        if arr[index].endswith('.json'):
            path = './' + hashtag_label + '/' + arr[index]
            score = calculate_score(path)
            date = get_date(arr[index])
            if date in highest_scores:
                if is_new_image(highest_scores[date], arr[index]):
                    if score > highest_scores[date]['best']['score']:
                        highest_scores[date]['3rd_best'] = highest_scores[date]['2nd_best']
                        highest_scores[date]['2nd_best'] = highest_scores[date]['best']
                        highest_scores[date]['best']['path'] = path
                        highest_scores[date]['best']['score'] = score
                    elif score > highest_scores[date]['2nd_best']['score']:
                        highest_scores[date]['3rd_best'] = highest_scores[date]['2nd_best']
                        highest_scores[date]['2nd_best']['path'] = path
                        highest_scores[date]['2nd_best']['score'] = score
                    elif score > highest_scores[date]['3rd_best']['score']:
                        highest_scores[date]['3rd_best']['path'] = path
                        highest_scores[date]['3rd_best']['score'] = score
                else:
                    print(highest_scores[date], arr[index])
            else:
                highest_scores[date] = {'best':     {'path': path, 'score': score},
                                        '2nd_best': {'path': None, 'score': 0},
                                        '3rd_best': {'path': None, 'score': 0}}
os.system('mkdir -p best')
print("")
print("##################")
print("Copying best images from each day")
print("##################")
print("")
h_s = 0
nome = ''
for day in highest_scores:
    if highest_scores[day]['best']['score'] > h_s:
        h_s = highest_scores[day]['best']['score']
        nome = highest_scores[day]['best']['path']
    os.system('mkdir -p best/' + day + '/1')
    os.system('mkdir -p best/' + day + '/2')
    os.system('mkdir -p best/' + day + '/3')
    slash = find_index_second_slash(highest_scores[day]['best']['path'])
    os.system('cp ' + highest_scores[day]['best']['path'][:slash] + '*' + highest_scores[day]['best']['path'][slash:-5] + '* ./best/' + day + '/1')
    slash = find_index_second_slash(highest_scores[day]['2nd_best']['path'])
    os.system('cp ' + highest_scores[day]['2nd_best']['path'][:slash] + '*' + highest_scores[day]['2nd_best']['path'][slash:-5] + '* ./best/' + day + '/2')
    slash = find_index_second_slash(highest_scores[day]['3rd_best']['path'])
    os.system('cp ' + highest_scores[day]['3rd_best']['path'][:slash] + '*' + highest_scores[day]['3rd_best']['path'][slash:-5] + '* ./best/'  + day + '/3')

print(str(h_s) + ' ' + nome)
print("")
print("Most popular images are in ./best")
print("")
