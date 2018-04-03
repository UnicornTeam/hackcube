#!flask/bin/python
# coding=utf-8

# Author: Anderson
# Email: liuhongda@360.cn
# Git repository: https://github.com/peacesky/flask-file-uploader.git
# This work based on jQuery-File-Upload which can be found at https://github.com/blueimp/jQuery-File-Upload/

import os
import hashlib
import subprocess
from subprocess import CalledProcessError

import simplejson
from flask import Flask, request, render_template, redirect, url_for, send_from_directory
from flask_api import status
from flask_bootstrap import Bootstrap
from flask_cors import CORS

from config.bcolor import bcolors
from config.config import DevelopmentConfig, TestingConfig, ProductionConfig
from lib.upload_file import uploadfile

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config['DEBUG'] = True
app.config['TEST'] = False

if app.config['DEBUG']:
    app.config.from_object(DevelopmentConfig)
elif app.config['TESTING']:
    app.config.from_object(TestingConfig)
else:
    app.config.from_object(ProductionConfig)

ALLOWED_EXTENSIONS = {'txt', 'gif', 'png', 'jpg', 'jpeg', 'bmp', 'rar', 'zip', '7zip', 'doc', 'docx'}
IGNORED_FILES = {'.gitignore'}

bootstrap = Bootstrap(app)


def file_as_bytes(f):
    with f:
        return f.read()


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/nfc_item", methods=['GET'])
def get_nfc_item():
    nfc_item = {}
    file_path = app.config['NFC_DATA_FILE']
    if not os.path.exists(file_path):
        return simplejson.dumps({'status': 'fail',
                                 'api': 'nfc_item',
                                 'parameter': None,
                                 'message': 'Get nfc_item fail.FILE NOT FOUND',
                                 'nfc_item': nfc_item,
                                 'data_key': 'nfc_item'
                                 }), status.HTTP_404_NOT_FOUND
    with open(file_path, 'rb') as f:
        now_md5 = hashlib.md5(file_as_bytes(f)).hexdigest()
    if now_md5 == app.config['NFC_DATA_FILE_MD5']:
        return simplejson.dumps({'status': 'success',
                                 'api': 'nfc_item',
                                 'parameter': None,
                                 'message': 'Get nfc_item success.But no new NFC item',
                                 'nfc_item': nfc_item,
                                 'data_key': 'nfc_item'
                                 }), status.HTTP_304_NOT_MODIFIED
    app.config['NFC_DATA_FILE_MD5'] = now_md5
    with open(file_path, 'r') as f:
        lines = f.readlines()
    while lines[-1].strip() == '':
        del lines[-1]
    if not lines:
        return simplejson.dumps({'status': 'fail',
                                 'api': 'nfc_item',
                                 'parameter': None,
                                 'message': 'Get nfc_item fail.Item NOT FOUND',
                                 'nfc_item': nfc_item,
                                 'data_key': 'nfc_item'
                                 }), status.HTTP_404_NOT_FOUND
    else:
        id = lines[-1]
        vid = '050'
        nfc_item = {
            'ID': id,
            'VID': vid,
            'WRITE': False,
            'SIMULATE': False
        }
        return simplejson.dumps({'status': 'success',
                                 'api': 'nfc_item',
                                 'parameter': None,
                                 'message': 'Get nfc_item success.',
                                 'nfc_item': nfc_item,
                                 'data_key': 'nfc_item'
                                 })


@app.route("/all_rf_item/<string:msg_type>", methods=['GET'])
def get_all_rf_item(msg_type):
    result_items = []
    data_key = msg_type + "_item"
    if msg_type == 'arf':
        file_path = app.config['ARF_DATA_FILE']
    elif msg_type == 'crf':
        file_path = app.config['CRF_DATA_FILE']
    else:
        return simplejson.dumps({'status': 'fail',
                                 'api': 'all_rf_item',
                                 'parameter': msg_type,
                                 'message': 'Get all_rf_item fail.parameter msg_type error.',
                                 data_key: result_items,
                                 'data_key': data_key
                                 }), status.HTTP_400_BAD_REQUEST

    with open(file_path, 'r') as f:
        lines = f.readlines()
    while lines and not lines[-1].strip():
        del lines[-1]
    if not lines:
        return simplejson.dumps({'status': 'fail',
                                 'api': 'all_rf_item',
                                 'parameter': msg_type,
                                 'message': 'Get all_rf_item fail.Item not exist.',
                                 data_key: result_items,
                                 'data_key': data_key
                                 }), status.HTTP_404_NOT_FOUND

    for line in lines:
        s = line.split(';')
        if len(s) != 4:
            return simplejson.dumps({'status': 'fail',
                                     'api': 'all_rf_item',
                                     'parameter': msg_type,
                                     'message': 'Get all_rf_item fail.Item format error.',
                                     data_key: result_items,
                                     'data_key': data_key
                                     }), status.HTTP_404_NOT_FOUND
        result_item = {
            'freq': s[0].split(':')[-1],
            'protocol': s[1].split(':')[-1],
            'modulation': s[2].split(':')[-1],
            'data': s[3].split(':')[-1],
            'playback': False,
            'msg_type': msg_type
        }
        result_items.append(result_item)
    return simplejson.dumps({'status': 'success',
                             'api': 'all_rf_item',
                             'parameter': msg_type,
                             'message': 'Get all_rf_item success.',
                             data_key: result_items,
                             'data_key': data_key
                             })


@app.route("/rf_item/<string:msg_type>", methods=['GET'])
def get_rf_item(msg_type):
    result_item = {}
    data_key = msg_type + "_item"
    if msg_type == 'arf':
        file_path = app.config['ARF_DATA_FILE']
        with open(file_path, 'rb') as f:
            new_MD5 = hashlib.md5(file_as_bytes(f)).hexdigest()
            is_change = new_MD5 != app.config['ARF_DATA_FILE_MD5']
            app.config['ARF_DATA_FILE_MD5'] = new_MD5 if is_change else app.config['ARF_DATA_FILE_MD5']
    elif msg_type == 'crf':
        file_path = app.config['CRF_DATA_FILE']
        with open(file_path, 'rb') as f:
            new_MD5 = hashlib.md5(file_as_bytes(f)).hexdigest()
            is_change = new_MD5 != app.config['CRF_DATA_FILE_MD5']
            app.config['CRF_DATA_FILE_MD5'] = new_MD5 if is_change else app.config['CRF_DATA_FILE_MD5']
    else:
        return simplejson.dumps({'status': 'fail',
                                 'api': 'rf_item',
                                 'parameter': msg_type,
                                 'message': 'Get rf_item fail.parameter msg_type error.',
                                 data_key: result_item,
                                 'data_key': data_key
                                 }), status.HTTP_400_BAD_REQUEST

    if not is_change:
        return simplejson.dumps({'status': 'success',
                                 'api': 'rf_item',
                                 'parameter': msg_type,
                                 'message': 'Get rf_item success, but NOT MODIFIED.',
                                 data_key: result_item,
                                 'data_key': data_key
                                 }), status.HTTP_304_NOT_MODIFIED
    with open(file_path, 'r') as f:
        lines = f.readlines()
    while lines and not lines[-1].strip():
        del lines[-1]
    if not lines:
        return simplejson.dumps({'status': 'fail',
                                 'api': 'rf_item',
                                 'parameter': msg_type,
                                 'message': 'Get rf_item fail.Item not exist.',
                                 data_key: result_item,
                                 'data_key': data_key
                                 }), status.HTTP_404_NOT_FOUND

    s = lines[-1].split(';')
    if len(s) != 4:
        return simplejson.dumps({'status': 'fail',
                                 'api': 'rf_item',
                                 'parameter': msg_type,
                                 'message': 'Get rf_item fail.Item format error.',
                                 data_key: result_item,
                                 'data_key': data_key
                                 }), status.HTTP_404_NOT_FOUND
    result_item = {
        'freq': s[0].split(':')[-1],
        'protocol': s[1].split(':')[-1],
        'modulation': s[2].split(':')[-1],
        'data': s[3].split(':')[-1],
        'playback': False,
        'msg_type': msg_type
    }
    return simplejson.dumps({'status': 'success',
                             'api': 'get_rf_item',
                             'parameter': msg_type,
                             'message': 'Get rf_item success.',
                             data_key: result_item,
                             'data_key': data_key
                             })


@app.route("/ap_list", methods=['GET'])
def get_ap_list():
    ap_list = []
    if not os.path.exists(app.config['AP_LIST_FILE']):
        return simplejson.dumps({'status': 'fail',
                                 'api': 'ap_list',
                                 'parameter': None,
                                 'message': 'Get ap_list fail.File not found.',
                                 'ap_list': ap_list,
                                 'data_key': 'ap_list'
                                 }), status.HTTP_404_NOT_FOUND
    with open(app.config['AP_LIST_FILE'], 'rb') as f:
        new_MD5 = hashlib.md5(file_as_bytes(f)).hexdigest()
    if new_MD5 == app.config['AP_LIST_FILE_MD5']:
        return simplejson.dumps({'status': 'success',
                                 'api': 'ap_list',
                                 'parameter': None,
                                 'message': 'Get ap_list success.But file NOT MODIFIED.',
                                 'ap_list': ap_list,
                                 'data_key': 'ap_list'
                                 }), status.HTTP_304_NOT_MODIFIED

    app.config['AP_LIST_FILE_MD5'] = new_MD5
    with open(app.config['AP_LIST_FILE'], 'r') as f:
        lines = f.readlines()
    for line in lines:
        l = line.split()
        if len(l) == 3:
            i = {
                'BSSID': l[0],
                'RSSI': l[2],
                'SSID': '(hidden)',
                'JAM': False
            }
        elif len(l) == 4:
            i = {
                'BSSID': l[0],
                'RSSI': l[2],
                'SSID': l[3],
                'JAM': False
            }
        else:
            continue
        ap_list.append(i)
    return simplejson.dumps({'status': 'success',
                             'api': 'ap_list',
                             'parameter': None,
                             'message': 'Get ap_list success.',
                             'ap_list': ap_list,
                             'data_key': 'ap_list'
                             })


@app.route("/sta_list", methods=['GET'])
def get_sta_list():
    sta_list = []
    if not os.path.exists(app.config['STA_LIST_FILE']):
        return simplejson.dumps({'status': 'fail',
                                 'api': 'sta_list',
                                 'parameter': app.config['STA_LIST_FILE'],
                                 'message': 'Get sta_list error.File not found.',
                                 'sta_list': sta_list,
                                 'data_key': 'sta_list'
                                 }), status.HTTP_404_NOT_FOUND

    file_path = app.config['STA_LIST_FILE']
    with open(file_path, 'rb') as f:
        new_MD5 = hashlib.md5(file_as_bytes(f)).hexdigest()
    if new_MD5 == app.config['STA_LIST_FILE_MD5']:
        return simplejson.dumps({'status': 'success',
                                 'api': 'sta_list',
                                 'parameter': None,
                                 'message': 'Get sta_list success.But file NOT MODIFIED.',
                                 'sta_list': sta_list,
                                 'data_key': 'sta_list'
                                 }), status.HTTP_304_NOT_MODIFIED
    app.config['STA_LIST_FILE_MD5'] = new_MD5
    with open(file_path, 'r') as f:
        lines = f.readlines()
    for line in lines:
        if not line:
            continue
        l = line.split()
        if len(l) < 4:
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
                             'message': 'Get sta_list success.',
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


@app.route('/hd_info', methods=['GET'])
def get_hd_info():
    hd_info = None
    file_path = app.config['HD_INFO_FILE']
    if not os.path.exists(file_path):
        return simplejson.dumps({'status': 'fail',
                                 'api': 'hd_info',
                                 'parameter': None,
                                 'message': 'Get hd_info fail, file not found.',
                                 'data_key': 'hd_info',
                                 'hd_info': hd_info
                                 }), status.HTTP_404_NOT_FOUND

    with open(file_path, 'r') as f:
        lines = f.readlines()
        for i in range(len(lines)):
            if not lines[i]:
                del lines[i]

    if len(lines) != 2:
        return simplejson.dumps({'status': 'fail',
                                 'api': 'hd_info',
                                 'parameter': None,
                                 'message': 'Get hd_info fail,log file format error.',
                                 'data_key': 'hd_info',
                                 'hd_info': hd_info
                                 }), status.HTTP_500_INTERNAL_SERVER_ERROR
    total = int(lines[0].split('G')[0])
    used = int(lines[1].split('G')[0])
    # get percentage
    hd_info = used * 100 / total
    return simplejson.dumps({'status': 'success',
                             'api': 'hd_info',
                             'parameter': None,
                             'message': 'Get hd_info success.',
                             'data_key': 'hd_info',
                             'hd_info': hd_info
                             })


@app.route("/update_firmware_log", methods=['GET'])
def update_firmware_log():
    update_log = None
    file_path = app.config['FIRMWARE_UPDATE_LOG_FILE']
    if not os.path.exists(file_path):
        return simplejson.dumps({'status': 'fail',
                                 'api': 'update_firmware_log',
                                 'parameter': None,
                                 'message': 'Get update_firmware_log fail, file not found.',
                                 'data_key': 'update_log',
                                 'update_log': update_log
                                 }), status.HTTP_404_NOT_FOUND
    # Check if update log is NOT MODIFIED by MD5
    with open(file_path, 'rb') as f:
        new_MD5 = hashlib.md5(file_as_bytes(f)).hexdigest()
    if new_MD5 == app.config['FIRMWARE_UPDATE_LOG_MD5']:
        return simplejson.dumps({'status': 'success',
                                 'api': 'update_firmware_log',
                                 'parameter': None,
                                 'message': 'Get update_firmware_log success.',
                                 'data_key': 'update_log',
                                 'update_log': update_log
                                 }), status.HTTP_304_NOT_MODIFIED
    else:
        app.config['FIRMWARE_UPDATE_LOG_MD5'] = new_MD5
        with open(file_path, 'r') as f:
            update_log = f.read()
        return simplejson.dumps({'status': 'success',
                                 'api': 'update_firmware_log',
                                 'parameter': None,
                                 'message': 'Get update_firmware_log success.',
                                 'data_key': 'update_log',
                                 'update_log': update_log
                                 })


@app.route("/update_firmware", methods=['POST'])
def update_firmware():
    # TODO: Parse as dict and get data
    uploaded_file_path = request.data.split('"')[3]
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
            # elif app.config['DEBUG']:
            #     app.config['UPLOAD_FOLDER'] = "data/"
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
                return simplejson.dumps({'status': 'fail',
                                         'api': 'upload',
                                         'parameter': filename,
                                         'message': 'Upload file fail.Error raise while save file.',
                                         'data_key': None
                                         }), status.HTTP_500_INTERNAL_SERVER_ERROR

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


def check_file(file_path, file_key):
    if not os.path.exists(file_path):
        print('{} in [{}] NOT FOUND, Please check it and then restart server.'.format(file_key, file_path))
        exit(1)
    return True


def init_data():
    if app.config['DEBUG']:
        print(bcolors.WARNING + 'NOTE: You are running server in DEBUG mode, please make sure '
                                'change to product mode before release.' + bcolors.ENDC)
    elif app.config['TESTING']:
        print(bcolors.WARNING + 'NOTE: You are running server in TESTING mode, please make sure '
                                'change to product mode before release.' + bcolors.ENDC)
    else:
        print('NOTE: You are running server in PRODUCTION mode, If you want more'
              'debug information, you can run in DEBUG or TESTING mode.')

    for key, value in app.config.items():
        if '_FILE' == key[-5:] or '_SHELL' == key[-6:]:
            try:
                check_file(value, key)
            except TypeError as e:
                print(e)

    file_path = app.config['FIRMWARE_UPDATE_LOG_FILE']
    with open(file_path, 'rb') as f:
        app.config['FIRMWARE_UPDATE_LOG_MD5'] = hashlib.md5(file_as_bytes(f)).hexdigest()

    file_path = app.config['NFC_DATA_FILE']
    with open(file_path, 'rb') as f:
        app.config['NFC_DATA_FILE_MD5'] = hashlib.md5(file_as_bytes(f)).hexdigest()

    file_path = app.config['ARF_DATA_FILE']
    with open(file_path, 'rb') as f:
        app.config['ARF_DATA_FILE_MD5'] = hashlib.md5(file_as_bytes(f)).hexdigest()

    file_path = app.config['CRF_DATA_FILE']
    with open(file_path, 'rb') as f:
        app.config['CRF_DATA_FILE_MD5'] = hashlib.md5(file_as_bytes(f)).hexdigest()

    file_path = app.config['AP_LIST_FILE']
    with open(file_path, 'rb') as f:
        app.config['AP_LIST_FILE_MD5'] = hashlib.md5(file_as_bytes(f)).hexdigest()

    file_path = app.config['STA_LIST_FILE']
    with open(file_path, 'rb') as f:
        app.config['STA_LIST_FILE_MD5'] = hashlib.md5(file_as_bytes(f)).hexdigest()

    # TODO: Improve code to intelligent detection
    folder_list = {
        'HID-Script': app.config['UPLOAD_FOLDERS']['HID-Script'],
        'INFO-Pie': app.config['UPLOAD_FOLDERS']['INFO-Pie'],
        'INFO-Ardu': app.config['UPLOAD_FOLDERS']['INFO-Ardu'],
    }
    for folder_key, folder_path in folder_list.items():
        check_file(folder_path, folder_key)


if __name__ == '__main__':
    init_data()
    app.run(host='0.0.0.0')
