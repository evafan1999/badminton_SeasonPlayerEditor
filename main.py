# main.py
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from firebase_utils import initialize_firebase, read_firebase_data, write_firebase_data

app = FastAPI()

# 目錄
templates = Jinja2Templates(directory="templates")

# 靜態文件目錄
app.mount("/static", StaticFiles(directory="static"), name="static")

# firebase
# 初始化 Firebase
initialize_firebase()


# 首頁
@app.get("/")
def read_root(request: Request):
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    return templates.TemplateResponse("index.html", {"request": request, "days": days})

# 每日名單
@app.get("/form/{day}")
def read_form(request: Request, day: str):
    return templates.TemplateResponse("form.html", {"request": request, "day": day})

# 資料庫欄位名稱
@app.get("/firebase_data")
def get_firebase_data():
    # 讀取資料
    firebase_data = read_firebase_data()
    return firebase_data

# 寫入firebase
@app.post("/write")
def write(request: Request, name: str, day: int):
    # 讀取資料
    firebase_data = read_firebase_data()
    # 寫入資料
    if name in firebase_data:
        firebase_data[name].append(day)
    else:
        firebase_data[name]=[day]
    write_firebase_data(firebase_data)
    return JSONResponse(status_code=200, content={"message": "success"})