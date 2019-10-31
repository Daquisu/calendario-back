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
        if highest_scores_day[classification]['path'] == None:
            return True
        if highest_scores_day[classification]['path'].endswith(ending):
            return False
    return True

for hashtag_label in hashtag_labels:
    arr = os.listdir("./" + hashtag_label + "/")
    for index in range(len(arr)):
        if arr[index].endswith('.json'):
            path = './' + hashtag_label + '/' + arr[index]
            score = calculate_score(path)
            date = get_date(arr[index])
            if date in highest_scores:
                if is_new_image(highest_scores[date], 'path'):
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
                highest_scores[date] = {'best': {'path': path, 'score': score},
                                                 '2nd_best': {'path': None, 'score': 0},
                                                 '3rd_best': {'path': None, 'score': 0}}

os.system('mkdir -p best')
print(highest_scores)
for day in highest_scores:
    os.system('cp ' + highest_scores[day]['best']['path'][:-4] + '* ./best')
    os.system('cp ' + highest_scores[day]['2nd_best']['path'][:-4] + '* ./best')
    os.system('cp ' + highest_scores[day]['3rd_best']['path'][:-4] + '* ./best')