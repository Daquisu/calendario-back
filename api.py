import zipfile
import os
from flask import send_file
from flask import Flask

def same_year_and_month(day1, day2):
    return day1[:7] == day2[:7]

app = Flask(__name__)

@app.route('/')

@app.route('/download_month')

@app.route('/download_month/<year_and_month>')
def download_month(year_and_month):
    return 'Oi'
    zipname = year_and_month + '.zip'
#    with zipfile.ZipFile(zipname, 'w') as zipf:
    zipf = zipfile.ZipFile(year_and_month + '.zip', 'w')
    for folder in os.listdir('./best'):
       if same_year_and_month(folder, year_and_month):
           zipf.write(folder)
    zipf.close()
    return send_file(zipname,
                     mimetype = 'zip',
                     attachment_filename = zipname,
                     as_attachment = True)
