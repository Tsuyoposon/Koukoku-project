# python-twitter用 wastonAPI用
import twitter
from watson_developer_cloud import PersonalityInsightsV3
# API処理用
from flask import Flask, request
import json, os

def DM_catch(twitter_account, watson_personal_API, request, respon_json):
    # timelineの文章
    DM_user_linked_timeline = ""
    # オウム返しでDMを返す
    twitter_account.PostDirectMessage(
        request.json["direct_message_events"][0]["message_create"]["message_data"]["text"],
        request.json["direct_message_events"][0]["message_create"]["sender_id"]
    )
    # 返信を”Get DM”に書き換える
    respon_json["status"] = "Get DM"


    # 相手のツイート10件を取得
    DM_user_timeline = twitter_account.GetUserTimeline(
        request.json["direct_message_events"][0]["message_create"]["sender_id"],
        count=10
    )
    for DM_user_tweet in DM_user_timeline:
        DM_user_linked_timeline += DM_user_tweet.text

    # watsonにテキストを送る
    watson_renponse = watson_personal_API.profile(
        DM_user_linked_timeline,
        content_type="text/plain",
        accept="application/json",
        content_language="ja"
    )

    print(json.dumps(watson_renponse, indent=2))


    return json.dumps(respon_json)

def follow_catch(twitter_account, watson_personal_API, request, respon_json):
    # 返信を”Get follow”に書き換える
    respon_json["status"] = "Get follow"

    print(json.dumps(request.json, indent=2))

    return json.dumps(respon_json)
