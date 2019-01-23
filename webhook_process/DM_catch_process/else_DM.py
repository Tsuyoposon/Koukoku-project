# DMで「その他のメッセージ」が来た時の処理
# 送信内容が間違っていることを警告
# アラートメッセージをDMで送る

# python-twitter用
import twitter
# API処理用
from flask import Flask, request
import json, os, requests

def process(twitter_account_auth, request, respon_json):
    #警告文を送信
    twitter_ID = request.json["direct_message_events"][0]["message_create"]["sender_id"]
    alert_string = "メッセージが間違っています\n" + \
        "「登録」「推薦」「評価」のいずれかを入力してください"
        
    sent_DM(alert_string, twitter_ID, twitter_account_auth)

    #レスポンス用メッセージ
    respon_json["DM"] = "else DM event"
    return json.dumps(respon_json)


# 分割した関数
def sent_DM(sent_text, sent_userID, twitter_account_auth):
    DM_sent_body = {
        "event": {
            "type": "message_create",
            "message_create": {
                "target": {
                    "recipient_id": sent_userID
                },
                "message_data": {
                    "text": sent_text
                }
            }
        }
    }
    response = requests.post(
        "https://api.twitter.com/1.1/direct_messages/events/new.json",
        auth=twitter_account_auth,
        data=json.dumps(DM_sent_body)
    )
