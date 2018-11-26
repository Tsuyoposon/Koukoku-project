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
        # 推薦結果を送る時
        sent_message = "1-A19 AmbientLetter：わからないスペルをこっそり知るための筆記検出および文字提示手法\n"\
            "1-A04 ニオイセンサーによるニオイの可視化と官能試験との相関性\n"\
            "1-A02 ProtoHole: 穴と音響センシングを用いたインタラクティブな３Dプリントオブジェクトの提案\n"\
            "1-A06 VRショールームのためのVR酔いを抑えた歩行移動インタフェース\n"\
            "1-A07 スマートウォッチを用いたモノづくりの動作検出に対する試み"
        if catch_json["event"]["message_create"]["target"]["recipient_id"] == os.environ['TEST_ACCOUNT_ID'] and \
        sent_message in catch_json["event"]["message_create"]["message_data"]["text"]:
            return MockResponse({}, 200)
        # quick-replies(推薦アイテム)を送信する時
        sent_first_description = "1-A02 ProtoHole: 穴と音響センシングを用いたインタラクティブな３Dプリントオブジェクトの提案"
        if catch_json["event"]["message_create"]["target"]["recipient_id"] == os.environ['TEST_ACCOUNT_ID'] and \
        catch_json["event"]["message_create"]["message_data"]["quick_reply"]["options"][0]["description"] == sent_first_description:
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
