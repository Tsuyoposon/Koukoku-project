# webhookトークンの生成
import base64, hashlib, hmac
# API処理用
from flask import Flask
from flask import request
import json, os
# python-twitter用 wastonAPI用
import twitter
from watson_developer_cloud import PersonalityInsightsV3
# webhookイベントの時の処理関数
from twitter_receve import webhook_process


app = Flask(__name__)
# twitter操作のための認証
twitter_account = twitter.Api(
    consumer_key=os.environ['TWITTER_CONSUMER'],
    consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
    access_token_key=os.environ['ACCESS_TOKEN'],
    access_token_secret=os.environ['ACCESS_TOKEN_SECRET']
)
# watsonAPIのための認証
watson_personal_API = PersonalityInsightsV3(
    version="2017-10-13",
    username=os.environ['WATSON_UESR_NAME'],
    password=os.environ['WATSON_PASSWORD']
)

# twitterのwebhook設定
@app.route('/webhooks/twitter', methods=['GET'])
def webhook_challenge():

    # 返信用トークンを生成
    twitter_byte = bytearray(os.environ['TWITTER_CONSUMER_SECRET'], "ASCII")
    crc_token_byte = bytearray(request.args.get('crc_token'), "ASCII")
    sha256_hash_digest = hmac.new(twitter_byte, crc_token_byte, hashlib.sha256).digest()
    response = {
        'response_token': 'sha256=' + base64.b64encode(sha256_hash_digest).decode('ASCII')
    }
    # トークンを返信
    return json.dumps(response)


# DMを受け取った時の処理
@app.route('/webhooks/twitter', methods=['POST'])
def webhook_catch():

    # 返信用json
    respon_json = {"status" : "OK"}

    # webhookイベントがユーザにフォローされた時の処理
    if request.json.get("follow_events"):
        return webhook_process.follow_catch(twitter_account, watson_personal_API, request, respon_json)
    # webhookイベントがDMの時の処理
    elif request.json.get("direct_message_events"):
        twitter_account.PostDirectMessage(
            request.json["direct_message_events"][0]["message_create"]["message_data"]["text"],
            request.json["direct_message_events"][0]["message_create"]["sender_id"]
        )
        return webhook_process.DM_catch(twitter_account, request, respon_json)
    # webhookイベントがそれ以外であれば何もしない
    else:
         return json.dumps(respon_json)



if __name__ == "__main__":
    app.run(host='0.0.0.0')
