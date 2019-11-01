from keras.models import load_model
from keras.preprocessing import image
from sklearn.metrics import classification_report, confusion_matrix
from keras.models import load_model
import os
import numpy as np

hashtag_label = '#mariellepresente'
arr = os.listdir("./" + hashtag_label + "/")

X_test = []

print("##################")
print("Making predict data")
print("##################")
print("")

image_index_list = []
for index in range(len(arr)):
    if arr[index].endswith('.jpg'):
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

model = load_model('./models/0.8732057416267942_1568206179.5820658.h5')
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

    os.system('mv /home/daquisu/projects/calendario-back/' + hashtag_label + '/' + arr[image_index_list[img]][:23] + '.*' + ' /home/daquisu/projects/calendario-back/' + hashtag_label + '/' + cat + '/')
