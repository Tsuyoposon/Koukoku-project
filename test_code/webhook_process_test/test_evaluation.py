import unittest, os
from unittest import mock
# twitter_receve用テストコード
import receve_api
from flask import Flask, request
import json
# mockのimport
from test_code.webhook_process_mock import evaluation_mock
# DB用のimport
from DB.koukokuDB.database import db
from DB.koukokuDB.models import User

class TestEvaluation(unittest.TestCase):

    # test_receve内関数を実行ごとに
    def setUp(self):
        app = Flask(__name__)
        app.config.from_object('DB.koukokuDB.config.Config')
        self.app = receve_api.app.test_client()

    # 「評価」メッセージが来た時の動作を確認
    @mock.patch('requests.post', side_effect=evaluation_mock.mocked_twitter_API)
    def test_evaluation(self, mock_post):
        # DMがきた時のjsonをロード
        with open("test_code/test_json/quick_replies_item.json", "r") as DM_event_json_file:
            DM_event_json = json.load(DM_event_json_file)
            DM_event_json["direct_message_events"][0]["message_create"]["sender_id"] = os.environ['TEST_ACCOUNT_ID']

        # twitterからのDMイベントのAPIを再現
        response = self.app.post(
            "/webhooks/twitter",
            content_type='application/json',
            data=json.dumps(DM_event_json)
        )

        # レスポンス結果の再現
        response_body = {
            "DM"       : "evaluation evaluation_sent DM",
            "New User" : "",
            "Follow"   : ""
        }
        response_body_encode = json.dumps(response_body).encode()
        # レスポンス結果のの照合
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, response_body_encode)

if __name__ == '__main__':
    unittest.main()
