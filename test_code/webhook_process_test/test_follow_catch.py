import unittest, os
from unittest import mock
# twitter_receve用テストコード
import receve_api
from flask import Flask, request
import json
from watson_developer_cloud import PersonalityInsightsV3
# mockのimport
from test_code.webhook_process_mock import follow_catch_mock
# DB用のimport
from DB.koukokuDB.database import reset_db, init_db, db
from DB.koukokuDB.models import User

class TestFollowCatch(unittest.TestCase):
    # test_receve実行前に1度だけ
    @classmethod
    def setUpClass(self):
        app = Flask(__name__)
        app.config.from_object('DB.koukokuDB.config.Config')
        init_db(app)
        reset_db(app)
        print('DB reset!!')
    # test_receve内関数を実行ごとに
    def setUp(self):
        self.app = receve_api.app.test_client()

    # フォローが来た時(まだフォローしていない)の動作を確認
    @mock.patch('requests.get', side_effect=follow_catch_mock.mocked_twitter_API)
    @mock.patch('requests.post', side_effect=follow_catch_mock.mocked_twitter_API)
    @mock.patch('watson_developer_cloud.PersonalityInsightsV3.profile', side_effect=follow_catch_mock.mocked_watson_API)
    def test_twitter_follow_1(self, mock_get, mock_post, mock_watson):
        # followがきた時のjsonをロード
        with open("test_code/test_json/follow_event.json", "r") as follow_event_json_file:
            follow_event_json = json.load(follow_event_json_file)
            follow_event_json["follow_events"][0]["source"]["id"] = os.environ['TEST_ACCOUNT_ID']
        # twitterからのfollowイベントのAPIを再現
        response = self.app.post(
            "/webhooks/twitter",
            content_type='application/json',
            data=json.dumps(follow_event_json)
        )

        # レスポンス結果の再現
        response_body = {
            "DM"       : "",
            "New User" : "OK",
            "Follow"   : "OK"
        }
        response_body_encode = json.dumps(response_body).encode()
        # レスポンス結果のの照合
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, response_body_encode)

        app = Flask(__name__)
        app.config.from_object('DB.koukokuDB.config.Config')
        init_db(app)
        # DB挿入結果の照会
        with app.app_context():
            user = User.query.get(1)
        if os.environ['ENV'] == "wercker":
            self.assertEqual(user.twitter_userid_hash, "1b4b80eac7655015bccdc0cc002a8ea04a2aadea")
        else:
            self.assertEqual(user.twitter_userid_hash, "a885426aedc08aa137078d16dfe28899b512d827")
    # フォローが来た時(既にフォローしている)の動作を確認
    @mock.patch('requests.get', side_effect=follow_catch_mock.mocked_twitter_API_2)
    @mock.patch('requests.post', side_effect=follow_catch_mock.mocked_twitter_API)
    @mock.patch('watson_developer_cloud.PersonalityInsightsV3.profile', side_effect=follow_catch_mock.mocked_watson_API)
    def test_twitter_follow_2(self, mock_get, mock_post, mock_watson):
        # followがきた時のjsonをロード
        with open("test_code/test_json/follow_event.json", "r") as follow_event_json_file:
            follow_event_json = json.load(follow_event_json_file)
            follow_event_json["follow_events"][0]["source"]["id"] = os.environ['TEST_ACCOUNT_ID']
        # twitterからのfollowイベントのAPIを再現
        response = self.app.post(
            "/webhooks/twitter",
            content_type='application/json',
            data=json.dumps(follow_event_json)
        )

        # レスポンス結果の再現
        response_body = {
            "DM"       : "",
            "New User" : "NO",
            "Follow"   : "NO"
        }
        response_body_encode = json.dumps(response_body).encode()
        # レスポンス結果のの照合
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, response_body_encode)

        app = Flask(__name__)
        app.config.from_object('DB.koukokuDB.config.Config')
        init_db(app)
        # DB挿入結果の照会
        with app.app_context():
            user_count = User.query.count()
        self.assertEqual(user_count, 1)
