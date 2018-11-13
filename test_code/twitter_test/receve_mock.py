from unittest import mock
import json, os
from io import StringIO

# twitterAPIの動作を再現
def mocked_twitter_API(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code
        def json(self):
            return self.json_data
    # DMを送る時のrequest(POST)
    if args[0] == "https://api.twitter.com/1.1/direct_messages/events/new.json":
        catch_json = json.loads(kwargs["data"])
        if catch_json["event"]["message_create"]["target"]["recipient_id"] == os.environ['TEST_ACCOUNT_ID'] and \
        catch_json["event"]["message_create"]["message_data"]["text"] == "こんにちは！":
            return MockResponse({}, 200)
        return MockResponse({}, 500)
    # フォロー返しをする時のrequest(POST)
    elif args[0] == "https://api.twitter.com/1.1/friendships/create.json":
        if kwargs["params"]["user_id"] == os.environ['TEST_ACCOUNT_ID']:
            return MockResponse({}, 200)
        return MockResponse({}, 500)
    # ツイートを取得する時のrequest(GET)
    elif args[0] == "https://api.twitter.com/1.1/statuses/user_timeline.json":
        if kwargs["params"]["user_id"] == os.environ['TEST_ACCOUNT_ID']:
            with open("test_code/test_json/tweet_timeline.json", "r") as tweet_timeline_json_file:
                tweet_timeline_json = json.load(tweet_timeline_json_file)
            return MockResponse(tweet_timeline_json, 200)
        return MockResponse({}, 500)
    # フォローしている情報を取得する時のrequest(GET)
    elif args[0] == "https://api.twitter.com/1.1/friendships/lookup.json":
        if kwargs["params"]["user_id"] == os.environ['TEST_ACCOUNT_ID']:
            with open("test_code/test_json/friendship_check.json", "r") as friendship_check_json_file:
                friendship_check_json = json.load(friendship_check_json_file)
            return MockResponse(friendship_check_json, 200)
        return MockResponse({}, 500)
    return MockResponse({}, 404)
# 2回目用のtwitter_API
def mocked_twitter_API_2(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code
        def json(self):
            return self.json_data
    # DMを送る時のrequest(POST)
    if args[0] == "https://api.twitter.com/1.1/direct_messages/events/new.json":
        catch_json = json.loads(kwargs["data"])
        if catch_json["event"]["message_create"]["target"]["recipient_id"] == os.environ['TEST_ACCOUNT_ID'] and \
        catch_json["event"]["message_create"]["message_data"]["text"] == "こんにちは！":
            return MockResponse({}, 200)
        return MockResponse({}, 500)
    # フォロー返しをする時のrequest(POST)
    elif args[0] == "https://api.twitter.com/1.1/friendships/create.json":
        if kwargs["params"]["user_id"] == os.environ['TEST_ACCOUNT_ID']:
            return MockResponse({}, 200)
        return MockResponse({}, 500)
    # ツイートを取得する時のrequest(GET)
    elif args[0] == "https://api.twitter.com/1.1/statuses/user_timeline.json":
        if kwargs["params"]["user_id"] == os.environ['TEST_ACCOUNT_ID']:
            with open("test_code/test_json/tweet_timeline.json", "r") as tweet_timeline_json_file:
                tweet_timeline_json = json.load(tweet_timeline_json_file)
            return MockResponse(tweet_timeline_json, 200)
        return MockResponse({}, 500)
    # フォローしている情報を取得する時のrequest(GET)
    elif args[0] == "https://api.twitter.com/1.1/friendships/lookup.json":
        if kwargs["params"]["user_id"] == os.environ['TEST_ACCOUNT_ID']:
            with open("test_code/test_json/friendship_check.json", "r") as friendship_check_json_file:
                friendship_check_json = json.load(friendship_check_json_file)
                friendship_check_json[0]["connections"] = ["following","followed_by"]
            return MockResponse(friendship_check_json, 200)
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
# 推薦エンドポイントの動作を再現
def boto3_client(*args, **kwargs):
    class MockClient:
        def invoke_endpoint(*args, **kwargs):
            with open("test_code/test_json/boto3_client.json", "r") as boto3_client_json_file:
                boto3_client_Body_json = boto3_client_json_file.read()
            boto3_client_json = { "Body" : StringIO(boto3_client_Body_json) }
            return boto3_client_json
    if args[0] == "sagemaker-runtime":
        return MockClient
    return None
