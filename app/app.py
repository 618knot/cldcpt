from typing import Optional
from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from starlette.requests import Request
from dotenv import load_dotenv
import os
import redis

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
)

class Cart(BaseModel):
    item01: Optional[int]
    item02: Optional[int]
    item03: Optional[int]

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("cart.html", {"request": request})

@app.post("/api/cart", response_class=HTMLResponse)
async def cart(request: Cart):
    cart_dict = {
        "item01": request.item01,
        "item02": request.item02,
        "item03": request.item03
    }

    red.hmset("hoge", cart_dict)

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
    return msg
