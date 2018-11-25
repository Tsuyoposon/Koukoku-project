# TwitterアカウントにDMが送られた時の処理

# API処理用
from flask import Flask, request
import json, os, requests
# 「推薦」処理関数
from webhook_process.DM_catch_process import recommen

# DMをもらった時
def process(twitter_account_auth, request, respon_json):
    # 他人からのDMイベントの時
    if request.json["direct_message_events"][0]["message_create"]["sender_id"] != os.environ['MYTWITTER_ACCOUNT_ID']:
        if request.json["direct_message_events"][0]["message_create"]["message_data"]["text"] == "推薦":
            # 「推薦」処理
            return recommen.process(twitter_account_auth, request, respon_json)
        elif request.json["direct_message_events"][0]["message_create"]["message_data"]["text"] == "評価":
            # 「評価」処理
            # return evaluation.process(twitter_account_auth, request, respon_json)
            print("「評価」")
        else:
            # それ以外のメッセージ
            respon_json["DM"] = "else DM event"
            return json.dumps(respon_json)
    else:
        # 自分に対してのDMイベントなので何もしない
        respon_json["DM"] = "My DM event"
        return json.dumps(respon_json)
