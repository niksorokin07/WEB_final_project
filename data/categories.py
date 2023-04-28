import sqlalchemy
from data.db_session import SqlAlchemyBase


association_table = sqlalchemy.Table(
    'association',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('products', sqlalchemy.Integer, sqlalchemy.ForeignKey('products.id')),
    sqlalchemy.Column('categories', sqlalchemy.Integer, sqlalchemy.ForeignKey('categories.id'))
)


class Categories(SqlAlchemyBase):
    __tablename__ = 'categories'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,  autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
