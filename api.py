import zipfile
import os
from flask import send_file
from flask import Flask
from flask import jsonify
from flask import request, send_from_directory
from flask_cors import CORS, cross_origin
import json
import copy
from consts import HASHTAG_LABELS
from consts import TAGS

def get_day(name):
    return name[:10]

def same_year_and_month(day1, day2):
    return day1[:7] == day2[:7]

def same_date(day1, day2):
    return day1 == day2

def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))

def get_metadata(day_r, hashtag_r, classification_r, f):
    file = './best/' + day_r + '/' + hashtag_r + '/' + classification_r + '/' + f
    metadata_dict = {}
    flag_found = False
    with open(file) as json_file:
        data = json.load(json_file)
        metadata_dict['owner_username'] = data['node']['owner']['username']
        # metadata_dict['caption_hashtags'] = data.caption_hashtags
        metadata_dict['likes'] = data['node']['edge_liked_by']['count']
        metadata_dict['comments'] = data['node']['edge_media_preview_comment']['count']
        for i in range(len(data['node']['display_resources'])):
            if data['node']['display_resources'][i]['config_width'] == 640:
                metadata_dict['display_url'] = data['node']['display_resources'][i]['src']
                flag_found = True
        if not flag_found:
            metadata_dict['display_url'] = data['node']['display_resources'][i]['src']
        metadata_dict['thumbnail_resources'] = data['node']['thumbnail_resources']
    metadata_dict['hashtags'] = [hashtag_r]
    metadata_dict['tags'] = []
    metadata_dict['caption'] = ''
    if f.replace('json', 'txt') in os.listdir('./best/' + day_r + '/' + hashtag_r + '/' + classification_r + '/'):
        with open(file.replace('.json', '.txt')) as txt_file:
            for line in txt_file:
                for hashtag in HASHTAG_LABELS:
                    if hashtag not in metadata_dict['hashtags'] and hashtag[1:] in line.lower():
                        metadata_dict['hashtags'].append(hashtag)
                for tag in TAGS:
                    if tag not in metadata_dict['tags'] and tag in line.lower():
                        metadata_dict['tags'].append(tag)
                        metadata_dict['caption'] += line

    return metadata_dict

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
@app.route('/download_month/<year_and_month>')
def download_month(year_and_month):
    number_to_str = {'1': 'best', '2': '2nd_best', '3': '3rd_best'}
    super_json = {}
    for day in os.listdir('./best'):
        if same_year_and_month(day, year_and_month):
            super_json[day] = {}
            super_json[day]['images'] = {}
            super_json[day]['used_tags'] = []
            index = 0
            for hashtag in sorted(os.listdir('./best/' + day)):
                if hashtag == 'top_3':
                    super_json[day][hashtag] = {}
                else:
                    super_json[day]['images'][hashtag] = {}
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
                                super_json[day]['images'][hashtag][number_to_str[classification]] = copy.deepcopy(get_metadata(day, hashtag, classification, f))
                                for tag in super_json[day]['images'][hashtag][number_to_str[classification]]['tags']:
                                    if tag not in super_json[day]['used_tags']:
                                        super_json[day]['used_tags'].append(tag)
                                super_json[day]['images'][hashtag][number_to_str[classification]]['paths'] = paths
                            else:
                                super_json[day][hashtag][number_to_str[classification]] = copy.deepcopy(get_metadata(day, hashtag, classification, f))
                                super_json[day][hashtag][number_to_str[classification]]['paths'] = paths
                super_json[day]['used_tags'].sort()
    response = jsonify(super_json)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/download_full_month/<year_and_month>')
def download_full_month(year_and_month):
    super_json = {}
    hashtags = HASHTAG_LABELS[:]
    for hashtag in ['#coleraalegria_eleicoes', '#desenhospelademocracia_eleicoes', '#designativista_eleicoes', '#mariellepresente_eleicoes', '#elenao_eleicoes']:
        hashtags.append(hashtag)
    for hashtag in hashtags:
        for path in os.listdir('./' + hashtag + '/'):
            day = get_day(path)
            if (day not in super_json) & same_year_and_month(day, year_and_month):
                super_json[day] = {}
            if day in super_json:
                if hashtag not in super_json[day]:
                    super_json[day][hashtag] = []

            if path.endswith('.jpg') & same_year_and_month(day, year_and_month):
                new_path = './' + hashtag + '/' + path
                new_path = new_path.replace('#', 'HASHTAG')
                super_json[day][hashtag].append(new_path)
                
    response = jsonify(super_json)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

#@app.route('/', defaults={'path': ''})
@app.route('/get_image/<path:path>')
def get_image(path):
    path = path.replace('HASHTAG', '#')
    flag = False
    for hashtag in HASHTAG_LABELS:
        if path.startswith(hashtag):
            flag = True
    if path.startswith('best/') or flag:
        response = send_file(path, mimetype='image')
        response.headers.add('Access-Control-Allow-Origin', '*')
        return send_file(path, mimetype='image')
    else:
        return 'Path should start with "/best/"'

@app.route('/hashtags')
def hashtags():
    response = jsonify({'hashtags': HASHTAG_LABELS, 'tags': TAGS})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response