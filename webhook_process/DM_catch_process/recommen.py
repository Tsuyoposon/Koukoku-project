# DMで「推薦」が来た時の処理
# DMを送ってきたアカウントの性格(follow_catch.pyで収集済み)から推薦を行う
# 推薦結果(上位5件)をDMで送る

# python-twitter用
import twitter
# API処理用
from flask import Flask, request
import json, os, requests
# DB用のモデル
from DB.koukokuDB.models import User
from DB.koukokuDB.models import Recommen_item
from DB.koukokuDB.database import db
# sagemakerの推薦モデルを利用
import boto3
# 乱数生成
import random
# twitter_IDをハッシュ化
import hashlib


def process(twitter_account_auth, request, respon_json):
    # DMを送ったユーザの情報をDBから取得
    twitter_ID = request.json["direct_message_events"][0]["message_create"]["sender_id"]
    user = db.session.query(User).filter_by(
        twitter_userid_hash=hashlib.sha1(bytearray(twitter_ID, 'UTF-8')).hexdigest()
        ).first()
    # もしユーザが見つからなかったら
    if user is None:
        sent_DM("「登録」が完了していません", twitter_ID, twitter_account_auth)
        # 推薦ができなかった
        respon_json["DM"] = "Not Recommen DM"
        return json.dumps(respon_json)

    user_byte_data = user.all_params()
    # boto3でsagemakerのクライアントを作成
    client = boto3.client('sagemaker-runtime')
    boto3_response = client.invoke_endpoint(
        EndpointName='tensorflow-poster-endpoint',
        Body=user_byte_data.encode(),
        ContentType='text/csv',
        Accept='application/json'
    )
    # 推薦結果をソート
    recommen_sent_string = recommen_sort(boto3_response['Body'])

    # 上位5件をDMで送信
    sent_DM(recommen_sent_string, twitter_ID, twitter_account_auth)
    # 推薦ができた
    respon_json["DM"] = "Recommen DM"
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

def recommen_sort(boto3_response):
    # 推薦結果をソート
    boto3_response_json = json.load(boto3_response)
    recommen_result_json = boto3_response_json['result']['classifications'][0]['classes']
    recommen_sort_result = sorted(recommen_result_json, key=lambda x:x['score'], reverse=True)
    # 推薦アイテムのロード
    recommen_items = Recommen_item.query.all()

    # ランダムに文字を変える(twitterエラー回避用)
    if random.randint(0, 1) == 1:
        recommen_sent_string = ""
    else:
        recommen_sent_string = "「推薦結果」\n"
    for i in range(5):
        recommen_item = recommen_items[int(recommen_sort_result[i]['label'])]
        recommen_sent_string += "「" + chr(ord("①")+i) + recommen_item.recommen_item_name + "」\n"

    return recommen_sent_string
