from fastapi import Depends, Request
from sqlalchemy.orm import Session

from db.repos.toy_repo import ToyRepo
from db.repos.user_repo import UserRepo


def get_db_session(request: Request):

    session: Session = request.app.state.session_factory()

    try:
        yield session
    finally:
        session.commit()
        session.close()


def get_toy_repo(
        session: Session = Depends(get_db_session)
) -> ToyRepo:
    return ToyRepo(session=session)


def get_user_repo(
        session: Session = Depends(get_db_session)
) -> UserRepo:
    return UserRepo(session=session)