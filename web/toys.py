from fastapi import Depends
from fastapi.routing import APIRouter
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from web.dependencies import get_toy_repo, get_db_session
from db.repos.toy_repo import ToyRepo
from web.schemas import ToyCreate, ToyOut

router = APIRouter()

templates = Jinja2Templates(directory='templates')


@router.post("/")
def create_toy(
        toy: ToyCreate,
        toy_repo: ToyRepo = Depends(get_toy_repo),
        session: Session = Depends(get_db_session)
) -> ToyOut:
    with session.begin():
        toy_id = toy_repo.create(data=toy)
        return toy_repo.get(toy_id=toy_id)

@router.get("/")
def get_all_toys(
        toy_repo: ToyRepo = Depends(get_toy_repo),
        session: Session = Depends(get_db_session)
) -> list[ToyOut]:
    with session.begin():
        return toy_repo.all()


@router.get(
    "/{toy_id}",
    response_model=ToyOut
)
def get_toy(
        toy_id: int,
        toy_repo: ToyRepo = Depends(get_toy_repo),
        session: Session = Depends(get_db_session)
) -> ToyOut:
    with session.begin():
        return toy_repo.get(toy_id=toy_id)

#
# @router.get("/{item_id}/info")
# def index(
#     request: Request,
#     item_id: int,
#     db_session: Session = Depends(get_db_session),
# ):
#     item = items_data.get(item_id)
#     return templates.TemplateResponse(
#         'index.html',
#         {
#             'request': request,
#             'id': item_id,
#             'name': item["name"]
#         }
#     )
