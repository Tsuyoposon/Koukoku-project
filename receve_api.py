# webhookトークンの生成
import base64, hashlib, hmac
# API処理用
from flask import Flask, request
import json, os
from requests_oauthlib import OAuth1
# python-twitter用 wastonAPI用
import twitter
from watson_developer_cloud import PersonalityInsightsV3

# 自作モジュール
# DMイベントを受けた時の処理関数
from webhook_process import DM_catch
# followイベントを受けた時の処理関数
from webhook_process import follow_catch
# DB用import
import DB.koukokuDB.models
from DB.koukokuDB.database import init_db

app = Flask(__name__)
app.config.from_object('DB.koukokuDB.config.Config')
init_db(app)
# twitter操作のための認証
twitter_account_auth = OAuth1(
    os.environ['TWITTER_CONSUMER'],
    os.environ['TWITTER_CONSUMER_SECRET'],
    os.environ['ACCESS_TOKEN'],
    os.environ['ACCESS_TOKEN_SECRET']
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


# Twitterからイベントを受け取った時の処理
@app.route('/webhooks/twitter', methods=['POST'])
def webhook_catch():

    # 返信用json
    respon_json = {
        "DM"           : "",
        "New User"     : "",
        "Follow"       : "",
        "Update_model" : ""
    }
    # webhookイベントがユーザにフォローされた時の処理
    if request.json.get("follow_events"):
        return follow_catch.process(twitter_account_auth, request, respon_json)
    # webhookイベントがDMの時の処理
    elif request.json.get("direct_message_events"):
        return DM_catch.process(twitter_account_auth, watson_personal_API, request, respon_json)
    # webhookイベントがそれ以外であれば何もしない
    else:
        return json.dumps(respon_json)



if __name__ == "__main__":
    app.run(host='0.0.0.0')
