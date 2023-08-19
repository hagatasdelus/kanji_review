from flaskr import db
from contextlib import contextmanager
from sqlalchemy import func

@contextmanager
def transaction():
    try:
        yield
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise


class Kanji(db.Model):

    __tablename__ = 'kanjis'
    
    id = db.Column(db.Integer, primary_key=True)
    kanji = db.Column(db.String(64), index=True, nullable=False)
    readings = db.Column(db.String(64), index=True, unique=False)
    hints = db.Column(db.String(64), nullable=True)
    sp_char = db.Column(db.Boolean, unique=False, default=False)

    def __init__(self, kanji, readings, hints, sp_char):
        self.kanji = kanji
        self.readings = readings
        self.hints = hints
        self.sp_char = sp_char
       
    def create_new_book(self):
        db.session.add(self)

    @classmethod
    def get_kanji(cls):
        return cls.query.order_by(
            func.random()
        ).first()
    
    @classmethod
    def select_kanji_by_id(cls, id):
        return cls.query.get(id)
    
    @classmethod
    def select_kanji_info_by_kanji(cls, kanji):
        return cls.query.filter_by(kanji=kanji).first()
