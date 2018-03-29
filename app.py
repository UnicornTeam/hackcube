#!flask/bin/python

# Author: Ngo Duy Khanh
# Email: ngokhanhit@gmail.com
# Git repository: https://github.com/ngoduykhanh/flask-file-uploader
# This work based on jQuery-File-Upload which can be found at https://github.com/blueimp/jQuery-File-Upload/

import os
import subprocess
import traceback
from subprocess import CalledProcessError

import PIL
import simplejson
from PIL import Image
from flask import Flask, request, render_template, redirect, url_for, send_from_directory
from flask_api import status
from flask_bootstrap import Bootstrap
from flask_cors import CORS

from lib.upload_file import uploadfile

# app = Flask(__name__)
app = Flask('foo')
CORS(app, supports_credentials=True)
app.config['SECRET_KEY'] = 'h\xcb\x81\xaf%\x81\xd5\x02\xc4L\xad,r\x04\xa4*\x8a\xfd\xb6m\\#<\xed'

app.config['THUMBNAIL_FOLDER'] = 'data/thumbnail/'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024
# TODO: Change this to actual path when release production version
app.config['AP_LIST_FILE'] = 'data/source/AP_list_tmp'
app.config['STA_LIST_FILE'] = 'data/source/STA_list_tmp'
app.config['STA_BLOCK_SHELL'] = "/root/monitor_file/STA_block.sh"
app.config['WIFI_SCAN_SHELL'] = "/root/monitor_file/wifi_scan.sh"
app.config['AP_BLOCK_SHELL'] = "/root/monitor_file/AP_block.sh"
app.config['DEBUG'] = False
# app.config['AP_BLOCK_SHELL'] = "data/example-bash/test.sh"

ALLOWED_EXTENSIONS = {'txt', 'gif', 'png', 'jpg', 'jpeg', 'bmp', 'rar', 'zip', '7zip', 'doc', 'docx'}
IGNORED_FILES = {'.gitignore'}

bootstrap = Bootstrap(app)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# TODO: Check whether need change this rule.
# TODO: Decide where the uploaded file should be store.
def gen_file_name(filename):
    """
    If file was exist already, rename it and return a new name
    """
    i = 1
    while os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
        name, extension = os.path.splitext(filename)
        filename = '%s_%s%s' % (name, str(i), extension)
        i += 1

    return filename


def create_thumbnail(image):
    try:
        base_width = 80
        img = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], image))
        w_percent = (base_width / float(img.size[0]))
        h_size = int((float(img.size[1]) * float(w_percent)))
        img = img.resize((base_width, h_size), PIL.Image.ANTIALIAS)
        img.save(os.path.join(app.config['THUMBNAIL_FOLDER'], image))

        return True

    except:
        print(traceback.format_exc())
        return False


# TODO: Fetch ap_list
@app.route("/ap_list", methods=['GET'])
def get_ap_list():
    ap_list = []
    try:
        f = open(app.config['AP_LIST_FILE'])
    except:
        return simplejson.dumps({"ap_list": ap_list}), status.HTTP_500_INTERNAL_SERVER_ERROR
    for line in f.readlines():
        l = line.split()
        if len(l) < 5:
            continue
        i = {
            'BSSID': l[0],
            'RSSI': l[2],
            'SSID': l[3],
            'JAM': False
        }
        ap_list.append(i)
    return simplejson.dumps({"ap_list": ap_list})


@app.route("/sta_list", methods=['GET'])
def get_sta_list():
    sta_list = []
    f = open(app.config['STA_LIST_FILE'])
    for line in f.readlines():
        l = line.split()
        if len(l) < 4:
            print("Too short: ", l)
            continue
        i = {
            'MAC': l[0],
            'RSSI': l[1],
            'BSSID': l[3]
        }
        sta_list.append(i)
    return simplejson.dumps({"sta_list": sta_list})


@app.route("/ap_block/<string:bssid>/<string:action>", methods=['GET'])
def ap_block(bssid, action):
    # print("[ap_block] Receive parameter: ", bssid, action)
    if action not in ['on', 'off']:
        return simplejson.dumps({'status': 'fail',
                                 'action': action,
                                 'api': 'ap_block',
                                 'message': 'Parameter error'}), status.HTTP_400_BAD_REQUEST
    try:
        subprocess.call("{} {} {}".format(app.config['AP_BLOCK_SHELL'], bssid, action), shell=True)
    except CalledProcessError:
        return simplejson.dumps({'status': 'fail',
                                 'action': action,
                                 'api': 'ap_block',
                                 'message': 'Call AP_block process error.'}), status.HTTP_500_INTERNAL_SERVER_ERROR
    return simplejson.dumps({'status': 'success',
                             'action': action,
                             'api': 'ap_block',
                             'message': 'Call AP_block process success.'
                             })


@app.route("/sta_block/<string:mac>/<string:action>")
def sta_block(mac, action):
    if action not in ['on', 'off']:
        return simplejson.dumps({'status': 'fail',
                                 'action': action,
                                 'api': 'sta_block',
                                 'message': 'Parameter error'}), status.HTTP_400_BAD_REQUEST
    try:
        subprocess.call("{} {} {}".format(app.config['STA_BLOCK_SHELL'], mac, action), shell=True)
    except CalledProcessError:
        return simplejson.dumps({'status': 'fail',
                                 'action': action,
                                 'api': 'sta_block',
                                 'message': 'Call STA_block process error.'}), status.HTTP_500_INTERNAL_SERVER_ERROR
    return simplejson.dumps({'status': 'success',
                             'action': action,
                             'api': 'sta_block',
                             'message': 'Call STA_block process success.'
                             })


@app.route("/wifi_scan/<string:action>/<string:channel>", methods=['GET'])
def wifi_scan(action, channel):
    if action not in ['on', 'off']:
        return simplejson.dumps({'status': 'fail',
                                 'message': 'Parameter error'}), status.HTTP_400_BAD_REQUEST
    try:
        subprocess.call("{} {} {}".format(app.config['WIFI_SCAN_SHELL'], action, channel), shell=True)
    except CalledProcessError:
        return simplejson.dumps({'status': 'fail',
                                 'message': 'Call wifi_scan process error.'}), status.HTTP_500_INTERNAL_SERVER_ERROR
    return simplejson.dumps({'status': 'success',
                             'message': 'Call wifi_scan process success.'
                             })


# TODO: Receive more parameter to do more action
# TODO: Decide which kind of filetype will be upload
@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        files = request.files['file']
        extra = None
        try:
            extra = request.form['type']
            print('Extra parameter: ', extra)
        except:
            pass
        if files:
            # TODO: Add test code
            if app.config['DEBUG']:
                app.config['UPLOAD_FOLDER'] = "../data/"
            elif extra:
                if extra == 'HID-Script':
                    app.config['UPLOAD_FOLDER'] = "/root/user_file/HID/"
                elif extra == 'INFO-Pie':
                    app.config['UPLOAD_FOLDER'] = "/root/user_file/raspberrypi"
                elif extra == 'INFO-Ardu':
                    app.config['UPLOAD_FOLDER'] = "/root/user_file/arduino/"
                else:
                    app.config['UPLOAD_FOLDER'] = 'data/'
            else:
                app.config['UPLOAD_FOLDER'] = 'data/'

            # filename = secure_filename(files.filename)
            # filename = gen_file_name(filename)
            filename = files.filename
            uploaded_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            try:
                if os.path.exists(uploaded_file_path):
                    os.remove(uploaded_file_path)
                files.save(uploaded_file_path)
            except IOError as e:
                print(e)
                data = simplejson.dumps({'status': 'fail',
                                         'file': filename,
                                         'save_path': uploaded_file_path,
                                         'api': 'upload',
                                         'message': 'Upload file fail.'
                                         })
                return data, status.HTTP_500_INTERNAL_SERVER_ERROR

            mime_type = files.content_type
            # create thumbnail after saving
            if mime_type.startswith('image'):
                create_thumbnail(filename)

            # get file size after saving
            size = os.path.getsize(uploaded_file_path)

            # return json for js call back
            result = uploadfile(name=filename, type=mime_type, size=size)

            return simplejson.dumps({"files": [result.get_file()]})

    if request.method == 'GET':
        # get all file in ./data directory
        files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if
                 os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], f)) and f not in IGNORED_FILES]

        file_display = []

        for f in files:
            size = os.path.getsize(os.path.join(app.config['UPLOAD_FOLDER'], f))
            file_saved = uploadfile(name=f, size=size)
            file_display.append(file_saved.get_file())

        return simplejson.dumps({"files": file_display})

    return redirect(url_for('index'))


@app.route("/delete/<string:filename>", methods=['DELETE'])
def delete(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file_thumb_path = os.path.join(app.config['THUMBNAIL_FOLDER'], filename)

    if os.path.exists(file_path):
        try:
            os.remove(file_path)

            if os.path.exists(file_thumb_path):
                os.remove(file_thumb_path)

            return simplejson.dumps({filename: 'True'})
        except:
            return simplejson.dumps({filename: 'False'})


# serve static files
@app.route("/thumbnail/<string:filename>", methods=['GET'])
def get_thumbnail(filename):
    return send_from_directory(app.config['THUMBNAIL_FOLDER'], filename=filename)


@app.route("/data/<string:filename>", methods=['GET'])
def get_file(filename):
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER']), filename=filename)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
