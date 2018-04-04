class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'h\xcb\x81\xaf%\x81\xd5\x02\xc4L\xad,r\x04\xa4*\x8a\xfd\xb6m\\#<\xed'
    THUMBNAIL_FOLDER = 'data/thumbnail/'
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024
    ARF_DATA_FILE_MD5 = None
    CRF_DATA_FILE_MD5 = None
    NFC_DATA_FILE_MD5 = None
    FIRMWARE_UPDATE_LOG_MD5 = None
    AP_LIST_FILE_MD5 = None
    STA_LIST_FILE_MD5 = None
    FIRMWARE_NFC_LOG_MD5 = None

class ProductionConfig(Config):
    AP_LIST_FILE = '/root/monitor_file/AP_list_tmp'
    STA_LIST_FILE = '/root/monitor_file/STA_list_tmp'
    NFC_DATA_FILE = '/root/serial_file/data/bNFC_data'
    ARF_DATA_FILE = '/root/serial_file/data/aRF_Keeloq_data'
    CRF_DATA_FILE = '/root/serial_file/data/cRF_24l01_data'
    FIRMWARE_UPDATE_LOG_FILE = '/root/user_file/INFO/update_firmware_log'
    HD_INFO_FILE = '/etc/HD_info'
    ATTACK_PROGRESS_FILE = '/root/serial_file/attack_progress_bar'
    FIRMWARE_NFC_LOG_FILE = '/root/serial_file/data/NFC_log'

    STA_BLOCK_SHELL = "/root/monitor_file/STA_block.sh"
    WIFI_SCAN_SHELL = "/root/monitor_file/wifi_scan.sh"
    AP_BLOCK_SHELL = "/root/monitor_file/AP_block.sh"
    SERIAL_SEND_SHELL = "/root/serial_file/serial_send.sh"
    UPDATE_FIRMWARE_SHELL = "/root/user_file/INFO/update.sh"
    SEND_DIRECTION_SHELL = "/root/Cube_GPIO/direction.sh"
    UPLOAD_FOLDERS = {
        'HID-Script': "/root/user_file/HID/",
        'INFO-Pie': "/root/user_file/INFO/raspberrypi/",
        'INFO-Ardu': "/root/user_file/INFO/arduino/"
    }


class DevelopmentConfig(Config):
    DEBUG = True
    AP_LIST_FILE = 'data/example_source/AP_list_tmp'
    STA_LIST_FILE = 'data/example_source/STA_list_tmp'
    NFC_DATA_FILE = 'data/example_source/bNFC_data'
    ARF_DATA_FILE = 'data/example_source/aRF_Keeloq_data'
    CRF_DATA_FILE = 'data/example_source/cRF_24l01_data'
    FIRMWARE_UPDATE_LOG_FILE = 'data/example_source/update_firmware_log'
    HD_INFO_FILE = 'data/example_source/HD_info'
    ATTACK_PROGRESS_FILE = 'data/example_source/attack_progress_bar'
    FIRMWARE_NFC_LOG_FILE = 'data/example_source/NFC_log'

    STA_BLOCK_SHELL = "data/example_bash/test_success.sh"
    WIFI_SCAN_SHELL = "data/example_bash/test_success.sh"
    AP_BLOCK_SHELL = "data/example_bash/test_success.sh"
    SERIAL_SEND_SHELL = "data/example_bash/test_success.sh"
    UPDATE_FIRMWARE_SHELL = "data/example_bash/test_success.sh"
    SEND_DIRECTION_SHELL = "data/example_bash/test_success.sh"
    UPLOAD_FOLDERS = {
        'HID-Script': "data/example_dir/HID/",
        'INFO-Pie': "data/example_dir/raspberrypi/",
        'INFO-Ardu': "data/example_dir/arduino/"
    }

    # app.config['AP_BLOCK_SHELL'] = "data/example_bash/test_success.sh"


class TestingConfig(Config):
    TESTING = True
