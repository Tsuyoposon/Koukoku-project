import unittest, os
from unittest import mock
# twitter_receve用テストコード
import receve_api
from flask import Flask, request
import json
# mockのimport
from test_code.aws_process_mock import update_model_mock
# DB用のimport
from DB.koukokuDB.database import reset_db, init_db, db
from DB.koukokuDB.models import Feedback

class TestUpdateModel(unittest.TestCase):

    # test_receve内関数を実行ごとに
    def setUp(self):
        app = Flask(__name__)
        app.config.from_object('DB.koukokuDB.config.Config')
        self.app = receve_api.app.test_client()

    # 10件評価が来た時に推薦モデルを更新する
    @mock.patch('boto3.resource', side_effect=update_model_mock.boto3_resource)
    @mock.patch('aws_process.update_model.process', side_effect=update_model_mock.mocked_update_model)
    def test_evaluation_hyouka(self, mock_boto3, mock_update_model):
        # DMがきた時のjsonをロード
        with open("test_code/test_json/quick_replies_item.json", "r") as DM_event_json_file:
            DM_event_json = json.load(DM_event_json_file)
            DM_event_json["direct_message_events"][0]["message_create"]["sender_id"] = os.environ['TEST_ACCOUNT_ID']
            DM_event_json["direct_message_events"][0]["message_create"]["message_data"]["quick_reply_response"]["metadata"] = "0,hyouka-1"
        # twitterからのDMイベントのAPIを再現(9回)
        for i in range(9):
            response = self.app.post(
                "/webhooks/twitter",
                content_type='application/json',
                data=json.dumps(DM_event_json)
            )

        # hyoukaレコードの照合
        app = Flask(__name__)
        app.config.from_object('DB.koukokuDB.config.Config')
        init_db(app)
        with app.app_context():
            feedbacks = Feedback.query.all()
        self.assertEqual(len(feedbacks), 10)

        # レスポンス結果の再現
        response_body = {
            "DM"           : "evaluation insert DM",
            "New User"     : "",
            "Follow"       : "",
            "Update_model" : "OK"
        }
        response_body_encode = json.dumps(response_body).encode()
        # レスポンス結果のの照合
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, response_body_encode)

if __name__ == '__main__':
    unittest.main()