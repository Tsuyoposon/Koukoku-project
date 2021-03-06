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
    # フォロー返しをする時のrequest(POST)
    if args[0] == "https://api.twitter.com/1.1/friendships/create.json":
        if kwargs["params"]["user_id"] == os.environ['TEST_ACCOUNT_ID']:
            return MockResponse({}, 200)
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
    # フォロー返しをする時のrequest(POST)
    if args[0] == "https://api.twitter.com/1.1/friendships/create.json":
        if kwargs["params"]["user_id"] == os.environ['TEST_ACCOUNT_ID']:
            return MockResponse({}, 200)
        return MockResponse({}, 500)
    # フォローしている情報を取得する時のrequest(GET)
    elif args[0] == "https://api.twitter.com/1.1/friendships/lookup.json":
        if kwargs["params"]["user_id"] == os.environ['TEST_ACCOUNT_ID']:
            with open("test_code/test_json/friendship_check.json", "r") as friendship_check_json_file:
                friendship_check_json = json.load(friendship_check_json_file)
                friendship_check_json[0]["connections"] = ["following_requested","followed_by"]
            return MockResponse(friendship_check_json, 200)
        return MockResponse({}, 500)
    return MockResponse({}, 404)
# 3回目用のtwitter_API
def mocked_twitter_API_3(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code
        def json(self):
            return self.json_data
    # フォロー返しをする時のrequest(POST)
    if args[0] == "https://api.twitter.com/1.1/friendships/create.json":
        if kwargs["params"]["user_id"] == os.environ['TEST_ACCOUNT_ID']:
            return MockResponse({}, 200)
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
