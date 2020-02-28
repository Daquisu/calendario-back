from keras.models import load_model
from keras.preprocessing import image
from sklearn.metrics import classification_report, confusion_matrix
import os
import numpy as np
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
import time

def slicer_vectorized(a,start,end):
    b = a.view((str,1)).reshape(len(a),-1)[:,start:end]
    return np.frombuffer(b.tostring(),dtype=(str,end-start))

model = load_model('./models/0.8732057416267942_1568206179.5820658.h5')
# ['#coleraalegria_eleicoes', '#desenhospelademocracia_eleicoes', '#designativista_eleicoes', '#elenao_eleicoes', '#mariellepresente_eleicoes']
for hashtag_label in ['#elenao_eleicoes']:
    arr = os.listdir("./" + hashtag_label + "/")
    os.system('mkdir \\' + hashtag_label + '/ID')
    os.system('mkdir \\' + hashtag_label + '/F')
    os.system('mkdir \\' + hashtag_label + '/IM')
    os.system('mkdir \\' + hashtag_label + '/TD')


    print("##################")
    print("Making predict data")
    print("##################")
    print("")

    n_div = 1
    for j in range(n_div):
        t1 = time.time()
        print(str(j) + ' of ' + str(n_div))
        X_test = []
        image_index_list = []
        renewed_arr = os.listdir("./" + hashtag_label + "/")
        print(len(arr))
        for index in range(j, len(arr), n_div):
            if arr[index].endswith('.jpg') and arr[index] in renewed_arr:
                try:
                    im = image.load_img("./" + hashtag_label + '/' + arr[index], target_size=(120,120,1), grayscale=False)
                    im = image.img_to_array(im)
                    im = im/255
                    X_test.append(im)
                    image_index_list.append(index)
                except IOError as err:
                    print(err)
                    print(arr[index])
                    pass
                except OSError as err:
                    print(err)
                    print(arr[index])
                    pass

        X_test = np.array(X_test)

        print("")
        print("##################")
        print("Predicting")
        print("##################")
        print("")

        y_pred = model.predict_classes(X_test)

        print("")
        print("##################")
        print("Renaming files")
        print("##################")
        print("")

        cat = {1: 'ID', 2: 'F', 3: 'IM', 4: 'TD'}
        for classification in range(1, 5):
            if True in (y_pred == classification):
                print('True: ' + cat[classification])
                image_names = np.array(arr)[image_index_list][y_pred==classification] # image names with the same classification
                image_names = slicer_vectorized(image_names,0,19) # slicing [:19] for every image name, so 'YYYY-MM-DD_hh-mm-ss'
                image_names = np.char.add(image_names, '* ') # concatenating '* ' at the end for every image name
                # print(''.join(image_names))
                # directory = '/home/daquisu/projects/calendario-back/' + hashtag_label + '/' # where images are
                directory = './' + hashtag_label + '/' # where images are
                image_names = np.char.add(directory, image_names) # concatenating directory at the beginning for every image name
                image_names = ''.join(image_names) # string with every image name. will be used with mv
                os.system('mv ' + image_names + '-t ' + directory + cat[classification] + '/')
        # cat = ''
        # for img in range(len(y_pred)):
        #     if y_pred[img] == 1:
        #         cat = "ID"

        #     if y_pred[img] == 2:
        #         cat = "F"

        #     if y_pred[img] == 3:
        #         cat = "IM"

        #     if y_pred[img] == 4:
        #         cat = "TD"

        #     # if y_pred[img] == 5:
        #     #     cat = "TV"

        #     os.system('mv /home/daquisu/projects/calendario-back/' + hashtag_label + '/' + arr[image_index_list[img]][:-7] + '*' + ' /home/daquisu/projects/calendario-back/' + hashtag_label + '/' + cat + '/')

        print('Time for last iteration: ' + str(time.time()-t1))
