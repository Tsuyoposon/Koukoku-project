from datetime import datetime
from DB.koukokuDB.database import db

class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    twitter_userid_hash = db.Column(db.String(40), index=True, nullable=False)

    openness = db.Column(db.Float, nullable=False)
    adventurousness = db.Column(db.Float, nullable=False)
    artistic_interests = db.Column(db.Float, nullable=False)
    emotionality = db.Column(db.Float, nullable=False)
    imagination = db.Column(db.Float, nullable=False)
    intellect = db.Column(db.Float, nullable=False)
    liberalism = db.Column(db.Float, nullable=False)

    conscientiousness = db.Column(db.Float, nullable=False)
    achievement_striving = db.Column(db.Float, nullable=False)
    cautiousness = db.Column(db.Float, nullable=False)
    dutifulness = db.Column(db.Float, nullable=False)
    orderliness = db.Column(db.Float, nullable=False)
    self_discipline = db.Column(db.Float, nullable=False)
    self_efficacy = db.Column(db.Float, nullable=False)

    extraversion = db.Column(db.Float, nullable=False)
    activity_level = db.Column(db.Float, nullable=False)
    assertiveness = db.Column(db.Float, nullable=False)
    cheerfulness = db.Column(db.Float, nullable=False)
    excitement_seeking = db.Column(db.Float, nullable=False)
    friendliness = db.Column(db.Float, nullable=False)
    gregariousness = db.Column(db.Float, nullable=False)

    agreeableness = db.Column(db.Float, nullable=False)
    altruism = db.Column(db.Float, nullable=False)
    cooperation = db.Column(db.Float, nullable=False)
    modesty = db.Column(db.Float, nullable=False)
    morality = db.Column(db.Float, nullable=False)
    sympathy = db.Column(db.Float, nullable=False)
    trust = db.Column(db.Float, nullable=False)

    emotional_range = db.Column(db.Float, nullable=False)
    anger = db.Column(db.Float, nullable=False)
    anxiety = db.Column(db.Float, nullable=False)
    depression = db.Column(db.Float, nullable=False)
    immoderation = db.Column(db.Float, nullable=False)
    self_consciousness = db.Column(db.Float, nullable=False)
    vulnerability = db.Column(db.Float, nullable=False)

    need_challenge = db.Column(db.Float, nullable=False)
    need_closeness = db.Column(db.Float, nullable=False)
    need_curiosity = db.Column(db.Float, nullable=False)
    need_excitement = db.Column(db.Float, nullable=False)
    need_harmony = db.Column(db.Float, nullable=False)
    need_ideal = db.Column(db.Float, nullable=False)
    need_liberty = db.Column(db.Float, nullable=False)
    need_love = db.Column(db.Float, nullable=False)
    need_practicality = db.Column(db.Float, nullable=False)
    need_self_expression = db.Column(db.Float, nullable=False)
    need_stability = db.Column(db.Float, nullable=False)
    need_structure = db.Column(db.Float, nullable=False)

    value_conservation = db.Column(db.Float, nullable=False)
    value_openness_to_change = db.Column(db.Float, nullable=False)
    value_hedonism = db.Column(db.Float, nullable=False)
    value_self_enhancement = db.Column(db.Float, nullable=False)
    value_self_transcendence = db.Column(db.Float, nullable=False)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    feedbacks = db.relationship('Feedback', backref='user', lazy='dynamic')

    def __init__(self, twitter_userid_hash,
        openness, adventurousness, artistic_interests, emotionality, imagination, intellect, liberalism,
        conscientiousness, achievement_striving, cautiousness, dutifulness, orderliness, self_discipline, self_efficacy,
        extraversion, activity_level, assertiveness, cheerfulness, excitement_seeking, friendliness, gregariousness,
        agreeableness, altruism, cooperation, modesty, morality, sympathy, trust,
        emotional_range, anger, anxiety, depression, immoderation, self_consciousness, vulnerability,
        need_challenge, need_closeness, need_curiosity, need_excitement, need_harmony, need_ideal,
        need_liberty, need_love, need_practicality, need_self_expression, need_stability, need_structure,
        value_conservation, value_openness_to_change, value_hedonism, value_self_enhancement, value_self_transcendence
    ):

        self.twitter_userid_hash = twitter_userid_hash

        self.openness = openness
        self.adventurousness = adventurousness
        self.artistic_interests = artistic_interests
        self.emotionality = emotionality
        self.imagination = imagination
        self.intellect = intellect
        self.liberalism = liberalism

        self.conscientiousness = conscientiousness
        self.achievement_striving = achievement_striving
        self.cautiousness = cautiousness
        self.dutifulness = dutifulness
        self.orderliness = orderliness
        self.self_discipline = self_discipline
        self.self_efficacy = self_efficacy

        self.extraversion = extraversion
        self.activity_level = activity_level
        self.assertiveness = assertiveness
        self.cheerfulness = cheerfulness
        self.excitement_seeking = excitement_seeking
        self.friendliness = friendliness
        self.gregariousness = gregariousness

        self.agreeableness = agreeableness
        self.altruism = altruism
        self.cooperation = cooperation
        self.modesty = modesty
        self.morality = morality
        self.sympathy = sympathy
        self.trust = trust

        self.emotional_range = emotional_range
        self.anger = anger
        self.anxiety = anxiety
        self.depression = depression
        self.immoderation = immoderation
        self.self_consciousness = self_consciousness
        self.vulnerability = vulnerability

        self.need_challenge = need_challenge
        self.need_closeness = need_closeness
        self.need_curiosity = need_curiosity
        self.need_excitement = need_excitement
        self.need_harmony = need_harmony
        self.need_ideal = need_ideal
        self.need_liberty = need_liberty
        self.need_love = need_love
        self.need_practicality = need_practicality
        self.need_self_expression = need_self_expression
        self.need_stability = need_stability
        self.need_structure = need_structure

        self.value_conservation = value_conservation
        self.value_openness_to_change = value_openness_to_change
        self.value_hedonism = value_hedonism
        self.value_self_enhancement = value_self_enhancement
        self.value_self_transcendence = value_self_transcendence

    def __repr__(self):
        return '<TwitterUserID %r>' % self.twitter_userid_hash

    def all_params(self):
        all_params_string = f'{self.openness},{self.adventurousness},{self.artistic_interests},{self.emotionality},{self.imagination},{self.intellect},{self.liberalism},' + \
            f'{self.conscientiousness},{self.achievement_striving},{self.cautiousness},{self.dutifulness},{self.orderliness},{self.self_discipline},{self.self_efficacy},' + \
            f'{self.extraversion},{self.activity_level},{self.assertiveness},{self.cheerfulness},{self.excitement_seeking},{self.friendliness},{self.gregariousness},' + \
            f'{self.agreeableness},{self.altruism},{self.cooperation},{self.modesty},{self.morality},{self.sympathy},{self.trust},' + \
            f'{self.emotional_range},{self.anger},{self.anxiety},{self.depression},{self.immoderation},{self.self_consciousness},{self.vulnerability},' + \
            f'{self.need_challenge},{self.need_closeness},{self.need_curiosity},{self.need_excitement},{self.need_harmony},{self.need_ideal},{self.need_liberty},' + \
            f'{self.need_love},{self.need_practicality},{self.need_self_expression},{self.need_stability},{self.need_structure},' + \
            f'{self.value_conservation},{self.value_openness_to_change},{self.value_hedonism},{self.value_self_enhancement},{self.value_self_transcendence}'
        return all_params_string
