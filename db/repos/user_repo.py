from sqlalchemy.orm import Session
from sqlalchemy import insert, select, delete
from db.models import UserModel
from web.schemas import UserCreate, UserOut


class UserRepo:
    def __init__(self, session: Session):
        self._session = session

    def create(self, data: UserCreate) -> int:
        statement = insert(UserModel).values(**data.dict())
        result = self._session.execute(statement)
        return result.inserted_primary_key[0]

    def get(self, user_id: int) -> UserOut:
        statement = select(UserModel).where(UserModel.id == user_id)
        result = self._session.execute(statement).scalars().unique().one()
        return UserOut.from_orm(result)

    def all(self) -> list[UserOut]:
        statement = select(UserModel)
        results = self._session.execute(statement).scalars().unique().all()
        return [UserOut.from_orm(result) for result in results]

    def delete(self, user_id: int) -> None:
        statement = delete(UserModel).where(UserModel.id == user_id)
        self._session.execute(statement)
