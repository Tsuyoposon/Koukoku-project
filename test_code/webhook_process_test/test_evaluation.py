import unittest, os
from unittest import mock
# twitter_receve用テストコード
import receve_api
from flask import Flask, request
import json
# mockのimport
from test_code.webhook_process_mock import evaluation_mock
# DB用のimport
from DB.koukokuDB.database import reset_db, init_db, db
from DB.koukokuDB.models import Feedback

class TestEvaluation(unittest.TestCase):

    # test_receve内関数を実行ごとに
    def setUp(self):
        app = Flask(__name__)
        app.config.from_object('DB.koukokuDB.config.Config')
        self.app = receve_api.app.test_client()

    # 「選択アイテムの切り替え(後半を要求)」メッセージが来た時の動作を確認
    @mock.patch('requests.post', side_effect=evaluation_mock.mocked_twitter_API)
    def test_select_item_1(self, mock_post):
        # DMがきた時のjsonをロード
        with open("test_code/test_json/quick_replies_item.json", "r") as DM_event_json_file:
            DM_event_json = json.load(DM_event_json_file)
            DM_event_json["direct_message_events"][0]["message_create"]["sender_id"] = os.environ['TEST_ACCOUNT_ID']
            DM_event_json["direct_message_events"][0]["message_create"]["message_data"]["quick_reply_response"]["metadata"] = "select_kouhann"
        # twitterからのDMイベントのAPIを再現
        response = self.app.post(
            "/webhooks/twitter",
            content_type='application/json',
            data=json.dumps(DM_event_json)
        )

        # レスポンス結果の再現
        response_body = {
            "DM"           : "evaluation item_sent DM",
            "New User"     : "",
            "Follow"       : "",
            "Update_model" : ""
        }
        response_body_encode = json.dumps(response_body).encode()
        # レスポンス結果のの照合
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, response_body_encode)

    # 「選択アイテムの切り替え(後半を要求)」メッセージが来た時の動作を確認
    @mock.patch('requests.post', side_effect=evaluation_mock.mocked_twitter_API)
    def test_select_item_1(self, mock_post):
        # DMがきた時のjsonをロード
        with open("test_code/test_json/quick_replies_item.json", "r") as DM_event_json_file:
            DM_event_json = json.load(DM_event_json_file)
            DM_event_json["direct_message_events"][0]["message_create"]["sender_id"] = os.environ['TEST_ACCOUNT_ID']
            DM_event_json["direct_message_events"][0]["message_create"]["message_data"]["quick_reply_response"]["metadata"] = "select_zenhann"
        # twitterからのDMイベントのAPIを再現
        response = self.app.post(
            "/webhooks/twitter",
            content_type='application/json',
            data=json.dumps(DM_event_json)
        )

        # レスポンス結果の再現
        response_body = {
            "DM"           : "evaluation item_sent DM",
            "New User"     : "",
            "Follow"       : "",
            "Update_model" : ""
        }
        response_body_encode = json.dumps(response_body).encode()
        # レスポンス結果のの照合
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, response_body_encode)

    # 「選択アイテムのquick-replies」メッセージが来た時の動作を確認
    @mock.patch('requests.post', side_effect=evaluation_mock.mocked_twitter_API)
    def test_evaluation_item(self, mock_post):
        # DMがきた時のjsonをロード
        with open("test_code/test_json/quick_replies_item.json", "r") as DM_event_json_file:
            DM_event_json = json.load(DM_event_json_file)
            DM_event_json["direct_message_events"][0]["message_create"]["sender_id"] = os.environ['TEST_ACCOUNT_ID']
            DM_event_json["direct_message_events"][0]["message_create"]["message_data"]["quick_reply_response"]["metadata"] = "0"
        # twitterからのDMイベントのAPIを再現
        response = self.app.post(
            "/webhooks/twitter",
            content_type='application/json',
            data=json.dumps(DM_event_json)
        )

        # レスポンス結果の再現
        response_body = {
            "DM"           : "evaluation evaluation_sent DM",
            "New User"     : "",
            "Follow"       : "",
            "Update_model" : ""
        }
        response_body_encode = json.dumps(response_body).encode()
        # レスポンス結果のの照合
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, response_body_encode)

    # 「評価結果のquick-replies」メッセージが来た時(1回目)の動作を確認
    @mock.patch('requests.post', side_effect=evaluation_mock.mocked_twitter_API)
    def test_evaluation_hyouka_1(self, mock_post):
        # DMがきた時のjsonをロード
        with open("test_code/test_json/quick_replies_item.json", "r") as DM_event_json_file:
            DM_event_json = json.load(DM_event_json_file)
            DM_event_json["direct_message_events"][0]["message_create"]["sender_id"] = os.environ['TEST_ACCOUNT_ID']
            DM_event_json["direct_message_events"][0]["message_create"]["message_data"]["quick_reply_response"]["metadata"] = "0,hyouka-1"
        # twitterからのDMイベントのAPIを再現
        response = self.app.post(
            "/webhooks/twitter",
            content_type='application/json',
            data=json.dumps(DM_event_json)
        )

        # insert結果の照合
        app = Flask(__name__)
        app.config.from_object('DB.koukokuDB.config.Config')
        init_db(app)
        with app.app_context():
            feedback = Feedback.query.get(1)
        self.assertEqual(feedback.user_id, 1)
        self.assertEqual(feedback.recommen_item_id, 1)
        self.assertEqual(feedback.feedback, 1)

        # レスポンス結果の再現
        response_body = {
            "DM"           : "evaluation insert DM",
            "New User"     : "",
            "Follow"       : "",
            "Update_model" : ""
        }
        response_body_encode = json.dumps(response_body).encode()
        # レスポンス結果のの照合
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, response_body_encode)

    # 「評価結果のquick-replies」メッセージが来た時(2回目)の動作を確認
    @mock.patch('requests.post', side_effect=evaluation_mock.mocked_twitter_API)
    def test_evaluation_hyouka_2(self, mock_post):
        # DMがきた時のjsonをロード
        with open("test_code/test_json/quick_replies_item.json", "r") as DM_event_json_file:
            DM_event_json = json.load(DM_event_json_file)
            DM_event_json["direct_message_events"][0]["message_create"]["sender_id"] = os.environ['TEST_ACCOUNT_ID']
            DM_event_json["direct_message_events"][0]["message_create"]["message_data"]["quick_reply_response"]["metadata"] = "0,hyouka-2"
        # twitterからのDMイベントのAPIを再現
        response = self.app.post(
            "/webhooks/twitter",
            content_type='application/json',
            data=json.dumps(DM_event_json)
        )

        # update結果の照合
        app = Flask(__name__)
        app.config.from_object('DB.koukokuDB.config.Config')
        init_db(app)
        with app.app_context():
            feedback = Feedback.query.get(1)
            feedbacks = Feedback.query.all()
        self.assertEqual(feedback.user_id, 1)
        self.assertEqual(feedback.recommen_item_id, 1)
        self.assertEqual(feedback.feedback, 2)
        self.assertEqual(len(feedbacks), 1)

        # レスポンス結果の再現
        response_body = {
            "DM"           : "evaluation update DM",
            "New User"     : "",
            "Follow"       : "",
            "Update_model" : ""
        }
        response_body_encode = json.dumps(response_body).encode()
        # レスポンス結果のの照合
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, response_body_encode)

    # 「取り消し」メッセージが来た時の動作を確認
    def test_evaluation_cancel(self):
        # DMがきた時のjsonをロード
        with open("test_code/test_json/quick_replies_item.json", "r") as DM_event_json_file:
            DM_event_json = json.load(DM_event_json_file)
            DM_event_json["direct_message_events"][0]["message_create"]["sender_id"] = os.environ['TEST_ACCOUNT_ID']
            DM_event_json["direct_message_events"][0]["message_create"]["message_data"]["quick_reply_response"]["metadata"] = "cancel"
        # twitterからのDMイベントのAPIを再現
        response = self.app.post(
            "/webhooks/twitter",
            content_type='application/json',
            data=json.dumps(DM_event_json)
        )

        # レスポンス結果の再現
        response_body = {
            "DM"           : "evaluation cancel quick_reply",
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
