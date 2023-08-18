from flaskr import db
from contextlib import contextmanager

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

    # @classmethod
    # def get_books(cls):
    #     return cls.query.order_by(
    #         cls.arrival_day.desc()
    #     ).limit(10).all()
    
    # @classmethod
    # def select_book_by_id(cls, id):
    #     return cls.query.get(id)
    
    # @classmethod
    # def delete_book(cls, id):    
    #     cls.query.filter_by(id=int(id)).delete()
      
# class Board(db.Model):

#     __tablename__ = 'boards'

#     id = db.Column(db.Integer, primary_key=True)
#     book_id = db.Column(db.Integer, db.ForeignKey('book_infos.id'), index=True)
#     from_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
#     post = db.Column(db.Text)
#     is_read = db.Column(db.Boolean, default=False)
#     create_at = db.Column(db.DateTime, default=datetime.now)
#     update_at = db.Column(db.DateTime, default=datetime.now)

#     user = relationship("User", back_populates="boards")

#     def __init__(self, from_user_id, book_id, post):
#         self.from_user_id = from_user_id
#         self.book_id = book_id
#         self.post = post

#     def create_post(self):
#         db.session.add(self)

#     @classmethod
#     def get_book_posts(cls, book_id, offset_value=0, limit_value=100):
#         return cls.query.filter_by(
#             book_id=book_id
#         ).order_by(
#             desc(cls.id)
#         ).offset(offset_value).limit(limit_value).all()
    
#     @classmethod
#     def delete_posts_by_book_id(cls, book_id):
#         return cls.query.filter_by(
#                 book_id=book_id
#             ).delete()
    
#     @classmethod
#     def update_is_read_by_ids(cls, ids):
#         cls.query.filter(cls.id.in_(ids)).update(
#             {'is_read': True},
#             synchronize_session='fetch'
#         )

#     @classmethod
#     def select_not_read_posts(cls, book_id):
#         return cls.query.filter(
#             and_(
#                 cls.book_id == book_id,
#                 cls.is_read == 0
#             )
#         ).order_by(cls.id).all()
