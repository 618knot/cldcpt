from typing import Optional
from fastapi import FastAPI, Cookie, Response
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from starlette.requests import Request
from dotenv import load_dotenv
import time
import os
import redis
import hashlib

from models.db.util import session
from models.user import User

load_dotenv()
REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = os.environ.get("REDIS_PORT")
ORIGIN = os.environ.get("ORIGIN")

app = FastAPI()
templates = Jinja2Templates(directory="docs")
red = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("cart.html", {"request": request})


class Cart(BaseModel):
    item01: Optional[int]
    item02: Optional[int]
    item03: Optional[int]

@app.post("/api/cart", response_class=HTMLResponse)
async def cart(cart: Cart, request: Request):
    cart_dict = {
        "item01": cart.item01,
        "item02": cart.item02,
        "item03": cart.item03
    }

    msg = """
    <h4>保存された値</h4>
    <table>
    """

    idx = 1
    for item in cart_dict.values():
        msg += f"""
        <tr>
            <td>item0{idx}</td>
            <td>{item}</td>
        </tr>
        """

        idx += 1

    msg += "</table>"
    response = Response(content=msg)

    cookie = request.cookies.get("_session")
    if cookie == None:
        cookie = str(time.time())
        response.set_cookie(key="_session", value=cookie, expires=600)

    if is_sign_in(cookie):
        user = session.query(User).filter(cookie == User.session).first()

        # redisにカートを保存
        red.hmset(user.email, cart_dict)
    else:
        # redisにカートを保存
        red.hmset(cookie, cart_dict)

    return response

class CookieV:
    _session: str

@app.post("/api/cart")
async def get_cart(_session: CookieV, request: Request):
    return red.hgetall(_session._session)

@app.get("/api/mycart")
async def get_cart(request: Request):
    _session = request.cookies.get("_session")
    try:
        if is_sign_in(_session):
            user = session.query(User).filter(_session == User.session).first()

            red.hgetall(user.email)
        elif _session:
            red.hgetall(_session)
    finally:
        return "なし"

@app.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    _session = request.cookies.get("_session")
    if is_sign_in(_session):
        return RedirectResponse(url="/mycart")
    return templates.TemplateResponse("register.html", {"request": request})

class UserReq(BaseModel):
    email: str
    password: str

@app.post("/api/register")
async def register(request: UserReq):
    try:
        _session = str(time.time())
        encrypted_password = hashlib.sha256(request.password.encode("utf-8")).hexdigest()
        user = User(email=request.email, password=encrypted_password, session=_session)
        session.add(user)
        session.commit()
        response = Response()
        response.set_cookie(key="_session", value=_session, expires=600)
        return response
    except:
        session.rollback()
        return Response(status_code=400)

@app.get("/login")
async def login(request: Request):
    _session = request.cookies.get("_session")

    if is_sign_in(_session):
        return RedirectResponse(url="/mycart")
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/api/login")
async def login(request: UserReq):
    _session = str(time.time())
    encrypted_password = hashlib.sha256(request.password.encode("utf-8")).hexdigest()
    user = session.query(User).filter(request.email == User.email, encrypted_password == User.password).first()

    if user:
        user.session = _session
        session.commit()
        response = Response()
        response.set_cookie(key="_session", value=_session, expires=600)
        return response
    
    return RedirectResponse(url="/register")

@app.get("/mycart", response_class=HTMLResponse)
async def mycart(request: Request):
    _session = request.cookies.get("_session")

    if not is_sign_in(_session):
        return RedirectResponse(url="/login")
    return templates.TemplateResponse("mycart.html", {"request": request})

def is_sign_in(_session: str) -> bool:
    return session and session.query(User).filter(_session == User.session).count()