import zipfile
import os
from flask import send_file
from flask import Flask

def same_year_and_month(day1, day2):
    return day1[:7] == day2[:7]

def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))

app = Flask(__name__)


@app.route('/download_month/<year_and_month>')
def download_month(year_and_month):
    zipname = year_and_month + '.zip'
    with zipfile.ZipFile(zipname, 'w', zipfile.ZIP_DEFLATED) as zipf:
#    zipf = zipfile.ZipFile(year_and_month + '.zip', 'w')
        for folder in os.listdir('./best'):
           if same_year_and_month(folder, year_and_month):
               zipdir('./best/' + folder, zipf)
#    zipf.close()
    return send_file(zipname,
                     mimetype = 'zip',
                     attachment_filename = zipname,
                     as_attachment = True)
