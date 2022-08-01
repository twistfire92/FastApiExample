from sqlalchemy.orm import Session
from sqlalchemy import insert, select, delete
from db.models import ToyModel
from web.schemas import ToyCreate, ToyOut


class ToyRepo:
    def __init__(self, session: Session):
        self._session = session

    def create(self, data: ToyCreate) -> int:
        statement = insert(ToyModel).values(**data.dict())
        result = self._session.execute(statement)
        return result.inserted_primary_key[0]

    def get(self, toy_id: int) -> ToyOut:
        statement = select(ToyModel).where(ToyModel.id == toy_id)
        result = self._session.execute(statement).scalars().unique().one()
        return ToyOut.from_orm(result)

    def all(self) -> list[ToyOut]:
        statement = select(ToyModel)
        results = self._session.execute(statement).scalars().unique().all()
        return [ToyOut.from_orm(result) for result in results]

    def delete(self, toy_id: int) -> None:
        statement = delete(ToyModel).where(ToyModel.id == toy_id)
        self._session.execute(statement)

    def delete_by_user_id(self, user_id: int) -> None:
        statement = delete(ToyModel).where(ToyModel.user_id == user_id)
        self._session.execute(statement)
