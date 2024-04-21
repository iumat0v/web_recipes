import sqlalchemy
from .db_session import SqlAlchemyBase


class Image(SqlAlchemyBase):
    __tablename__ = 'images'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    file = sqlalchemy.Column(sqlalchemy.String)
    