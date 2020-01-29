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
import io
import time
from PIL import Image

def serve_pil_image(pil_img):
    img_io = io.BytesIO()
    pil_img.save(img_io,format = 'JPEG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')

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

def get_day(name):
    return name[:10]

def get_year(day):
    return day[:4]

def same_year_and_month(day1, day2):
    return day1[:7] == day2[:7]

def get_year_and_month(day):
    return day[:7]

def same_date(day1, day2):
    return day1 == day2

def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))

def get_metadata(day_r, hashtag_r, classification_r, f):
    file_f = './best/' + day_r + '/' + hashtag_r + '/' + classification_r + '/' + f
    metadata_dict = {}
    flag_found = False
    with open(file_f) as json_file:
        data = json.load(json_file)
        metadata_dict['owner_username'] = data['node']['owner']['username']
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
        with open(file_f.replace('.json', '.txt')) as txt_file:
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
    t1 = time.time()
    year = get_year(year_and_month)
    # try:
    #     json_path = './' + year + '/' + year_and_month + '.json'
    #     with open(json_path) as text_json:
    #         for line in text_json:

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
                    jpgs = []
                    json = ''
                    for f in os.listdir('./best/' + day + '/' + hashtag + '/' + classification):
                        
                        if f.endswith('.jpg'):
                            jpgs.append(f)
                        if f.endswith('.json'):
                            json = f
                    for f in jpgs:
                        if hashtag[0] == '#':
                            paths[index] = './best/' + day + '/' + 'HASHTAG' + hashtag[1:] + '/' + classification + '/' + f
                            index += 1
                        else:
                            paths.append('./best/' + day + '/' + hashtag + '/' + classification + '/' + f)
                    f = json
                    if f != '':
                        if not hashtag.startswith('top_3'):
                            super_json[day]['images'][hashtag][number_to_str[classification]] = deepcopy(get_metadata(day, hashtag, classification, f))
                            for tag in super_json[day]['images'][hashtag][number_to_str[classification]]['tags']:
                                if tag not in super_json[day]['used_tags']:
                                    super_json[day]['used_tags'].append(tag)
                            super_json[day]['images'][hashtag][number_to_str[classification]]['paths'] = paths
                        else:
                            super_json[day][hashtag][number_to_str[classification]] = deepcopy(get_metadata(day, hashtag, classification, f))
                            super_json[day][hashtag][number_to_str[classification]]['paths'] = paths

                super_json[day]['used_tags'].sort()
    response = jsonify(super_json)
    response.headers.add('Access-Control-Allow-Origin', '*')

    print(time.time()-t1)
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
    # if path.startswith('best/'):
    #     path_wo_slash = path.split('/')
    #     best = path_wo_slash[0]
    #     date = path_wo_slash[1]
    #     hashtag = path_wo_slash[2]
    #     classification = path_wo_slash[3]
    #     f = path_wo_slash[4]
    #     year = get_year(date)
    #     try:
    #         image_number = int(f[-5]) # up to 10 images in albums, so image_number between 0 and 9
    #         f = f.replace('_' + str(image_number) + '.jpg', '.json')
    #     except:
    #         image_number = 0
    #         f = f.replace('.jpg', '.json')
    #     with open('./' + best + '/' + date + '/' + hashtag + '/' + classification + '/' + f) as data:
    #         json_file = json.load(data)
    #         if image_number == 0:
    #             for i in range(len(json_file['node']['display_resources'])):
    #                 if json_file['node']['display_resources'][i]['config_width'] == 640:
    #                     image_url == json_file['node']['display_resources'][i]['src']
    #                     flag_found = True
    #             if not flag_found:
    #                 image_url = = json_file['node']['display_resources'][i]['src']
    #         else: 
    #             for i in range(len(json_file['node']['edge_sidecar_to_children']['edges'][image_number]['node']['display_resources'])):
    #                 if json_file['node']['edge_sidecar_to_children']['edges'][image_number]['node']['display_resources'][i]['config_width'] == 640:
    #                     image_url = = json_file['node']['edge_sidecar_to_children']['edges'][image_number]['node']['display_resources'][i]['src']
    #                     flag_found = True
    #             if not flag_found:
    #                 image_url = = json_file['node']['edge_sidecar_to_children']['edges'][image_number]['node']['display_resources'][i]['src']
    #         local_filename = urllib.urlopen.urlretrieve(image_url)

        # response.headers.add('Access-Control-Allow-Origin', '*')
        # return response
    if path.startswith('best/') or flag:
        img = Image.open(path)
        orig_width = img.size[1]
        if orig_width > 640:
            scale = 640/orig_width
            new_size = (int(i*scale) for i in img.size)
            img = img.resize(new_size, Image.ANTIALIAS)
        response = serve_pil_image(img)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    else:
        return 'Path should start with "/best/"'

@app.route('/hashtags')
def hashtags():
    response = jsonify({'hashtags': HASHTAG_LABELS, 'tags': TAGS})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int("8080"))

