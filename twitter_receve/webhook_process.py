# python-twitter用 wastonAPI用
import twitter
from watson_developer_cloud import PersonalityInsightsV3
# API処理用
from flask import Flask, request
import json, os, requests
# DB用のモデル
from twitter_receve.koukokuDB.models import User
from twitter_receve.koukokuDB.database import db

# DMをもらった時
def DM_catch(twitter_account_auth, request, respon_json):

    # DM返信用のjsonを作成
    DM_sent_body = {
        "event": {
            "type": "message_create",
            "message_create": {
                "target": {
                    "recipient_id": request.json["direct_message_events"][0]["message_create"]["sender_id"]
                },
                "message_data": {
                    "text": request.json["direct_message_events"][0]["message_create"]["message_data"]["text"]
                }
            }
        }
    }
    # オウム返しでDMを返す
    requests.post(
        "https://api.twitter.com/1.1/direct_messages/events/new.json",
        auth=twitter_account_auth,
        data=json.dumps(DM_sent_body)
    )

    # 返信を”Get DM”に書き換える
    respon_json["status"] = "Get DM"
    return json.dumps(respon_json)


# フォローされた時
def follow_catch(twitter_account_auth, watson_personal_API, request, respon_json):

    # フォロー返しをする
    requests.post(
        "https://api.twitter.com/1.1/friendships/create.json",
        auth=twitter_account_auth,
        params={
            "user_id" : request.json["follow_events"][0]["source"]["id"],
            "follow"  : "true"
        }
    )

    # 相手のツイート10件を取得
    DM_user_timeline = requests.get(
        "https://api.twitter.com/1.1/statuses/user_timeline.json",
        auth=twitter_account_auth,
        params={
            "user_id" : request.json["follow_events"][0]["source"]["id"],
            "count"   : 10
        }
    )

    # timelineの文章
    DM_user_linked_timeline = ""
    for DM_user_tweet in DM_user_timeline.json():
        DM_user_linked_timeline += DM_user_tweet["text"]

    # watsonにテキストを送る
    watson_renponse = watson_personal_API.profile(
        DM_user_linked_timeline,
        content_type="text/plain",
        accept="application/json",
        content_language="ja"
    )

    # フォローしたユーザの性格情報をいれる
    user = User(request.json["follow_events"][0]["source"]["id"])
    db.session.add(user)
    db.session.commit()

    # 返信を”Get follow”に書き換える
    respon_json["status"] = "Get follow"
    return json.dumps(respon_json)
