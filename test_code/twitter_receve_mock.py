from unittest import mock
import json, os

# twitterAPIの動作を再現
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

# watsonAPIの動作を再現
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
