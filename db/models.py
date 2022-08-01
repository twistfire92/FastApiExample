import sqlalchemy as sa
from sqlalchemy import Table, MetaData
from sqlalchemy.orm import as_declarative, relationship

from web.schemas import Group

metadata = MetaData()


@as_declarative(metadata=metadata)
class Base:
    __tablename__: str
    __table__: Table


class UserModel(Base):
    __tablename__ = 'user'

    id: int = sa.Column(sa.Integer, primary_key=True)
    name: str = sa.Column(sa.String)
    age: int = sa.Column(sa.Integer)
    group: int = sa.Column(sa.Enum(Group))
    toys: "ToyModel" = relationship(
        "ToyModel",
        back_populates='user',
        cascade="all, delete",
    )


class ToyModel(Base):
    __tablename__ = 'toy'

    id: int = sa.Column(sa.Integer, primary_key=True)
    name: str = sa.Column(sa.String)
    description: str = sa.Column(sa.String)
    user_id: int = sa.Column(sa.Integer, sa.ForeignKey('user.id', ondelete='CASCADE'))
    user: UserModel = relationship(
        UserModel,
        back_populates='toys',
        cascade="all, delete"
    )
