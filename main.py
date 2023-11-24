# main.py
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from firebase_utils import initialize_firebase, read_firebase_data, write_firebase_data
from typing import List

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
    days = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    return templates.TemplateResponse("index.html", {"request": request, "days": days})


# 每日名單

# 資料庫欄位名稱
@app.get("/firebase_data")
def get_firebase_data():
    # 讀取資料
    firebase_data = read_firebase_data()
    return firebase_data


# 寫入firebase
@app.post("/write")
def write(request: Request, name: str, day: str):
    # 讀取資料
    firebase_data = read_firebase_data()
    # 寫入資料
    if name in firebase_data:
        firebase_data[name].append(day)
    else:
        firebase_data[name] = [day]
    write_firebase_data(firebase_data)
    return JSONResponse(status_code=200, content={"message": "success"})

# 刪除firebase
@app.post("/deletePlayer")
def delete(request: Request, params: dict):
    name = params["name"]
    # 讀取資料
    firebase_data = read_firebase_data()
    # 刪除資料
    if name in firebase_data:
        del firebase_data[name]
    write_firebase_data(firebase_data)
    return JSONResponse(status_code=200, content={"message": "success"})

# 資料庫中的姓名
@app.get("/names")
def get_names():
    firebase_data = read_firebase_data()
    names = list(firebase_data.keys())
    return {"names": names}

# 取得指定星期名單的路由
@app.get("/names/{day}")
def get_names_by_day(day: str) -> List[str]:
    firebase_data = read_firebase_data()
    print(firebase_data) #{'fff': ['Tuesday'], 'qq': ['monday'], 'vv': ['Monday'], 'ww': ['monday'], 'xx': ['Monday'], '小王': 550, '耿Z': ['monday']}
    # 將schedule變成小寫
    names_for_day = [name for name, schedule in firebase_data.items() if isinstance(schedule, list) and day in schedule]
    return names_for_day