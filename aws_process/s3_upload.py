# s3に評価データcsvをアップロードする

import os
# DB用のモデル
from DB.koukokuDB.models import User
from DB.koukokuDB.models import Recommen_item
from DB.koukokuDB.models import Feedback
from DB.koukokuDB.database import db
# csv関連
import csv
# AWS関連
import boto3

def process():
    # データのロード
    feedbacks = Feedback.query.all()
    recommen_items = Recommen_item.query.all()
    csv_header = [len(feedbacks), 52]
    for i in range(len(recommen_items)):
        csv_header.append(recommen_items[i].recommen_item_name)

    # 書き込み処理
    with open('feedbacks_traning.csv', 'w') as data_csv_file:
        # ヘッダー書き込み
        writer = csv.writer(data_csv_file, lineterminator='\n')
        writer.writerow(csv_header)

        # データ書き込み
        for i in range(len(feedbacks)):
            # 性格データ(52種類) + 評価アイテムid
            data_list = feedbacks[i].user.all_params_list()
            data_list.append(feedbacks[i].recommen_item_id - 1)
            writer.writerow(data_list)

    # s3 upload
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(os.environ['BUCKET_NAME'])
    bucket.upload_file('feedbacks_traning.csv', 'feedbacks_data/feedbacks_traning.csv')
