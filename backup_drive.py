import json
import requests
from consts.py import HASHTAG_LABELS

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
        addingHistory = addingHistory + Upload_File(auth_token, hashtag + ".zip", folderID, "./" + hashtag + ".zip") + "\n"
   
    history = open("addingHistory.txt", "w+")
    addingHistory = history.read() + addingHistory
    history.write(addingHistory)
    history.close()
     
    Upload_File(auth_token, "addingHistory.txt", folderID, "./addingHistory.txt")
    
def Main():
    auth_token = "ya29.a0AfH6SMBP4Mi1srLgeT43PenJgGPmOFYCnpzguEMly18Fae9egL_i2ngDe_w5kBKWGExZhGVAmBh0MFNCc8VLeNd3TuLlNIF-bQuglXpukrr0wIqRZP_N1yw6U7bjHmPV60yEOHp3t7judiFFJBuFuLfABcMaiT4JJSc"
    folderID = "1UlkoCZ1jjEdPI8CwC2dViBFI-QyUVaK7"
    
    Upload_Hashtags_Zips(HASHTAG_LABELS, auth_token, folderID)

Main()