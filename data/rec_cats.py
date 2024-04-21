import sqlalchemy
from .db_session import SqlAlchemyBase


class RecCat(SqlAlchemyBase):
    __tablename__ = 'rec_cats'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    id_cats = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("cats.id"))
    id_rec = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("recipes.id"))
