import json
import requests
from consts import HASHTAG_LABELS, folderID

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
    
    for hashtag in HASHTAG_LABELS:
        upfile = Upload_File(auth_token, hashtag + "ZIP.zip", folderID, "./" + hashtag + "ZIP.zip")
        print(f"File uploaded to drive: {upfile}")
    
    
def Main():
    auth_token = input("Please paste here the access token: \n")
    
    print("Google Drive Backup Process initialized...")
    print("Please wait...")
    
    Upload_Hashtags_Zips(HASHTAG_LABELS, auth_token, folderID)
    
    print("Backup finished.")

Main()