# main.py
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# 目錄
templates = Jinja2Templates(directory="templates")

# 靜態文件目錄
app.mount("/static", StaticFiles(directory="static"), name="static")


# 首頁
@app.get("/")
def read_root(request: Request):
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    return templates.TemplateResponse("index.html", {"request": request, "days": days})

# 每日名單
@app.get("/form/{day}")
def read_form(request: Request, day: str):
    return templates.TemplateResponse("form.html", {"request": request, "day": day})