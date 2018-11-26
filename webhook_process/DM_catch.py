# TwitterアカウントにDMが送られた時の処理

# API処理用
from flask import Flask, request
import json, os, requests
# 「推薦」処理関数
from webhook_process.DM_catch_process import recommen
# 「評価」処理関数
from webhook_process.DM_catch_process import evaluation


# DMをもらった時
def process(twitter_account_auth, request, respon_json):
    # 他人からのDMイベントの時
    if request.json["direct_message_events"][0]["message_create"]["sender_id"] != os.environ['MYTWITTER_ACCOUNT_ID']:
        if request.json["direct_message_events"][0]["message_create"]["message_data"]["text"] == "推薦":
            # 「推薦」が送られた処理
            return recommen.process(twitter_account_auth, request, respon_json)
        elif request.json["direct_message_events"][0]["message_create"]["message_data"]["text"] == "評価":
            # 「評価」が送られた処理
            return evaluation.item_sent(twitter_account_auth, request, respon_json)
        elif "quick_reply_response" in request.json["direct_message_events"][0]["message_create"]["message_data"]:
            # 「評価によるquick-replies」が送られた処理
            if "hyouka" not in request.json["direct_message_events"][0]["message_create"]["message_data"]["quick_reply_response"]["metadata"]:
                # 推薦アイテムのquick-repliesの時
                return evaluation.evaluation_sent(twitter_account_auth, request, respon_json)
            else:
                # 評価のquick-repliesの時
                print("evaluation input DM")
                respon_json["DM"] = "evaluation input DM"
                return json.dumps(respon_json)
        else:
            # それ以外のメッセージ
            print(json.dumps(request.json, indent=2))
            respon_json["DM"] = "else DM event"
            return json.dumps(respon_json)
    else:
        # 自分に対してのDMイベントなので何もしない
        respon_json["DM"] = "My DM event"
        return json.dumps(respon_json)
