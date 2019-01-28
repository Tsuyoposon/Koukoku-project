# TwitterアカウントにDMが送られた時の処理
# DM_event --- 自分が送信したDMイベント(何もしない)
#           |- 利用者が送信したDMイベント --- 「登録」と送信された（ツイートを採取して性格情報を取得＆登録）
#                                      |- 「推薦」と送信された (推薦結果表示)
#                                      |- 「評価」と送信された (推薦アイテムのquick_replyを送信)
#                                      |- quick_replyイベント --- 「ポスター切り替え」が選択された (推薦アイテムのquick_replyを送信)
#                                      |                      |- 「取り消し」が選択された (何もしない)
#                                      |                      |- 推薦アイテムの選択結果 (評価のquick_replyを送信)
#                                      |                      |- 評価の選択結果 (結果をinsert)
#                                      |- その他DM(アラートメッセージ)


# API処理用
from flask import Flask, request
import json, os, requests
# 「登録」処理関数
from webhook_process.DM_catch_process import registration
# 「推薦」処理関数
from webhook_process.DM_catch_process import recommen
# 「評価」処理関数
from webhook_process.DM_catch_process import evaluation
# 「その他」処理関数
from webhook_process.DM_catch_process import else_DM


# DMをもらった時
def process(twitter_account_auth, watson_personal_API, request, respon_json):

    if request.json["direct_message_events"][0]["message_create"]["sender_id"] == os.environ['MYTWITTER_ACCOUNT_ID']:
        # 自分が送信したDMイベント(何もしない)
        respon_json["DM"] = "My DM event"
        return json.dumps(respon_json)
    else:
        if request.json["direct_message_events"][0]["message_create"]["message_data"]["text"] == "登録":
            # 「登録」と送信された (推薦結果表示)
            return registration.process(twitter_account_auth, watson_personal_API, request, respon_json)
        elif request.json["direct_message_events"][0]["message_create"]["message_data"]["text"] == "推薦":
            # 「推薦」と送信された (推薦結果表示)
            return recommen.process(twitter_account_auth, request, respon_json)
        elif request.json["direct_message_events"][0]["message_create"]["message_data"]["text"] == "評価":
            # 「評価」と送信された (推薦アイテムのquick_replyを送信)
            return evaluation.item_sent(twitter_account_auth, request, respon_json)
        elif "quick_reply_response" in request.json["direct_message_events"][0]["message_create"]["message_data"]:
            # quick_replyイベント
            if "select" in request.json["direct_message_events"][0]["message_create"]["message_data"]["quick_reply_response"]["metadata"]:
                # 「ポスター選択の切り替え」が選択された（後半 or 前半のポスターを表示）
                return evaluation.item_sent(twitter_account_auth, request, respon_json)
            elif "cancel" == request.json["direct_message_events"][0]["message_create"]["message_data"]["quick_reply_response"]["metadata"]:
                # 「取り消し」が選択された (何もしない)
                respon_json["DM"] = "evaluation cancel quick_reply"
                return json.dumps(respon_json)
            elif "hyouka" not in request.json["direct_message_events"][0]["message_create"]["message_data"]["quick_reply_response"]["metadata"]:
                # 推薦アイテムの選択結果 (評価のquick_replyを送信)
                return evaluation.evaluation_sent(twitter_account_auth, request, respon_json)
            else:
                # 評価の選択結果 (結果をinsert)
                return evaluation.evaluation_insert(twitter_account_auth, request, respon_json)
        else:
            # その他DM(アラートメッセージ)
            return else_DM.process(twitter_account_auth, request, respon_json)
