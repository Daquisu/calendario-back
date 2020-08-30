import json
import requests
from consts import HASHTAG_LABELS

#Function to upload a file to google Drive
def Upload_File(auth_token, name, folderID, relat_path):

    headers = {"Authorization": "Bearer " + auth_token} #token gotten from drive api at google developers
    para = {
        "name": name,       #name to be given to the file in drive
        "parents": [folderID] #id of the folder where the file will be put into
    }
    files = {
        'data': ('metadata', json.dumps(para), 'application/json; charset=UTF-8'),
        'file': open(relat_path, "rb") #relative path of the file. Ex: ./#coleraalegria
    }
    requests.post(
        "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
        headers=headers,
        files=files
    )
    
    print("Added: " + name)
    
    return name #return the name for the purpose of registering the addings

#Function to upload all the zip files based on the hashtags
def Upload_Hashtags_Zips(HASHTAG_LABELS, auth_token, folderID):
    
    addingHistory = ""
    for hashtag in HASHTAG_LABELS:
        addingHistory = addingHistory + Upload_File(auth_token, hashtag + "ZIP.zip", folderID, "./" + hashtag + "ZIP.zip") + "\n"
   
    history = open("addingHistory.txt", "w+")
    addingHistory = history.read() + addingHistory
    history.write(addingHistory)
    history.close()
     
    Upload_File(auth_token, "addingHistory.txt", folderID, "./addingHistory.txt")
    
def Main():
    print("Google Drive Backup Process initialized...")
    print("Please wait...")
    auth_token = "ya29.a0AfH6SMAvz326QKrPpr7-lSpqMGRBURdzGMPa8_g_87ERpIy7q2M5Obc1y31BS-4Krj-ZbkI1Si5WByw3iwEfLZk3qtxwgLzMB7B6he_jRJ99a3fBcZpArDFv2kNW7xjXmZ1EfVsZG9oxGdpG8qXBt3v-MqgTabGBEKk"
    folderID = "1UlkoCZ1jjEdPI8CwC2dViBFI-QyUVaK7"
    
    Upload_Hashtags_Zips(HASHTAG_LABELS, auth_token, folderID)

Main()