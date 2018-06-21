import unittest, os
from unittest import mock
# twitter_receve用テストコード
import receve_api
from flask import Flask, request
import json
from watson_developer_cloud import PersonalityInsightsV3

def mocked_twitter_API(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code
        def json(self):
            return self.json_data
    # DMを送る時のrequest
    if args[0] == "https://api.twitter.com/1.1/direct_messages/events/new.json":
        catch_json = json.loads(kwargs["data"])
        if catch_json["event"]["message_create"]["target"]["recipient_id"] == os.environ['TEST_ACCOUNT_ID'] and \
        catch_json["event"]["message_create"]["message_data"]["text"] == "こんにちは！":
            return MockResponse({}, 200)
        return MockResponse({}, 500)
    # フォロー返しをする時のrequest
    elif args[0] == "https://api.twitter.com/1.1/friendships/create.json":
        if kwargs["params"]["user_id"] == os.environ['TEST_ACCOUNT_ID']:
            return MockResponse({}, 200)
        return MockResponse({}, 500)
    # ツイートを取得する時のrequest
    elif args[0] == "https://api.twitter.com/1.1/statuses/user_timeline.json":
        if kwargs["params"]["user_id"] == os.environ['TEST_ACCOUNT_ID']:
            with open("test_code/test_json/tweet_timeline.json", "r") as tweet_timeline_json_file:
                tweet_timeline_json = json.load(tweet_timeline_json_file)
            return MockResponse(tweet_timeline_json, 200)
        return MockResponse({}, 500)

    return MockResponse({}, 404)

def mocked_watson_API(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code
        def json(self):
            return self.json_data

    if args[0] == "こんばんは":
        with open("test_code/test_json/watson_result.json", "r") as watson_result_json_file:
            watson_result_json = json.load(watson_result_json_file)
        return watson_result_json
    return MockResponse({}, 500)

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

    @mock.patch('requests.post', side_effect=mocked_twitter_API)
    def test_twitter_DM(self, mock_post):
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
        response_body = {"status" : "Get DM"}
        response_body_encode = json.dumps(response_body).encode()
        # レスポンス結果のの照合
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, response_body_encode)

    @mock.patch('requests.get', side_effect=mocked_twitter_API)
    @mock.patch('requests.post', side_effect=mocked_twitter_API)
    @mock.patch('watson_developer_cloud.PersonalityInsightsV3.profile', side_effect=mocked_watson_API)
    def test_twitter_follow(self, mock_get, mock_post, mock_watson):
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
        response_body = {"status" : "Get follow"}
        response_body_encode = json.dumps(response_body).encode()
        # レスポンス結果のの照合
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, response_body_encode)


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
