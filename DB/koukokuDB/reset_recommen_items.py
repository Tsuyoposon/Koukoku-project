# flaskサーバを起動した時に1回だけ実行
# recommen_itemテーブルに初期値を入れる
# -*- coding: utf-8 -*-

# DB用のモデル
import DB.koukokuDB.models
from DB.koukokuDB.models import Recommen_item
# DB関連
from flask_sqlalchemy import SQLAlchemy

def process(app):
    db = SQLAlchemy()
    with app.app_context():
        db.session.query(Recommen_item).delete()
        items = [
            Recommen_item(1, "1-A02 ProtoHole: 穴と音響センシングを用いたインタラクティブな３Dプリントオブジェクトの提案"),
            Recommen_item(2, "1-A03 視覚的でインタラクティブな分類器の構築手法"),
            Recommen_item(3, "1-A04 ニオイセンサーによるニオイの可視化と官能試験との相関性"),
            Recommen_item(4, "1-A05 プレゼンテーションにおける実空間とオンライン空間の聴衆コンテクストの融合"),
            Recommen_item(5, "1-A06 VRショールームのためのVR酔いを抑えた歩行移動インタフェース"),
            Recommen_item(6, "1-A07 スマートウォッチを用いたモノづくりの動作検出に対する試み"),
            Recommen_item(7, "1-A08 睡眠時間の副次利用によるエンタテインメント価値創出"),
            Recommen_item(8, "1-A09 腰背部へのせん断力提示による歩行誘導に関する一検討"),
            Recommen_item(9, "1-A10 ユーザ周囲の多種多様な情報機器を「サービス化」するLBSインタラクション"),
            Recommen_item(10, "1-A15 実世界人形遊びを拡張する仮想ドールハウス"),
            Recommen_item(11, "1-A16 透紙: 紙媒体の質感を拡張する表現手法の提案"),
            Recommen_item(12, "1-A17 Pulse shot:心拍情報を用いた写真撮影システムおよび検索システム"),
            Recommen_item(13, "1-A19 AmbientLetter：わからないスペルをこっそり知るための筆記検出および文字提示手法"),
            Recommen_item(14, "1-A20 ポーチの型紙製作支援システム"),
            Recommen_item(15, "1-A21 宿泊者のホテル内での動きの偏りに関して"),
            Recommen_item(16, "1-A22 パッチワーク風キルト作成支援システム"),
            Recommen_item(17, "1-A23 女性のためのシチュエーションドラマを利用した癒しシステム")
        ]
        db.session.add_all(items)
        db.session.commit()
