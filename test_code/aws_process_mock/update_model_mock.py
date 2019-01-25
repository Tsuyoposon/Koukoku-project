from unittest import mock
import json, os
from io import StringIO
import datetime
from pytz import timezone, utc

# mocked_update_modelの動作を再現
def mocked_update_model():
    return 1

def boto3_resource(*args, **kwargs):
    class MockBucket:
        def Bucket(*args, **kwargs):
            class MockUploadFile:
                def upload_file(*args, **kwargs):
                    return
            if args[0] == os.environ['BUCKET_NAME']:
                return MockUploadFile
            return None
        def list_endpoints(*args, **kwargs):
            with open("test_code/test_json/endpoint.json", "r") as endpoint_json_file:
                endpoint_json = json.load(endpoint_json_file)
            endpoint_json["Endpoints"][0]["LastModifiedTime"] = datetime.datetime(2019, 1, 25, 5, 13, 30, 29000, timezone('UTC'))
            return endpoint_json
    if args[0] == "s3":
        return MockBucket
    elif args[0] == "sagemaker":
        return MockBucket
    return None

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
        # 警告メッセージが届いた時
        if catch_json["event"]["message_create"]["target"]["recipient_id"] == os.environ['TEST_ACCOUNT_ID'] and \
        catch_json["event"]["message_create"]["message_data"]["text"] is not None:
            return MockResponse({}, 200)
