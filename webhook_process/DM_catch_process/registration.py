# DMで「登録」が来た時の処理
# フォローしたアカウントのツイート文を取得
# ツイート文をWatsonAPIに投げて性格情報を取得
# DBに保存

# python-twitter用
import twitter
# watsonAPI用
from watson_developer_cloud import PersonalityInsightsV3
# API処理用
from flask import Flask, request
import json, os, requests
# DB用のモデル
from DB.koukokuDB.models import User
from DB.koukokuDB.database import db
# twitter_IDをハッシュ化
import hashlib


def process(twitter_account_auth, watson_personal_API, request, respon_json):
    # DB内に登録しようとしているユーザが既にいるのか確認する
    twitter_ID = request.json["direct_message_events"][0]["message_create"]["sender_id"]
    twitter_ID_hash = hashlib.sha1(bytearray(twitter_ID, 'UTF-8')).hexdigest()
    check_user = User.query.filter_by(twitter_userid_hash=twitter_ID_hash).first()
    if check_user is None:
        # 相手のツイート50件を取得
        DM_user_timeline = requests.get(
            "https://api.twitter.com/1.1/statuses/user_timeline.json",
            auth=twitter_account_auth,
            params={
                "user_id" : twitter_ID,
                "count"   : 50
            }
        )
        # もしツイートを取得する許可がないなら(相互フォローしていない)
        if "error" in DM_user_timeline.json():
            # フォローを許可する様に警告
            sent_DM("このアカウントに対してフォローをしてください(相互フォロー状態でないとツイートが取得できません)", twitter_ID, twitter_account_auth)
            respon_json["New User"] = "NO"
            return json.dumps(respon_json)

        # timelineの文章
        DM_user_linked_timeline = ""
        for DM_user_tweet in DM_user_timeline.json():
            DM_user_linked_timeline += DM_user_tweet["text"]
        if len(DM_user_linked_timeline) < 100:
            # 「登録ができない」DMを送信
            sent_DM("ツイート文字数が少ないため登録できません", twitter_ID, twitter_account_auth)
            respon_json["New User"] = "NO"
            return json.dumps(respon_json)
        # watsonにツイート50件を送る
        watson_renponse = watson_personal_API.profile(
            DM_user_linked_timeline,
            content_type="text/plain",
            accept="application/json",
            content_language="ja"
        )
        # フォローしたユーザの性格情報をいれる
        insert_user(watson_renponse, twitter_ID)

        # 「登録完了」DMを送信
        sent_DM("登録が完了しました", twitter_ID, twitter_account_auth)
        # もしツイート文字数が「15文字×50ツイート=750文字」以下であれば警告
        if len(DM_user_linked_timeline) < 750:
            # 「登録完了」DMを送信
            sent_DM("※ツイート文字数が少なかったため、正確な推薦結果が出ない可能性があります", twitter_ID, twitter_account_auth)
        # ”ユーザ情報をDBに書き込んだ”という返信
        respon_json["New User"] = "OK"
        return json.dumps(respon_json)
    else:
        # 「登録済み」DMを送信
        sent_DM("すでに登録済みです", twitter_ID, twitter_account_auth)
        # ”ユーザ情報を書き込んでいない”という返信
        respon_json["New User"] = "NO"
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

def insert_user(watson_renponse, twitter_ID):
    user = User(
        hashlib.sha1(bytearray(twitter_ID, 'UTF-8')).hexdigest(),
        watson_renponse["personality"][0]["percentile"],
        watson_renponse["personality"][0]["children"][0]["percentile"],
        watson_renponse["personality"][0]["children"][1]["percentile"],
        watson_renponse["personality"][0]["children"][2]["percentile"],
        watson_renponse["personality"][0]["children"][3]["percentile"],
        watson_renponse["personality"][0]["children"][4]["percentile"],
        watson_renponse["personality"][0]["children"][5]["percentile"],
        watson_renponse["personality"][1]["percentile"],
        watson_renponse["personality"][1]["children"][0]["percentile"],
        watson_renponse["personality"][1]["children"][1]["percentile"],
        watson_renponse["personality"][1]["children"][2]["percentile"],
        watson_renponse["personality"][1]["children"][3]["percentile"],
        watson_renponse["personality"][1]["children"][4]["percentile"],
        watson_renponse["personality"][1]["children"][5]["percentile"],
        watson_renponse["personality"][2]["percentile"],
        watson_renponse["personality"][2]["children"][0]["percentile"],
        watson_renponse["personality"][2]["children"][1]["percentile"],
        watson_renponse["personality"][2]["children"][2]["percentile"],
        watson_renponse["personality"][2]["children"][3]["percentile"],
        watson_renponse["personality"][2]["children"][4]["percentile"],
        watson_renponse["personality"][2]["children"][5]["percentile"],
        watson_renponse["personality"][3]["percentile"],
        watson_renponse["personality"][3]["children"][0]["percentile"],
        watson_renponse["personality"][3]["children"][1]["percentile"],
        watson_renponse["personality"][3]["children"][2]["percentile"],
        watson_renponse["personality"][3]["children"][3]["percentile"],
        watson_renponse["personality"][3]["children"][4]["percentile"],
        watson_renponse["personality"][3]["children"][5]["percentile"],
        watson_renponse["personality"][4]["percentile"],
        watson_renponse["personality"][4]["children"][0]["percentile"],
        watson_renponse["personality"][4]["children"][1]["percentile"],
        watson_renponse["personality"][4]["children"][2]["percentile"],
        watson_renponse["personality"][4]["children"][3]["percentile"],
        watson_renponse["personality"][4]["children"][4]["percentile"],
        watson_renponse["personality"][4]["children"][5]["percentile"],
        watson_renponse["needs"][0]["percentile"],
        watson_renponse["needs"][1]["percentile"],
        watson_renponse["needs"][2]["percentile"],
        watson_renponse["needs"][3]["percentile"],
        watson_renponse["needs"][4]["percentile"],
        watson_renponse["needs"][5]["percentile"],
        watson_renponse["needs"][6]["percentile"],
        watson_renponse["needs"][7]["percentile"],
        watson_renponse["needs"][8]["percentile"],
        watson_renponse["needs"][9]["percentile"],
        watson_renponse["needs"][10]["percentile"],
        watson_renponse["needs"][11]["percentile"],
        watson_renponse["values"][0]["percentile"],
        watson_renponse["values"][1]["percentile"],
        watson_renponse["values"][2]["percentile"],
        watson_renponse["values"][3]["percentile"],
        watson_renponse["values"][4]["percentile"]
    )
    db.session.add(user)
    db.session.commit()
