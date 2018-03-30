#!flask/bin/python
# coding=utf-8

# Author: Ngo Duy Khanh
# Email: ngokhanhit@gmail.com
# Git repository: https://github.com/ngoduykhanh/flask-file-uploader
# This work based on jQuery-File-Upload which can be found at https://github.com/blueimp/jQuery-File-Upload/

import os
import hashlib
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
app.config['DEBUG'] = True
app.config['TEST'] = False

if app.config['DEBUG']:
    app.config['AP_LIST_FILE'] = 'data/example_source/AP_list_tmp'
    app.config['STA_LIST_FILE'] = 'data/example_source/STA_list_tmp'
    app.config['NFC_DATA_FILE'] = 'data/example_source/bNFC_data'
    app.config['ARF_DATA_FILE'] = 'data/example_source/aRF_Keeploq_data'
    app.config['CRF_DATA_FILE'] = 'data/example_source/cRF_24l01_data'
    app.config['FIRMWARE_UPDATE_LOG'] = 'data/example_source/update_firmware_log'
    app.config['HD_INFO'] = 'data/example_source/HD_info'
else:
    app.config['AP_LIST_FILE'] = '/root/monitor_file/AP_list_tmp'
    app.config['STA_LIST_FILE'] = '/root/monitor_file/STA_list_tmp'
    app.config['NFC_DATA_FILE'] = '/root/serial_file/data/bNFC_data'
    app.config['RF_DATA_FILE'] = '/root/serial_file/data/aRF_Keeploq_data'
    app.config['CRF_DATA_FILE'] = '/root/serial_file/data/cRF_24l01_data'
    app.config['FIRMWARE_UPDATE_LOG'] = '/root/user_file/INFO/update_firmware_log'
    app.config['HD_INFO'] = '/etc/HD_info'

app.config['STA_BLOCK_SHELL'] = "/root/monitor_file/STA_block.sh"
app.config['WIFI_SCAN_SHELL'] = "/root/monitor_file/wifi_scan.sh"
app.config['AP_BLOCK_SHELL'] = "/root/monitor_file/AP_block.sh"
app.config['SERIAL_SEND_SHELL'] = "/root/serial_files/serial_send.sh"
app.config['UPLOAD_FOLDERS'] = {
    'HID-Script': "/root/user_file/HID/",
    'INFO-Pie': "/root/user_file/raspberrypi",
    'INFO-Ardu': "/root/user_file/arduino/"
}

# app.config['AP_BLOCK_SHELL'] = "data/example-bash/test.sh"

ALLOWED_EXTENSIONS = {'txt', 'gif', 'png', 'jpg', 'jpeg', 'bmp', 'rar', 'zip', '7zip', 'doc', 'docx'}
IGNORED_FILES = {'.gitignore'}

bootstrap = Bootstrap(app)


def file_as_bytes(f):
    with f:
        return f.read()


app.config['MD5'] = hashlib.md5(file_as_bytes(open(app.config['NFC_DATA_FILE'], 'rb'))).hexdigest()


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


# TODO: Deal with 304 in Front_End
@app.route("/nfc_item", methods=['GET'])
def get_nfc_item():
    nfc_item = {}
    now_md5 = hashlib.md5(file_as_bytes(open(app.config['NFC_DATA_FILE'], 'rb'))).hexdigest()
    if now_md5 == app.config['MD5']:
        return simplejson.dumps({'status': 'success',
                                 'api': 'get_nfc_item',
                                 'parameter': None,
                                 'message': 'Call get_nfc_item success.There is no new NFC item',
                                 'nfc_item': nfc_item,
                                 'data_key': 'nfc_item'
                                 }), status.HTTP_304_NOT_MODIFIED
    app.config['MD5'] = now_md5
    f = open(app.config['NFC_DATA_FILE'])
    lines = f.readlines()
    while lines[-1].strip() == '':
        del lines[-1]
    if not lines:
        return simplejson.dumps({"nfc_item": None}), status.HTTP_404_NOT_FOUND
    else:
        id = lines[-1]
        vid = '050'
        # todo: 和前端[RF]data的items不匹配
        nfc_item = {
            'ID': id,
            'VID': vid
        }
        return simplejson.dumps({'status': 'success',
                                 'api': 'get_nfc_item',
                                 'parameter': None,
                                 'message': 'Call get_nfc_item success.',
                                 'nfc_item': nfc_item,
                                 'data_key': 'nfc_item'
                                 })


@app.route("/rf_item/<string:msg_type>", methods=['GET'])
def get_rf_item(msg_type):
    rf_item = {}
    if msg_type == 'arf':
        new_MD5 = hashlib.md5(file_as_bytes(open(app.config['ARF_DATA_FILE'], 'rb'))).hexdigest()
        is_change = new_MD5 != app.config['ARF_MD5']
        app.config['ARF_MD5'] = new_MD5 if is_change else app.config['ARF_MD5']
        f = open(app.config['ARF_DATA_FILE'])
    elif msg_type == 'crf':
        new_MD5 = hashlib.md5(file_as_bytes(open(app.config['CRF_DATA_FILE'], 'rb'))).hexdigest()
        is_change = new_MD5 != app.config['CRF_MD5']
        app.config['CRF_MD5'] = new_MD5 if is_change else app.config['CRF_MD5']
        f = open(app.config['CRF_DATA_FILE'])
    else:
        return simplejson.dumps({'status': 'fail',
                                 'api': 'get_rf_item',
                                 'parameter': msg_type,
                                 'message': 'Call get_rf_item fail.',
                                 'rf_item': rf_item,
                                 'data_key': 'rf_item'
                                 }), status.HTTP_400_BAD_REQUEST

    key = msg_type + "_item"
    if not is_change:
        return simplejson.dumps({key: None, 'key': key}), status.HTTP_304_NOT_MODIFIED

    lines = f.readlines()
    while lines[-1].strip() == '':
        del lines[-1]
    if not lines:
        return simplejson.dumps({'status': 'fail',
                                 'api': 'get_rf_item',
                                 'parameter': msg_type,
                                 'message': 'Call get_rf_item fail.Item not exist.',
                                 'rf_item': rf_item,
                                 'data_key': 'rf_item'
                                 }), status.HTTP_404_NOT_FOUND

    # TODO: Get Vid and ID from file then response it
    # todo: 和前端[RF]data的items不匹配
    s = lines[-1].split(';')
    if len(s) != 4:
        return simplejson.dumps({key: None, 'key': key}), status.HTTP_404_NOT_FOUND
    rf_item = {
        u'频率': s[0].split(':')[-1],
        u'协议': s[1].split(':')[-1],
        u'调制': s[2].split(':')[-1],
        u'数据': s[3].split(':')[-1],
        u'重放': False,
        u'msg_type': msg_type
    }
    return simplejson.dumps({'status': 'success',
                             'api': 'get_rf_item',
                             'parameter': msg_type,
                             'message': 'Call get_rf_item success.',
                             'rf_item': rf_item,
                             'data_key': 'rf_item'
                             })


@app.route("/ap_list", methods=['GET'])
def get_ap_list():
    ap_list = []
    try:
        f = open(app.config['AP_LIST_FILE'])
    except IOError as e:
        return simplejson.dumps({'status': 'fail',
                                 'api': 'ap_list',
                                 'parameter': None,
                                 'message': 'Call ap_list fail.',
                                 'ap_list': ap_list,
                                 'data_key': 'ap_list'
                                 }), status.HTTP_500_INTERNAL_SERVER_ERROR
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
    return simplejson.dumps({'status': 'success',
                             'api': 'ap_list',
                             'parameter': None,
                             'message': 'Call ap_list success.',
                             'ap_list': ap_list,
                             'data_key': 'ap_list'
                             })


@app.route("/sta_list", methods=['GET'])
def get_sta_list():
    sta_list = []
    try:
        f = open(app.config['STA_LIST_FILE'])
    except IOError as e:
        print(e)
        return simplejson.dumps({'status': 'fail',
                                 'api': 'sta_list',
                                 'parameter': app.config['STA_LIST_FILE'],
                                 'message': 'Call sta_list error.File not found.',
                                 'sta_list': sta_list,
                                 'data_key': 'sta_list'
                                 }), status.HTTP_500_INTERNAL_SERVER_ERROR

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
    return simplejson.dumps({'status': 'success',
                             'api': 'sta_list',
                             'parameter': None,
                             'message': 'Call sta_list success.',
                             'sta_list': sta_list,
                             'data_key': 'sta_list'
                             })


@app.route("/ap_block/<string:bssid>/<string:action>", methods=['GET'])
def ap_block(bssid, action):
    # print("[ap_block] Receive parameter: ", bssid, action)
    if action not in ['on', 'off']:
        return simplejson.dumps({'status': 'fail',
                                 'api': 'ap_block',
                                 'parameter': [bssid, action],
                                 'message': 'Call AP_block fail, parameter error',
                                 'data_key': None
                                 }), status.HTTP_400_BAD_REQUEST
    try:
        subprocess.call("{} {} {}".format(app.config['AP_BLOCK_SHELL'], bssid, action), shell=True)
    except CalledProcessError:
        return simplejson.dumps({'status': 'fail',
                                 'api': 'ap_block',
                                 'parameter': [bssid, action],
                                 'message': 'Call AP_block error.',
                                 'data_key': None
                                 }), status.HTTP_500_INTERNAL_SERVER_ERROR
    return simplejson.dumps({'status': 'success',
                             'api': 'ap_block',
                             'parameter': [bssid, action],
                             'message': 'Call AP_block success.',
                             'data_key': None
                             })


@app.route("/sta_block/<string:mac>/<string:action>")
def sta_block(mac, action):
    if action not in ['on', 'off']:
        return simplejson.dumps({'status': 'fail',
                                 'api': 'sta_block',
                                 'parameter': [mac, action],
                                 'message': 'Call STA_block fail, parameter error',
                                 'data_key': None
                                 }), status.HTTP_400_BAD_REQUEST
    try:
        subprocess.call("{} {} {}".format(app.config['STA_BLOCK_SHELL'], mac, action), shell=True)
    except CalledProcessError:
        return simplejson.dumps({'status': 'fail',
                                 'api': 'sta_block',
                                 'parameter': [mac, action],
                                 'message': 'Call STA_block error.',
                                 'data_key': None
                                 }), status.HTTP_500_INTERNAL_SERVER_ERROR
    return simplejson.dumps({'status': 'success',
                             'api': 'sta_block',
                             'parameter': [mac, action],
                             'message': 'Call STA_block success.'
                             })


@app.route("/wifi_scan/<string:action>/<string:channel>", methods=['GET'])
def wifi_scan(action, channel):
    if action not in ['on', 'off']:
        return simplejson.dumps({'status': 'fail',
                                 'api': 'wifi_scan',
                                 'parameter': [action, channel],
                                 'message': 'Call wifi_scan fail, parameter error',
                                 'data_key': None
                                 }), status.HTTP_400_BAD_REQUEST
    try:
        subprocess.call("{} {} {}".format(app.config['WIFI_SCAN_SHELL'], action, channel), shell=True)
    except CalledProcessError:
        return simplejson.dumps({'status': 'fail',
                                 'api': 'wifi_scan',
                                 'parameter': [action, channel],
                                 'message': 'Call wifi_scan error.',
                                 'data_key': None
                                 }), status.HTTP_500_INTERNAL_SERVER_ERROR
    return simplejson.dumps({'status': 'success',
                             'api': 'wifi_scan',
                             'parameter': [action, channel],
                             'message': 'Call wifi_scan success.',
                             'data_key': None
                             })


@app.route("/serial_send/<string:parameter>", methods=['GET'])
def serial_send(parameter):
    if parameter[:2] not in ['ns', 'nw']:
        return simplejson.dumps({'status': 'fail',
                                 'api': 'serial_send',
                                 'parameter': parameter,
                                 'message': 'Call serial_send fail, parameter error',
                                 'data_key': None
                                 }), status.HTTP_400_BAD_REQUEST
    try:
        subprocess.call("{} {}".format(app.config['SERIAL_SEND_SHELL'], parameter), shell=True)
    except CalledProcessError:
        return simplejson.dumps({'status': 'fail',
                                 'api': 'serial_send',
                                 'parameter': parameter,
                                 'message': 'Call serial_send error.',
                                 'data_key': None
                                 }), status.HTTP_500_INTERNAL_SERVER_ERROR
    return simplejson.dumps({'status': 'success',
                             'api': 'serial_send',
                             'parameter': parameter,
                             'message': 'Call serial_send success.',
                             'data_key': None
                             })


@app.route("update_firmware/<string:uploaded_file_path>", methods=['GET'])
def update_firmware(uploaded_file_path):
    if not update_firmware:
        return simplejson.dumps({'status': 'fail',
                                 'api': 'update_firmware',
                                 'parameter': uploaded_file_path,
                                 'message': 'Call update_firmware fail, parameter error',
                                 'data_key': None
                                 }), status.HTTP_400_BAD_REQUEST

    try:
        subprocess.call("{} {}".format(app.config['UPDATE_FIRMWARE_SHELL'], uploaded_file_path), shell=True)
    except CalledProcessError:
        return simplejson.dumps({'status': 'fail',
                                 'api': 'update_firmware',
                                 'parameter': uploaded_file_path,
                                 'message': 'Call update_firmware fail',
                                 'data_key': None
                                 }), status.HTTP_500_INTERNAL_SERVER_ERROR
    return simplejson.dumps({'status': 'success',
                             'api': 'update_firmware',
                             'parameter': uploaded_file_path,
                             'message': 'Call update_firmware success',
                             'data_key': None
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
            if extra is None:
                app.config['UPLOAD_FOLDER'] = "data/"
            elif app.config['TEST']:
                app.config['UPLOAD_FOLDER'] = "../data/"
            elif app.config['DEBUG']:
                app.config['UPLOAD_FOLDER'] = "data/"
            elif extra not in app.config['UPLOAD_FOLDERS']:
                app.config['UPLOAD_FOLDER'] = "data/"
            else:
                app.config['UPLOAD_FOLDER'] = app.config['UPLOAD_FOLDERS'][extra]

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
                                         'api': 'upload',
                                         'parameter': filename,
                                         'message': 'Upload file fail.Error raise while save file.',
                                         'data_key': None
                                         })
                return data, status.HTTP_500_INTERNAL_SERVER_ERROR

            mime_type = files.content_type
            # create thumbnail after saving
            # if mime_type.startswith('image'):
            #     create_thumbnail(filename)

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
