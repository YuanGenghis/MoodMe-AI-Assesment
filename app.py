from email.mime import base
from multiprocessing.connection import wait
import sys,os,re,glob,base64,io
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename
from config import *
from PIL import Image


app=Flask(__name__, 
            static_url_path='', # removes path prefix requirement */templates/static
            static_folder='templates/static',# static file location
            template_folder='templates' # template file location
            )
app.secret_key = app_key
app.config['MAX_CONTENT_LENGTH'] = file_mb_max * 1024 * 1024

# Check that the upload folder exists
def makedir (dest):
    fullpath = '%s/%s'%(upload_dest,dest)
    if not os.path.isdir(fullpath):
        os.mkdir(fullpath)

makedir('')# make uploads folder

## on page load display the upload file
@app.route('/upload')
def upload_form():
    flash('Drag files to upload here.')
    return render_template('upload.html')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in extensions

## on a POST request of data 
@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':

        if not os.path.isdir(upload_dest):
            os.mkdir(upload_dest)

    if 'files[]' not in request.files:
            flash('No files found, try again.')
            return redirect(request.url)
    files = request.files.getlist('files[]')
    for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join( upload_dest, filename))
    flash('File(s) uploaded')

    os.system('python gad.py --image ' + 'uploads_folder/' + filename)

    img = Image.open(os.path.join(os.getcwd(), 'uploads_folder') + "/" + filename)
    data = io.BytesIO()
    img.save(data, "JPEG")

    encode_img = base64.b64encode(data.getvalue())

    return render_template("upload.html", filename=encode_img.decode("UTF-8"))




if __name__ == "__main__":
    print('to upload files navigate to http://127.0.0.1:4000/upload')
    # lets run this on localhost port 4000
    app.run(host='127.0.0.1',port=4000,debug=True,threaded=True)