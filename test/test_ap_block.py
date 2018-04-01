import unittest
import json
import app as instance


class JSONObject:
    def __init__(self, d):
        self.__dict__ = d


class APBlockTestCase(unittest.TestCase):
    def setUp(self):
        instance.app.testing = True
        self.ssid = 'F0:50:40:30:20:10'
        self.api = 'ap_block'
        self.app = instance.app.test_client()

    # TODO: Add fail test
    def test_ap_block_on_success(self):
        action = 'on'
        instance.app.config['AP_BLOCK_SHELL'] = "example_bash/test_success.sh"
        resp = self.app.get('/{}/{}/{}'.format(self.api, self.ssid, action))
        exp_resp = {'status': 'success',
                    'action': action,
                    'api': self.api,
                    'message': 'Call AP_block process success.'
                    }
        assert resp.data == json.dumps(exp_resp)

    # TODO: Add fail test
    def test_ap_block_off_success(self):
        action = 'off'
        instance.app.config['AP_BLOCK_SHELL'] = "example_bash/test_success.sh"
        resp = self.app.get('/{}/{}/{}'.format(self.api, self.ssid, action))
        exp_resp = {'status': 'success',
                    'action': action,
                    'api': self.api,
                    'message': 'Call AP_block process success.'
                    }
        assert resp.data == json.dumps(exp_resp)

    def tearDown(self):
        print('Done')


if __name__ == '__main__':
    unittest.main()
