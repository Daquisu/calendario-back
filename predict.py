from keras.models import load_model
from keras.preprocessing import image
from sklearn.metrics import classification_report, confusion_matrix
from keras.models import load_model
import os
import numpy as np

hashtag_label = '#mariellepresente'
# ['#coleraalegria_eleicoes', '#desenhospelademocracia_eleicoes', '#designativista_eleicoes', '#elenao_eleicoes', '#mariellepresente_eleicoes']
for hashtag_label in ['top_6_diario_2020']:
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
        X_test = []
        image_index_list = []
        renewed_arr = os.listdir("./" + hashtag_label + "/")
        print(len(arr))
        for index in range(j, len(arr), n_div):
            if arr[index].endswith('.jpg') and arr[index] in renewed_arr:
                im = image.load_img("./" + hashtag_label + '/' + arr[index], target_size=(120,120,1), grayscale=False)
                im = image.img_to_array(im)
                im = im/255
                X_test.append(im)
                image_index_list.append(index)

        X_test = np.array(X_test)

        print("")
        print("##################")
        print("Predicting")
        print("##################")
        print("")

        model = load_model('./models/aprimorado.h5')
        y_pred = model.predict_classes(X_test)

        print("")
        print("##################")
        print("Renaming files")
        print("##################")
        print("")

        cat = ''
        for img in range(len(y_pred)):
            if y_pred[img] == 1:
                cat = "ID"

            if y_pred[img] == 2:
                cat = "F"

            if y_pred[img] == 3:
                cat = "IM"

            if y_pred[img] == 4:
                cat = "TD"

            # if y_pred[img] == 5:
            #     cat = "TV"

            #os.system('mv /home/daquisu/projects/calendario-back/' + hashtag_label + '/' + arr[image_index_list[img]][:-6] + '*' + ' /home/daquisu/projects/calendario-back/' + hashtag_label + '/' + cat + '/')
            os.system('mv /home/daquisu/projects/calendario-back/' + hashtag_label + '/' + arr[image_index_list[img]] + ' /home/daquisu/projects/calendario-back/' + hashtag_label + '/' + cat + '/')
