import sqlalchemy
from .db_session import SqlAlchemyBase


class RecImage(SqlAlchemyBase):
    __tablename__ = 'rec_images'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    id_rec = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("recipes.id"))
    id_images = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("images.id"))