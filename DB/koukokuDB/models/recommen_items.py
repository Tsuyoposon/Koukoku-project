from datetime import datetime
from DB.koukokuDB.database import db
# DB関連
from flask_sqlalchemy import SQLAlchemy

class Recommen_item(db.Model):

    __tablename__ = 'recommen_items'

    id = db.Column(db.Integer, primary_key=True)
    recommen_item_name = db.Column(db.String(255), nullable=False)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    feedbacks = db.relationship('Feedback', backref='recommen_item', lazy='dynamic')

    def __init__(self, id, recommen_item_name):
        self.id = id
        self.recommen_item_name = recommen_item_name

    def __repr__(self):
        return '<recommen_item_name %r>' % self.recommen_item_name

    def set_recommen_items(app):
        db = SQLAlchemy()
        with app.app_context():
            items = [
                Recommen_item(1, "チーム王研 センチメント分析と機械学習を用いたレビュー信頼性に基づく分類システム"),
                Recommen_item(2, "次世代型推薦システムズ SNSによる「性格ターゲティング広告」システム"),
                Recommen_item(3, "チームどんとはれ 遠野昔話における方言音声キーワードのリアルタイム解説表示システム"),
                Recommen_item(4, "SpecialDesignLab 情熱価格!!顧客ヒートマップ!"),
                Recommen_item(5, "ごじろくじ DeepLearningでバーチャルYouTuberを作ってみた!"),
                Recommen_item(6, "エモモエ 機械学習技術を用いた表情認識アプリケーション"),
                Recommen_item(7, "PRMLLAB 日本を訪れた外国人のための生活における問題解決と情報支援システムの構築"),
                Recommen_item(8, "ミーティングス 筋変異センサを用いたフリーハンドジェスチャーの実現"),
                Recommen_item(9, "衝動買い活動サークル△ 散財支援システム"),
                Recommen_item(10, "もじつくーる ひらがな文字の特徴を基にした文字生成"),
                Recommen_item(11, "低レイヤ同好会 数百万を数万円に!TDW構築に関する研究"),
                Recommen_item(12, "チームCG 動画配信への利用を目的としたwebカメラによる超お手軽モーションキャプチャの提案"),
                Recommen_item(13, "COMM研究室 インターネット生放送における放送者間コラボレーションシステムの提案"),
                Recommen_item(14, "No.14 広告の分析・生成および物語・映像への展開"),
                Recommen_item(15, "チーム印象派 世界観、人間関係、BGM等によるストーリーの生成"),
                Recommen_item(16, "RNSY 携帯端末における返信文候補提示システムの実現"),
                Recommen_item(17, "YATTE製作委員会 リモートロールプレイシステムYATTE"),
                Recommen_item(18, "TNT VRによる街の生活体験"),
                Recommen_item(19, "販売をラクにし隊 小規模販売時におけるらくらく販売記録デジタル化アプリ"),
                Recommen_item(20, "DeepDetector 車外映像を用いたDeep-CNNによる徘徊者検出システム"),
                Recommen_item(21, "明日から本気出す メッシュネットワークしようぜ"),
                Recommen_item(22, "GTO.kid's テレビ視聴履歴の分析による番組と放送局に対する視聴ロイヤルティの算出")
            ]
            db.session.add_all(items)
            db.session.commit()
