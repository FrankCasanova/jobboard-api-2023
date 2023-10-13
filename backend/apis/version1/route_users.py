from .db.models.users import User
from .db.repository.users import create_new_user
from .db.session import get_db
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Request
from fastapi.security.utils import get_authorization_scheme_param
from .schemas.users import ShowUser
from .schemas.users import UserCreate
from sqlalchemy.orm import Session

from .route_login import get_current_user_from_token


router = APIRouter()


@router.post("/", response_model=ShowUser)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user = create_new_user(user=user, db=db)
    return user


@router.get("/me", response_model=ShowUser)
def read_users_me(
    request: Request,
    db: Session = Depends(get_db),
):
    token = request.cookies.get("access_token")
    scheme, param = get_authorization_scheme_param(
        token,
    )  # scheme will hold "Bearer" and param will hold actual token value
    current_user: User = get_current_user_from_token(token=param, db=db)
    return current_user
