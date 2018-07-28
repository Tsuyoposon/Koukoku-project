# python-twitter用 wastonAPI用
import twitter
from watson_developer_cloud import PersonalityInsightsV3
# API処理用
from flask import Flask, request
import json, os, requests
# DB用のモデル
from twitter_receve.koukokuDB.models import User
from twitter_receve.koukokuDB.models import UserStatus
from twitter_receve.koukokuDB.database import db

# DMをもらった時
def DM_catch(twitter_account_auth, request, respon_json):
    # print(json.dumps(request.json, indent=2))
    if request.json["direct_message_events"][0]["message_create"]["sender_id"] != os.environ['MYTWITTER_ACCOUNT_ID']:
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
        respon_json["status"] = "Return DM"
        return json.dumps(respon_json)
    else:
        # 返信を”Get DM”に書き換える
        respon_json["status"] = "Get DM"
        return json.dumps(respon_json)


# フォローされた時
def follow_catch(twitter_account_auth, watson_personal_API, request, respon_json):

    print(json.dumps(request.json, indent=2))
    # 自分が相手をフォローしているか確認する
    friendships_result = requests.get(
        "https://api.twitter.com/1.1/friendships/lookup.json",
        auth=twitter_account_auth,
        params={
            "user_id" : request.json["follow_events"][0]["source"]["id"],
        }
    )
    print(json.dumps(friendships_result.json(), indent=2))
    if "following" not in friendships_result.json()[0]["connections"]:
        # もし相手をフォローしていなかったらフォロー返しをする
        requests.post(
            "https://api.twitter.com/1.1/friendships/create.json",
            auth=twitter_account_auth,
            params={
                "user_id" : request.json["follow_events"][0]["source"]["id"],
                "follow"  : "true"
            }
        )
        respon_json["Follow"] = "OK"
    else:
        respon_json["Follow"] = "NO"

    # DB内に登録しようとしているユーザが既にいるのか確認する
    check_user = User.query.filter_by(twitter_userid=request.json["follow_events"][0]["source"]["id"]).first()
    if check_user is None:
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
        user = User(
            request.json["follow_events"][0]["source"]["id"],
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
        # ”ユーザ情報をDBに書き込んだ”という返信
        respon_json["New User"] = "OK"
        respon_json["status"] = "Get follow"
        return json.dumps(respon_json)
    else:
        # ”ユーザ情報を書き込んでいない”という返信
        respon_json["New User"] = "NO"
        respon_json["status"] = "Get follow"
        return json.dumps(respon_json)
