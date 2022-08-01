from fastapi.routing import APIRouter
from web import toys, users

api_router = APIRouter()

api_router.include_router(users.router, tags=['users'])
api_router.include_router(toys.router, prefix='/toys', tags=['toys'])
