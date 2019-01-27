# s3に評価データcsvをアップロードする

import os
# DB用のモデル
from DB.koukokuDB.models import User
from DB.koukokuDB.models import Recommen_item
from DB.koukokuDB.models import Feedback
from DB.koukokuDB.database import db
# csv関連
import csv
import datetime
# AWS関連
import boto3
# 乱数
import random

def process():
    # データのロード
    feedbacks = Feedback.query.all()
    recommen_items = Recommen_item.query.all()

    # ヘッダー情報の書き込み
    rabel_number = 0
    for i in range(len(feedbacks)):
        if feedbacks[i].feedback == 4:
            rabel_number += 2
        elif feedbacks[i].feedback == 1:
            rabel_number += 8
        else:
            rabel_number += 4
    csv_header = [rabel_number, 52]
    for i in range(len(recommen_items)):
        csv_header.append(recommen_items[i].recommen_item_name)

    # ラベルデータ書き込み処理
    with open('feedbacks_traning.csv', 'w') as data_csv_file:
        # ヘッダー書き込み
        writer = csv.writer(data_csv_file, lineterminator='\n')
        writer.writerow(csv_header)

        # データ書き込み
        for i in range(len(feedbacks)):
            this_feedback_user_params = feedbacks[i].user.all_params_list()
            # 評価によってラベルをつける
            if feedbacks[i].feedback == 5:
                # 5の時、そのポスターを4回学習させる
                data_list = this_feedback_user_params[:]
                data_list.append(feedbacks[i].recommen_item_id - 1)
                for j in range(4):
                    writer.writerow(data_list)
            elif feedbacks[i].feedback == 4:
                # 4の時、そのポスターを2回学習させる
                data_list = this_feedback_user_params[:]
                data_list.append(feedbacks[i].recommen_item_id - 1)
                for j in range(2):
                    writer.writerow(data_list)
            elif feedbacks[i].feedback == 3:
                # 3の時、そのポスターを1回、
                data_list = this_feedback_user_params[:]
                data_list.append(feedbacks[i].recommen_item_id - 1)
                writer.writerow(data_list)
                # それ以外を3回学習させる
                recommen_items_del = recommen_items[:]
                del recommen_items_del[feedbacks[i].recommen_item_id - 1]
                choice_item = random.sample(recommen_items_del, 3)
                for j in range(3):
                    data_list = this_feedback_user_params[:]
                    data_list.append(choice_item[j].id - 1)
                    writer.writerow(data_list)
            elif feedbacks[i].feedback == 2:
                # 2の時、そのポスターを4回
                recommen_items_del = recommen_items[:]
                del recommen_items_del[feedbacks[i].recommen_item_id - 1]
                choice_item = random.sample(recommen_items_del, 4)
                for j in range(4):
                    data_list = this_feedback_user_params[:]
                    data_list.append(choice_item[j].id - 1)
                    writer.writerow(data_list)
            elif feedbacks[i].feedback == 1:
                # 1の時、そのポスターを8回
                recommen_items_del = recommen_items[:]
                del recommen_items_del[feedbacks[i].recommen_item_id - 1]
                choice_item = random.sample(recommen_items_del, 8)
                for j in range(8):
                    data_list = this_feedback_user_params[:]
                    data_list.append(choice_item[j].id - 1)
                    writer.writerow(data_list)

    # s3 upload
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(os.environ['BUCKET_NAME'])
    bucket.upload_file('feedbacks_traning.csv', 'feedbacks_data/feedbacks_traning.csv')
    # 評価結果書き込み(50件に1回)
    if len(recommen_items) % 50 == 0:
        with open('feedbacks_table.csv', 'w') as table_data_csv:
            writer = csv.writer(table_data_csv, lineterminator='\n')
            # データ書き込み
            for i in range(len(feedbacks)):
                # 性格データ(52種類) + 評価アイテムid + 評価内容
                data_list = feedbacks[i].user.all_params_list()
                data_list.append(feedbacks[i].recommen_item_id - 1)
                data_list.append(feedbacks[i].feedback)
                data_list.append(feedbacks[i].created_at)
                data_list.append(feedbacks[i].updated_at)
                writer.writerow(data_list)
        bucket.upload_file('feedbacks_table.csv', 'feedbacks_table_data/feedbacks_table' + str(datetime.datetime.now()) + '.csv')
