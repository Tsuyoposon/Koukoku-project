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
# sagemakerの推薦モデルを利用
import boto3
# 乱数生成
import random

# DMをもらった時
def DM_catch(twitter_account_auth, request, respon_json):
    # print(json.dumps(request.json, indent=2))
    if request.json["direct_message_events"][0]["message_create"]["sender_id"] != os.environ['MYTWITTER_ACCOUNT_ID']:

        # 推薦処理
        # DMを送ったユーザの情報を取得
        user = db.session.query(User).filter_by(
            twitter_userid=request.json["direct_message_events"][0]["message_create"]["sender_id"]
            ).first()
        user_byte_data = user.all_params()
        # boto3でsagemakerのクライアントを作成
        client = boto3.client('sagemaker-runtime')
        boto3_response = client.invoke_endpoint(
            EndpointName='koukoku-recommen-endpoint',
            Body=user_byte_data.encode(),
            ContentType='text/csv',
            Accept='application/json'
        )
        # 推薦結果をソート
        boto3_response_json = json.load(boto3_response['Body'])
        recommen_result_json = boto3_response_json['result']['classifications'][0]['classes']
        recommen_sort_result = sorted(recommen_result_json, key=lambda x:x['score'], reverse=True)
        # 推薦結果上位5件を表示
        recommen_item_list = [
            "1-A02 ProtoHole: 穴と音響センシングを用いたインタラクティブな３Dプリントオブジェクトの提案",
            "1-A03 視覚的でインタラクティブな分類器の構築手法",
            "1-A04 ニオイセンサーによるニオイの可視化と官能試験との相関性",
            "1-A05 プレゼンテーションにおける実空間とオンライン空間の聴衆コンテクストの融合",
            "1-A06 VRショールームのためのVR酔いを抑えた歩行移動インタフェース",
            "1-A07 スマートウォッチを用いたモノづくりの動作検出に対する試み",
            "1-A08 睡眠時間の副次利用によるエンタテインメント価値創出",
            "1-A09 腰背部へのせん断力提示による歩行誘導に関する一検討",
            "1-A10 ユーザ周囲の多種多様な情報機器を「サービス化」するLBSインタラクション",
            "1-A15 実世界人形遊びを拡張する仮想ドールハウス",
            "1-A16 透紙: 紙媒体の質感を拡張する表現手法の提案",
            "1-A17 Pulse shot:心拍情報を用いた写真撮影システムおよび検索システム",
            "1-A19 AmbientLetter：わからないスペルをこっそり知るための筆記検出および文字提示手法",
            "1-A20 ポーチの型紙製作支援システム",
            "1-A21 宿泊者のホテル内での動きの偏りに関して",
            "1-A22 パッチワーク風キルト作成支援システム",
            "1-A23 女性のためのシチュエーションドラマを利用した癒しシステム"
        ]
        # ランダムに文字を変える(twitterエラー回避用)
        if random.randint(0, 1) == 1:
            recommen_sent_string = ""
        else:
            recommen_sent_string = "「推薦結果」\n"
        for i in range(5):
            recommen_sent_string += recommen_item_list[int(recommen_sort_result[i]['label'])] + "\n"

        # 上位5件をDMで送信
        DM_sent_body = {
            "event": {
                "type": "message_create",
                "message_create": {
                    "target": {
                        "recipient_id": request.json["direct_message_events"][0]["message_create"]["sender_id"]
                    },
                    "message_data": {
                        "text": recommen_sent_string
                    }
                }
            }
        }
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

    if request.json["follow_events"][0]["source"]["id"] == os.environ['MYTWITTER_ACCOUNT_ID']:
        # ”ユーザ情報をDBに書き込んだ”という返信
        respon_json["New User"] = "NO"
        respon_json["status"] = "MY follow"
        return json.dumps(respon_json)

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
