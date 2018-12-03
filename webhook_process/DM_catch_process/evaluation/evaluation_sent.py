# DMで「評価」が来た時の処理
# ①「推薦アイテムのquick-replies」を送る (item_sent)
# ②選択してもらったら「評価(5段階)のquick-replies」を送る (evaluation_sent)
# ③「評価」と「選択されたポスター」と「ユーザid」を評価DBに入れる (evaluation_insert)

# API処理用
from flask import Flask, request
import json, requests

def evaluation_sent(twitter_account_auth, request, respon_json):
    # ②選択してもらったら「評価(5段階)のquick-replies」を送る
    # 送るquick-repliesの作成
    select_item = request.json["direct_message_events"][0]["message_create"]["message_data"]["quick_reply_response"]["metadata"]
    reply_list = [
        {
            "label"       : "1",
            "description" : "とてもつまらない",
            "metadata"    : select_item + ",hyouka-1"
        },
        {
            "label"       : "2",
            "description" : "つまらない",
            "metadata"    : select_item + ",hyouka-2"
        },
        {
            "label"       : "3",
            "description" : "普通",
            "metadata"    : select_item + ",hyouka-3"
        },
        {
            "label"       : "4",
            "description" : "良かった",
            "metadata"    : select_item + ",hyouka-4"
        },
        {
            "label"       : "5",
            "description" : "とても良かった",
            "metadata"    : select_item + ",hyouka-5"
        }
    ]
    DM_sent_body = {
        "event": {
            "type": "message_create",
            "message_create": {
                "target": {
                    "recipient_id": request.json["direct_message_events"][0]["message_create"]["sender_id"]
                },
                "message_data": {
                    "text": "ポスターの評価を選択してください",
                    "quick_reply": {
                        "type": "options",
                        "options": reply_list
                    }
                }
            }
        }
    }
    # quick-repliesを送信
    response = requests.post(
        "https://api.twitter.com/1.1/direct_messages/events/new.json",
        auth=twitter_account_auth,
        data=json.dumps(DM_sent_body)
    )
    if response.status_code == 200:
        # DMが返信できた
        respon_json["DM"] = "evaluation evaluation_sent DM"
        return json.dumps(respon_json)
    else:
        # DMが返信できなかった
        respon_json["DM"] = "Not evaluation evaluation_sent DM"
        return json.dumps(respon_json)
