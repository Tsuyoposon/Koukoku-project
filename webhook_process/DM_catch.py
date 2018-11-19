# TwitterアカウントにDMが送られた時の処理
# DMを送ってきたアカウントの性格(follow_catch.pyで収集済み)から推薦を行う
# 推薦結果(上位5件)をDMで送る

# python-twitter用
import twitter
# API処理用
from flask import Flask, request
import json, os, requests
# DB用のモデル
from DB.koukokuDB.models import User
from DB.koukokuDB.models import UserStatus
from DB.koukokuDB.database import db
# sagemakerの推薦モデルを利用
import boto3
# 乱数生成
import random

# DMをもらった時
def process(twitter_account_auth, request, respon_json):
    if request.json["direct_message_events"][0]["message_create"]["sender_id"] != os.environ['MYTWITTER_ACCOUNT_ID']:

        # 推薦処理
        # DMを送ったユーザの情報をDBから取得
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
        recommen_sent_string = recommen_sort(boto3_response['Body'])

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
        response = requests.post(
            "https://api.twitter.com/1.1/direct_messages/events/new.json",
            auth=twitter_account_auth,
            data=json.dumps(DM_sent_body)
        )

        if response.status_code == 200:
            # DMが返信できた
            respon_json["DM"] = "Return DM"
            return json.dumps(respon_json)
        else:
            # DMが返信できなかった
            respon_json["DM"] = "Not sent DM"
            return json.dumps(respon_json)
    else:
        # 自分に対してのDMなので何もしない
        respon_json["DM"] = "My DM event"
        return json.dumps(respon_json)

def recommen_sort(boto3_response):
    # 推薦結果をソート
    boto3_response_json = json.load(boto3_response)
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

    return recommen_sent_string
