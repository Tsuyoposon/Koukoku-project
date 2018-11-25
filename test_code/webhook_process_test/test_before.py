import unittest, os
from unittest import mock
# twitter_receve用テストコード
import receve_api
from flask import Flask, request
import json
# DB用のimport
from DB.koukokuDB.database import reset_db, init_db, db
from DB.koukokuDB.models import Recommen_item

class TestBefore(unittest.TestCase):
    # test_receve内関数を実行ごとに
    def setUp(self):
        app = Flask(__name__)
        app.config.from_object('DB.koukokuDB.config.Config')
        self.app = receve_api.app.test_client()

    # webhookの登録が正常にできるか確認
    def test_webhook_challenge(self):
        # twitterからのリクエストAPIを再現
        response = self.app.get("/webhooks/twitter?crc_token=foo")
        # レスポンス結果の再現
        if os.environ['ENV'] == "wercker":
            response_body = {
                "response_token": "sha256=D1UXbLq0ougTycgcBn9pWDTS2jarXz/3wS5yVJniPFY="
            }
        else:
            response_body = {
                "response_token": "sha256=ixNpKHq5nOOou0Vviyxnq6OyFiqJCPsF6rzyfIlP/o0="
            }
        response_body_encode = json.dumps(response_body).encode()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, response_body_encode)

    # 推薦アイテムがセットされているか確認
    def test_reset_recommen_items(self):

        app = Flask(__name__)
        app.config.from_object('DB.koukokuDB.config.Config')
        init_db(app)
        # DB挿入結果の照会
        with app.app_context():
            recommen_item = Recommen_item.query.get(1)
        self.assertEqual(recommen_item.recommen_item_name, "1-A02 ProtoHole: 穴と音響センシングを用いたインタラクティブな３Dプリントオブジェクトの提案")


if __name__ == '__main__':
    unittest.main()
