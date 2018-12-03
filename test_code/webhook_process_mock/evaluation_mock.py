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
        # quick-replies(推薦アイテム)を送信する時
        sent_first_description = "とてもつまらない"
        if catch_json["event"]["message_create"]["target"]["recipient_id"] == os.environ['TEST_ACCOUNT_ID'] and \
        catch_json["event"]["message_create"]["message_data"]["quick_reply"]["options"][0]["description"] == sent_first_description:
            return MockResponse({}, 200)
        return MockResponse({}, 500)
