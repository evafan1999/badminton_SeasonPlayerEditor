# firebase_utils.py
import firebase_admin
from firebase_admin import credentials, db
import os


def initialize_firebase():
    # 使用服務帳戶金鑰初始化 SDK
    cred = credentials.Certificate(
        os.getcwd() + "/badmatch-659fd-firebase-adminsdk-oc0wg-3f070eb3ad.json"
    )
    firebase_admin.initialize_app(
        cred,
        {
            "databaseURL": "https://badmatch-659fd-default-rtdb.asia-southeast1.firebasedatabase.app/"
        },
    )


def read_firebase_data():
    # 取得資料庫
    ref = db.reference("/")

    # 取得資料庫內容
    data = ref.get()

    # 回傳資料
    return data


def write_firebase_data(data):
    # 取得資料庫
    ref = db.reference("/")

    # 寫入資料
    ref.set(data)
