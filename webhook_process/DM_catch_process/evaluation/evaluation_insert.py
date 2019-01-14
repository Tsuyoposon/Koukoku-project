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
from aws_process import update_model


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
        # 10件評価が溜まったらモデル更新
        feedbacks = Feedback.query.all()
        if len(feedbacks) % 10 == 0:
            s3_upload.process()
            update_model.process()
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

        respon_json["DM"] = "evaluation update DM"
        return json.dumps(respon_json)
