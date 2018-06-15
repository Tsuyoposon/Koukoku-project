import base64
import hashlib
import hmac
import json
import os
import twitter
from flask import Flask
from flask import request


app = Flask(__name__)
twitter_account = twitter.Api(
    consumer_key=os.environ['TWITTER_CONSUMER'],
    consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
    access_token_key=os.environ['ACCESS_TOKEN'],
    access_token_secret=os.environ['ACCESS_TOKEN_SECRET']
)

# twitterのwebhook設定
@app.route('/webhooks/twitter', methods=['GET'])
def webhook_challenge():

    # creates HMAC SHA-256 hash from incomming token and your consumer secret
    twitter_byte = bytearray(os.environ['TWITTER_CONSUMER_SECRET'], "ASCII")
    crc_token_byte = bytearray(request.args.get('crc_token'), "ASCII")
    sha256_hash_digest = hmac.new(twitter_byte, crc_token_byte, hashlib.sha256).digest()

    # construct response data with base64 encoded hash
    response = {
    'response_token': 'sha256=' + base64.b64encode(sha256_hash_digest).decode('ASCII')
    }

    # returns properly formatted json response
    return json.dumps(response)


# DMを受け取った時の処理
@app.route('/webhooks/twitter', methods=['POST'])
def DM_catch():

    # 返信用json
    respon_json = {"status" : "OK"}

    # webhookされたイベントがDMの送受信の場合だけ処理する
    if request.json.get("direct_message_events"):
        # オウム返しでDMを返す
        twitter_account.PostDirectMessage(
            request.json["direct_message_events"][0]["message_create"]["message_data"]["text"],
            request.json["direct_message_events"][0]["message_create"]["sender_id"]
        )
        # 返信を”Get DM”に書き換える
        respon_json["status"] = "Get DM"

    return json.dumps(respon_json)



if __name__ == "__main__":
    app.run(host='0.0.0.0')
