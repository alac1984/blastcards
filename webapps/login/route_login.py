from fastapi import APIRouter
from fastapi import Request
from fastapi import Depends
from fastapi.responses import HTMLResponse
from fastapi.exceptions import HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from apis.version1.route_login import login_for_access_token
from db.session import get_db
from webapps.login.forms import LoginForm

templates = Jinja2Templates(directory="templates/")

router = APIRouter()


@router.get("/login", response_class=HTMLResponse)
def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
async def login_form_data(request: Request, db: Session = Depends(get_db)):
    form = LoginForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            form.__dict__.update(msg="Login Successful :)")
            response = templates.TemplateResponse("dashboard.html", form.__dict__)
            login_for_access_token(response=response, form_data=form, db=db)
            return response
        except HTTPException:
            form.__dict__.update(msg="")
            form.__dict__.get("errors").append("Incorrect email or password")
            print(form.__dict__)
            return templates.TemplateResponse("login.html", form.__dict__)
    print(form.__dict__)
    return templates.TemplateResponse("login.html", form.__dict__)
