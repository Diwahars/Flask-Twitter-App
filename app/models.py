from app import db

class User(db.Model):
    id = db.Column(db.String(120), primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    url = db.Column(db.String(120))
    profile_image_url_https = db.Column(db.String(120))
    tweets = db.relationship('Tweet', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}, PI {}>'.format(self.name, self.profile_image_url_https)

    def last_tweet(self):
        return Tweet.query.filter_by(user_id=self.id).order_by(Tweet.created_at.desc()).first()

    def tweeted_tweets(self):
        return Tweet.query.filter_by(user_id=self.id).order_by(Tweet.created_at.desc()).all()

class Tweet(db.Model):
    id_str = db.Column(db.String(120), primary_key=True)
    created_at = db.Column(db.DateTime, index=True)
    text = db.Column(db.String(280))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Tweet {}, User {}>'.format(self.text, self.user_id)

    def new_tweets(self):
        pass