from datetime import date, datetime

from app import db


class GuestBook(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author = db.Column(db.String(30), unique=False, nullable=False)  # 2
    mess_txt = db.Column(db.String(1000), unique=False, nullable=False)  # 3
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # 4
    del_flag = db.Column(db.Boolean, unique=False, nullable=False, default=False)  # 5
    date_updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)  # 2_3 onupdate=datetime.utcnow

    def to_json(self):
        return {
            'id': self.id,
            'Author': self.author,
            'Date created': self.date_created,
            'Date updated': self.date_updated,
            'Text': self.mess_txt,
            'Del flag': self.del_flag,
        }
