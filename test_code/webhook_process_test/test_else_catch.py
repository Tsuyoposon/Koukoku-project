import unittest, os
from unittest import mock
# twitter_receve用テストコード
import receve_api
from flask import Flask, request
import json

class TestElseCatch(unittest.TestCase):
    # test_receve内関数を実行ごとに
    def setUp(self):
        app = Flask(__name__)
        app.config.from_object('DB.koukokuDB.config.Config')
        self.app = receve_api.app.test_client()

    # その他のイベント(お気に入り)が来た時の動作を確認
    def test_twitter_favorite(self):
        # お気に入りされた時のjsonをロード
        with open("test_code/test_json/favorite_events.json", "r") as favorite_event_json_file:
            favorite_event_json = json.load(favorite_event_json_file)
        # twitterからのDMイベントのAPIを再現
        response = self.app.post(
            "/webhooks/twitter",
            content_type='application/json',
            data=json.dumps(favorite_event_json)
        )

        # レスポンス結果の再現
        response_body = {
            "DM"       : "",
            "New User" : "",
            "Follow"   : ""
        }
        response_body_encode = json.dumps(response_body).encode()
        # レスポンス結果のの照合
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, response_body_encode)

if __name__ == '__main__':
    unittest.main()
