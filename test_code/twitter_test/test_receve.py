import unittest, os
from unittest import mock
# twitter_receve用テストコード
import receve_api
from flask import Flask, request
import json
from watson_developer_cloud import PersonalityInsightsV3
# mockのimport
from test_code.twitter_test import receve_mock
# DB用のimport
from twitter_receve.koukokuDB.database import reset_db, init_db, db
from twitter_receve.koukokuDB.models import User
from twitter_receve.koukokuDB.database import db
# sagemakerの推薦モデルを利用
import boto3

class TestTwitterReceve(unittest.TestCase):
    # test_receve実行前に1度だけ
    @classmethod
    def setUpClass(self):
        app = Flask(__name__)
        app.config.from_object('twitter_receve.koukokuDB.config.Config')
        init_db(app)
        reset_db(app)
        print('DB reset!!')
    # test_receve内関数を実行ごとに
    def setUp(self):
        self.app = receve_api.app.test_client()


    # webhookの登録が正常にできるか確認
    def test_webhook_challenge(self):
        # twitterからのリクエストAPIを再現
        response = self.app.get("/webhooks/twitter?crc_token=foo")
        # レスポンス結果の再現
        if os.environ['ACCESS_TOKEN_SECRET'] == "wercker":
            response_body = {
                "response_token": "sha256=D1UXbLq0ougTycgcBn9pWDTS2jarXz/3wS5yVJniPFY="
            }
        else:
            response_body = {
                "response_token": "sha256=jT6F6QmWjlqEuBvcEH96KZyhlRuQKjypYClETaAnl48="
            }
        response_body_encode = json.dumps(response_body).encode()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, response_body_encode)

    # フォローが来た時(まだフォローしていない)の動作を確認
    @mock.patch('requests.get', side_effect=receve_mock.mocked_twitter_API)
    @mock.patch('requests.post', side_effect=receve_mock.mocked_twitter_API)
    @mock.patch('watson_developer_cloud.PersonalityInsightsV3.profile', side_effect=receve_mock.mocked_watson_API)
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
            "status" : "Get follow",
            "New User" : "OK",
            "Follow" : "OK"
        }
        response_body_encode = json.dumps(response_body).encode()
        # レスポンス結果のの照合
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, response_body_encode)

        app = Flask(__name__)
        app.config.from_object('twitter_receve.koukokuDB.config.Config')
        init_db(app)
        # DB挿入結果の照会
        with app.app_context():
            user = User.query.get(1)
        self.assertEqual(user.twitter_userid, os.environ['TEST_ACCOUNT_ID'])
    # フォローが来た時(既にフォローしている)の動作を確認
    @mock.patch('requests.get', side_effect=receve_mock.mocked_twitter_API_2)
    @mock.patch('requests.post', side_effect=receve_mock.mocked_twitter_API)
    @mock.patch('watson_developer_cloud.PersonalityInsightsV3.profile', side_effect=receve_mock.mocked_watson_API)
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
            "status" : "Get follow",
            "New User" : "NO",
            "Follow" : "NO"
        }
        response_body_encode = json.dumps(response_body).encode()
        # レスポンス結果のの照合
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, response_body_encode)

        app = Flask(__name__)
        app.config.from_object('twitter_receve.koukokuDB.config.Config')
        init_db(app)
        # DB挿入結果の照会
        with app.app_context():
            user_count = User.query.count()
        self.assertEqual(user_count, 1)

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
            "status" : "OK",
            "New User" : "",
            "Follow" : ""
        }
        response_body_encode = json.dumps(response_body).encode()
        # レスポンス結果のの照合
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, response_body_encode)

class TestTwitterReceve2(unittest.TestCase):
    # test_receve内関数を実行ごとに
    def setUp(self):
        self.app = receve_api.app.test_client()

    # DMが来た時の動作を確認
    @mock.patch('boto3.client', side_effect=receve_mock.boto3_client)
    @mock.patch('requests.post', side_effect=receve_mock.mocked_twitter_API)
    def test_twitter_DM(self, mock_post, mock_boto3):
        # DMがきた時のjsonをロード
        with open("test_code/test_json/direct_message_events.json", "r") as DM_event_json_file:
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
            "status" : "Return DM",
            "New User" : "",
            "Follow" : ""
        }
        response_body_encode = json.dumps(response_body).encode()
        # レスポンス結果のの照合
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, response_body_encode)

if __name__ == '__main__':
    unittest.main()
