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
