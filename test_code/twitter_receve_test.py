import unittest
# twitter_receve用テストコード
import twitter_receve.receve_api
from flask import Flask, request
import json, os


class TestTwitterReceve(unittest.TestCase):

    def setUp(self):
        self.app = twitter_receve.receve_api.app.test_client()

    def test_twitter_request(self):
        # twitterからのリクエストAPIを再現
        response = self.app.get('/webhooks/twitter?crc_token=foo')
        # レスポンス結果の再現
        response_body = {
            'response_token': 'sha256=Qe1LDfqj4CGReEd7COcmXOPpt/L+WwLXsFLzAQyN2mc='
        }
        response_body_encode = json.dumps(response_body).encode()
        print(os.environ['TWITTER_CONSUMER_SECRET'])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, response_body_encode)

if __name__ == '__main__':
    unittest.main()
