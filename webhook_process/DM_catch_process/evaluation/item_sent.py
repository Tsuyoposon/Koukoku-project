# DMで「評価」が来た時の処理
# ①「推薦アイテムのquick-replies」を送る (item_sent)
# ②選択してもらったら「評価(5段階)のquick-replies」を送る (evaluation_sent)
# ③「評価」と「選択されたポスター」と「ユーザid」を評価DBに入れる (evaluation_insert)

# API処理用
from flask import Flask, request
import json, requests
# DB用のモデル
from DB.koukokuDB.models import User
from DB.koukokuDB.models import Recommen_item
from DB.koukokuDB.database import db
# twitter_IDをハッシュ化
import hashlib

def item_sent(twitter_account_auth, request, respon_json):
    # DMを送ったユーザの情報をDBから取得
    twitter_ID = request.json["direct_message_events"][0]["message_create"]["sender_id"]
    user = db.session.query(User).filter_by(
        twitter_userid_hash=hashlib.sha1(bytearray(twitter_ID, 'UTF-8')).hexdigest()
        ).first()
    # もしユーザが見つからなかったら
    if user is None:
        sent_DM("「登録」が完了していません", twitter_ID, twitter_account_auth)
        # 推薦ができなかった
        respon_json["DM"] = "evaluation NO DM"
        return json.dumps(respon_json)

    # ①「推薦アイテムのquick-replies」を送る
    # 送るquick-repliesの作成
    recommen_items = Recommen_item.query.all()
    reply_list = []
    for i in range(len(recommen_items)):
        recommen_item_name = recommen_items[i].recommen_item_name.split()
        reply_item = {
            "label"       : recommen_item_name[0],
            "description" : recommen_items[i].recommen_item_name,
            "metadata"    : str(i)
        }
        reply_list.append(reply_item)
    #「取り消し」が選択できる様にする
    reply_item = {
        "label"       : "取り消し",
        "description" : "評価を取り消します",
        "metadata"    : "cancel"
    }
    reply_list.append(reply_item)

    DM_sent_body = {
        "event": {
            "type": "message_create",
            "message_create": {
                "target": {
                    "recipient_id": request.json["direct_message_events"][0]["message_create"]["sender_id"]
                },
                "message_data": {
                    "text": "評価したいポスターを選択してください",
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
        respon_json["DM"] = "evaluation item_sent DM"
        return json.dumps(respon_json)
    else:
        # DMが返信できなかった
        respon_json["DM"] = "Not evaluation item_sent DM"
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
