import unittest, os
from unittest import mock
# twitter_receve用テストコード
import receve_api
from flask import Flask, request
import json
# mockのimport
from test_code.webhook_process_mock import DM_catch_error_mock
# DB用のimport
from DB.koukokuDB.database import init_db
from DB.koukokuDB.models import User
# sagemakerの推薦モデルを利用
import boto3

class TestDMCatch(unittest.TestCase):

    # test_receve内関数を実行ごとに
    def setUp(self):
        app = Flask(__name__)
        app.config.from_object('DB.koukokuDB.config.Config')
        self.app = receve_api.app.test_client()

    # 「登録」前に「推薦」メッセージが来た時の動作を確認
    @mock.patch('boto3.client', side_effect=DM_catch_error_mock.boto3_client)
    @mock.patch('requests.post', side_effect=DM_catch_error_mock.mocked_twitter_API)
    def test_twitter_DM_1_recommen_error(self, mock_post, mock_boto3):
        # DMがきた時のjsonをロード
        with open("test_code/test_json/direct_message_events.json", "r") as DM_event_json_file:
            DM_event_json = json.load(DM_event_json_file)
            DM_event_json["direct_message_events"][0]["message_create"]["sender_id"] = os.environ['TEST_ACCOUNT_ID']
            DM_event_json["direct_message_events"][0]["message_create"]["message_data"]["text"] = "推薦"

        # twitterからのDMイベントのAPIを再現
        response = self.app.post(
            "/webhooks/twitter",
            content_type='application/json',
            data=json.dumps(DM_event_json)
        )

        # レスポンス結果の再現
        response_body = {
            "DM"           : "Not Recommen DM",
            "New User"     : "",
            "Follow"       : "",
            "Update_model" : ""
        }
        response_body_encode = json.dumps(response_body).encode()
        # レスポンス結果のの照合
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, response_body_encode)

    # 「登録」前に「評価」メッセージが来た時の動作を確認
    @mock.patch('requests.post', side_effect=DM_catch_error_mock.mocked_twitter_API)
    def test_twitter_DM_2_evaluation_error(self, mock_post):
        # DMがきた時のjsonをロード
        with open("test_code/test_json/direct_message_events.json", "r") as DM_event_json_file:
            DM_event_json = json.load(DM_event_json_file)
            DM_event_json["direct_message_events"][0]["message_create"]["sender_id"] = os.environ['TEST_ACCOUNT_ID']
            DM_event_json["direct_message_events"][0]["message_create"]["message_data"]["text"] = "評価"

        # twitterからのDMイベントのAPIを再現
        response = self.app.post(
            "/webhooks/twitter",
            content_type='application/json',
            data=json.dumps(DM_event_json)
        )

        # レスポンス結果の再現
        response_body = {
            "DM"           : "evaluation NO DM",
            "New User"     : "",
            "Follow"       : "",
            "Update_model" : ""
        }
        response_body_encode = json.dumps(response_body).encode()
        # レスポンス結果のの照合
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, response_body_encode)

    # 「フォロー」前に「登録」メッセージが来た時の動作を確認
    @mock.patch('requests.get', side_effect=DM_catch_error_mock.mocked_twitter_API)
    @mock.patch('requests.post', side_effect=DM_catch_error_mock.mocked_twitter_API)
    @mock.patch('watson_developer_cloud.PersonalityInsightsV3.profile', side_effect=DM_catch_error_mock.mocked_watson_API)
    def test_twitter_DM_3_registration_error(self, mock_post, mock_boto3, mock_watson):
        # DMがきた時のjsonをロード
        with open("test_code/test_json/direct_message_events.json", "r") as DM_event_json_file:
            DM_event_json = json.load(DM_event_json_file)
            DM_event_json["direct_message_events"][0]["message_create"]["sender_id"] = os.environ['TEST_ACCOUNT_ID']
            DM_event_json["direct_message_events"][0]["message_create"]["message_data"]["text"] = "登録"
        # twitterからのDMイベントのAPIを再現
        response = self.app.post(
            "/webhooks/twitter",
            content_type='application/json',
            data=json.dumps(DM_event_json)
        )
        # レスポンス結果の再現
        response_body = {
            "DM"           : "",
            "New User"     : "NO",
            "Follow"       : "",
            "Update_model" : ""
        }
        response_body_encode = json.dumps(response_body).encode()
        # レスポンス結果のの照合
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, response_body_encode)

    # DMが来た時の動作を確認
    @mock.patch('requests.post', side_effect=DM_catch_error_mock.mocked_twitter_API)
    def test_twitter_DM_4_error(self, mock_post):
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
            "DM"           : "else DM event",
            "New User"     : "",
            "Follow"       : "",
            "Update_model" : ""
        }
        response_body_encode = json.dumps(response_body).encode()
        # レスポンス結果のの照合
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, response_body_encode)

if __name__ == '__main__':
    unittest.main()
