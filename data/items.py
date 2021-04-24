import sqlalchemy
from sqlalchemy import orm
from data.db_session import SqlAlchemyBase


class Items(SqlAlchemyBase):
    __tablename__ = 'items'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    owner_id = sqlalchemy.Column(sqlalchemy.Integer,
                                 sqlalchemy.ForeignKey("users.id"))

    rent_id = sqlalchemy.Column(sqlalchemy.Integer,
                                nullable=True)
    count = sqlalchemy.Column(sqlalchemy.Integer,nullable=False)
    user = orm.relation('User')
