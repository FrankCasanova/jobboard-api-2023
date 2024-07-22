from db.repository.users import create_new_user
from db.session import get_db
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Request
from fastapi import responses, Response
from fastapi.responses import RedirectResponse
from fastapi import status
from fastapi.templating import Jinja2Templates
from schemas.users import UserCreate
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from webapps.users.forms import UserCreateForm
import logging


templates = Jinja2Templates(directory="backend/templates")
router = APIRouter(include_in_schema=False)


@router.get("/register/")
def register(request: Request):
    return templates.TemplateResponse("users/register.html", {"request": request})


@router.post("/register/")
async def register(request: Request, db: Session = Depends(get_db)):
    form = UserCreateForm(request)
    await form.load_data()
    if await form.is_valid():
        user = UserCreate(
            username=form.username,
            email=form.email,
            password=form.password,
        )
        try:
            user = create_new_user(user=user, db=db)
            return responses.RedirectResponse(
                "/?msg=Successfully-Registered",
                status_code=status.HTTP_302_FOUND,
            )  # default is post request, to use get request added status code 302
        except IntegrityError:
            form.__dict__.get("errors").append("Duplicate username or email")
            return templates.TemplateResponse("users/register.html", form.__dict__)
    return templates.TemplateResponse("users/register.html", form.__dict__)

@router.get("/logout")
@router.post("/logout")
def logout(request: Request, response: Response, db: Session = Depends(get_db)):
    logging.info("Logout route accessed")

    # Get the domain from the request
    domain = request.url.hostname

    # Attempt to delete the cookie with various configurations
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="access_token", domain=domain)
    response.delete_cookie(key="access_token", domain=domain, path="/")
    response.delete_cookie(key="access_token", secure=True, httponly=True)
    response.delete_cookie(key="access_token", domain=domain, path="/", secure=True, httponly=True)

    # Log the cookies after attempted deletion
    logging.info(f"Cookies after deletion attempt: {request.cookies}")

    # Return the response with a redirect to ensure the cookie deletion is sent to the client
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    return response

# Add this function to your routes to check cookie status
@router.get("/check-cookie")
def check_cookie(request: Request):
    access_token = request.cookies.get("access_token")
    return {"access_token": access_token}