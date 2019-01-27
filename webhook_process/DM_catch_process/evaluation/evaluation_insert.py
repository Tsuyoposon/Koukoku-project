# DMで「評価」が来た時の処理
# ①「推薦アイテムのquick-replies」を送る (item_sent)
# ②選択してもらったら「評価(5段階)のquick-replies」を送る (evaluation_sent)
# ③「評価」と「選択されたポスター」と「ユーザid」を評価DBに入れる (evaluation_insert)

# API処理用
from flask import Flask, request
import json, requests
# DB用のモデル
from DB.koukokuDB.models import User
from DB.koukokuDB.models import Feedback
from DB.koukokuDB.database import db
# twitter_IDをハッシュ化
import hashlib
# s3_upload関数
from aws_process import s3_upload
from aws_process import UpdateModelThread
# AWS関連
import boto3
import datetime
from pytz import timezone


def evaluation_insert(twitter_account_auth, request, respon_json):
    # ③評価」と「選択されたポスター」と「ユーザid」を評価DBに入れる
    # twitter_idからuserを検索
    twitter_ID = request.json["direct_message_events"][0]["message_create"]["sender_id"]
    user = db.session.query(User).filter_by(
        twitter_userid_hash=hashlib.sha1(bytearray(twitter_ID, 'UTF-8')).hexdigest()
        ).first()
    # 選択したポスターと評価値を取得
    select_item_hyouka = request.json["direct_message_events"][0]["message_create"]["message_data"]["quick_reply_response"]["metadata"]
    evaluation_data = select_item_hyouka.split(',')
    select_item = int(evaluation_data[0]) + 1
    hyouka = int(evaluation_data[1][-1])

    # 評価結果をinsert(同じアイテムを評価したらupdate)
    check_feedback = Feedback.query.filter_by(user_id=user.id, recommen_item_id=select_item).first()
    if check_feedback is None:
        insert_feedback = Feedback(user.id, select_item, hyouka)
        db.session.add(insert_feedback)
        db.session.commit()
        # 「評価完了」DMを送信
        sent_DM("評価ありがとうございます", twitter_ID, twitter_account_auth)

        #評価が10件たまったら
        feedbacks = Feedback.query.all()
        if len(feedbacks) % 10 == 0:
            # エンドポイントの状態を取得して、現在とのタイムラグを取得
            client = boto3.client('sagemaker')
            response_endpoint = client.list_endpoints(
                MaxResults=1,
                NameContains='tensorflow-poster-endpoint',
            )
            time_lag = datetime.datetime.now(timezone('UTC')) - response_endpoint["Endpoints"][0]["LastModifiedTime"]
            # タイムラグが10分以下であれば or 最初の10件だった時
            print(time_lag)
            if datetime.timedelta(minutes=10) < time_lag or len(feedbacks) == 10:
                s3_upload.process()
                # 時間がかかるため並列
                UpdateModel_Thread = UpdateModelThread.UpdateModelThread()
                UpdateModel_Thread.start()
                respon_json["Update_model"] = "OK"
                respon_json["DM"] = "evaluation insert DM"
                return json.dumps(respon_json)
        else:
            respon_json["DM"] = "evaluation insert DM"
            return json.dumps(respon_json)
    else:
        check_feedback.feedback = hyouka
        db.session.add(check_feedback)
        db.session.commit()
        # 「評価完了」DMを送信
        sent_DM("評価内容を更新しました", twitter_ID, twitter_account_auth)

        respon_json["DM"] = "evaluation update DM"
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
