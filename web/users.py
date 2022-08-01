from fastapi import Depends, Request
from fastapi.routing import APIRouter
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from db.repos.toy_repo import ToyRepo
from web.dependencies import get_user_repo, get_db_session, get_toy_repo
from db.repos.user_repo import UserRepo
from web.schemas import UserCreate, UserOut

router = APIRouter(prefix='/users')


@router.get("/index")
def info(
    request: Request,
    user_repo: UserRepo = Depends(get_user_repo),
    session: Session = Depends(get_db_session),
):
    with session.begin():
        users = user_repo.all()

    return templates.TemplateResponse(
        'index.html',
        {
            'request': request,
            'users': users
        }
    )


templates = Jinja2Templates(directory='templates')


@router.post("/")
def create_user(
        user: UserCreate,
        user_repo: UserRepo = Depends(get_user_repo),
        session: Session = Depends(get_db_session)
) -> UserOut:
    with session.begin():
        user_id = user_repo.create(data=user)
        return user_repo.get(user_id=user_id)


@router.get("/")
def get_all_users(
        user_repo: UserRepo = Depends(get_user_repo),
        session: Session = Depends(get_db_session)
) -> list[UserOut]:
    with session.begin():
        return user_repo.all()


@router.get("/{user_id}")
def get_user(
        user_id: int,
        user_repo: UserRepo = Depends(get_user_repo),
        session: Session = Depends(get_db_session)
) -> UserOut:
    with session.begin():
        return user_repo.get(user_id=user_id)


@router.delete("/{user_id}")
def delete_user(
    user_id: int,
        user_repo: UserRepo = Depends(get_user_repo),
        toy_repo: ToyRepo = Depends(get_toy_repo),
        session: Session = Depends(get_db_session)
) -> None:
    with session.begin():
        toy_repo.delete_by_user_id(user_id=user_id)
        user_repo.delete(user_id=user_id)
