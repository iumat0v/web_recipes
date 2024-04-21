import sqlalchemy
from .db_session import SqlAlchemyBase


class Cat(SqlAlchemyBase):
    __tablename__ = 'cats'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)