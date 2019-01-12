# Twitterアカウントに対してfollowされた時の処理
# フォロー返しをする

# python-twitter用
import twitter
# watsonAPI用
from watson_developer_cloud import PersonalityInsightsV3
# API処理用
from flask import Flask, request
import json, os, requests
# DB用のモデル
from DB.koukokuDB.models import User
# twitter_IDをハッシュ化
import hashlib

# フォローされた時
def process(twitter_account_auth, request, respon_json):
    if request.json["follow_events"][0]["source"]["id"] != os.environ['MYTWITTER_ACCOUNT_ID']:
        twitter_ID = request.json["follow_events"][0]["source"]["id"]
        # 自分が相手をフォローしているか確認する
        friendships_result = requests.get(
            "https://api.twitter.com/1.1/friendships/lookup.json",
            auth=twitter_account_auth,
            params={
                "user_id" : twitter_ID,
            }
        )
        if "following" not in friendships_result.json()[0]["connections"] and \
        "following_requested" not in friendships_result.json()[0]["connections"]:
            # もし相手をフォローしていなない　かつ
            # 相手にフォローリクエスト中でないならフォロー返しをする
            requests.post(
                "https://api.twitter.com/1.1/friendships/create.json",
                auth=twitter_account_auth,
                params={
                    "user_id" : twitter_ID,
                    "follow"  : "true"
                }
            )
            respon_json["Follow"] = "OK"
            return json.dumps(respon_json)
        else:
            respon_json["Follow"] = "NO"
            return json.dumps(respon_json)
    else:
        # 自分に対してのフォローイベントなので何もしない
        respon_json["Follow"] = "NO"
        return json.dumps(respon_json)
