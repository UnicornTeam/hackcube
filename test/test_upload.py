import unittest
import app as instance
import tempfile


class UploadTestCase(unittest.TestCase):

    def setUp(self):
        f, filename = tempfile.mkstemp(suffix='txt', text=True)
        f.write('foo bar')
        self.type_list = ['HID-Script', 'INFO-Pie', 'INFO-Ardu']
        self.app = instance.app.test_client()
        instance.app.config['UPLOAD_FOLDER'] = 'data/'
        instance.app.config['UPLOAD_HID_SCRIPT_FOLDER'] = "/root/user_file/HID/"
        instance.app.config['UPLOAD_INFO_PIE_FOLDER'] = "/root/user_file/raspberrypi"
        instance.app.config['UPLOAD_INFO_ARDU_FOLDER'] = "/root/user_file/arduino/"

    def test_upload(self):
        for file_type in self.type_list:
            extra_data = {
                'type': file_type
            }
            resp = self.app.post('/upload', data=extra_data)
