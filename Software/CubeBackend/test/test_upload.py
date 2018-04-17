import json
import unittest
from StringIO import StringIO
import app as instance


class UploadTestCase(unittest.TestCase):

    def setUp(self):
        self.type_list = ['HID-Script', 'INFO-Pie', 'INFO-Ardu']
        self.app = instance.app.test_client()
        instance.app.config['TEST'] = True

    def test_upload(self):
        for file_type in self.type_list:
            resp = self.app.post(
                '/upload',
                buffered=True,
                content_type='multipart/form-data',
                data={
                    'file': (StringIO('foo'), 'hello world.txt'),
                    'type': file_type
                }
            )
            exp_resp = {
                "files": [{
                    "name": "hello world.txt",
                    "url": "data/hello world.txt",
                    "deleteType": "DELETE",
                    "type": "text/plain",
                    "deleteUrl": "delete/hello world.txt",
                    "size": 3
                }]
            }
            assert resp.data == json.dumps(exp_resp)

    def tearDown(self):
        print('done')
