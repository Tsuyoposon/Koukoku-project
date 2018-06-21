import unittest
# twitter_receve用テストコード
import receve_api
from flask import Flask, request
import json


class TestTwitterReceve(unittest.TestCase):

    def setUp(self):
        self.app = receve_api.app.test_client()

    def test_webhook_challenge(self):
        # twitterからのリクエストAPIを再現
        response = self.app.get("/webhooks/twitter?crc_token=foo")
        # レスポンス結果の再現
        response_body = {
            "response_token": "sha256=D1UXbLq0ougTycgcBn9pWDTS2jarXz/3wS5yVJniPFY="
        }
        response_body_encode = json.dumps(response_body).encode()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, response_body_encode)

    def test_twitter_DM(self):
        # DMがきた時のjsonをロード
        with open("test_code/test_json/direct_message_events.json", "r") as DM_event_json_file:
            DM_event_json = json.load(DM_event_json_file)
        # twitterからのDMイベントのAPIを再現
        response = self.app.post(
            "/webhooks/twitter",
            content_type='application/json',
            data=json.dumps(DM_event_json)
        )

        # レスポンス結果の再現
        response_body = {"status" : "Get DM"}
        response_body_encode = json.dumps(response_body).encode()
        # レスポンス結果のの照合
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, response_body_encode)

    # def test_twitter_follow(self):
    #     # followがきた時のjsonをロード
    #     with open("test_code/test_json/follow_event.json", "r") as follow_event_json_file:
    #         follow_event_json = json.load(follow_event_json_file)
    #     # twitterからのfollowイベントのAPIを再現
    #     response = self.app.post(
    #         "/webhooks/twitter",
    #         content_type='application/json',
    #         data=json.dumps(follow_event_json)
    #     )
    #
    #     # レスポンス結果の再現
    #     response_body = {"status" : "Get follow"}
    #     response_body_encode = json.dumps(response_body).encode()
    #     # レスポンス結果のの照合
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.data, response_body_encode)


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
        response_body = {"status" : "OK"}
        response_body_encode = json.dumps(response_body).encode()
        # レスポンス結果のの照合
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, response_body_encode)

if __name__ == '__main__':
    unittest.main()
