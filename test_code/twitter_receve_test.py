import unittest
# twitter_receve用テストコード
import twitter_receve.receve_api
from flask import Flask, request
import json


class TestTwitterReceve(unittest.TestCase):

    def setUp(self):
        self.app = twitter_receve.receve_api.app.test_client()

    def test_twitter_request(self):
        # twitterからのリクエストAPIを再現
        response = self.app.get('/webhooks/twitter?crc_token=foo')
        # レスポンス結果の再現
        response_body = {
            'response_token': 'sha256=D1UXbLq0ougTycgcBn9pWDTS2jarXz/3wS5yVJniPFY='
        }
        response_body_encode = json.dumps(response_body).encode()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, response_body_encode)

if __name__ == '__main__':
    unittest.main()
