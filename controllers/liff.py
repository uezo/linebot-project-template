"""
LIFFの実体はHTTPSでアクセスするWebアプリケーションです。
事前に以下のようにminette.iniにサーバのアドレスを設定してください。

例1
host = 9b41ad02.ngrok.io

例2
host = yourdomain.com:21212
"""

from flask import Flask, Blueprint, current_app, request, render_template
import requests
import json
from minette import Config


# メインから読み込むBlueprintの定義
bp = Blueprint("liff", __name__)


# LIFFの例
@bp.route("/liff/example")
def liff_example():
    return render_template("liff.html")


# LIFF操作用クラス（おまけ）
class LiffManager:
    def __init__(self, channel_access_token):
        self.endpoint_url = "https://api.line.me/liff/v1/apps"
        self.headers = {
            "Authorization": "Bearer {}".format(channel_access_token),
            "Content-Type": "application/json"
        }

    def get(self, liff_id=None, liff_url=None):
        ret = requests.get(self.endpoint_url, headers=self.headers)
        if ret.status_code != 200:
            raise ret.raise_for_status()
        apps = ret.json()["apps"]
        if liff_id:
            liff_apps = [a for a in apps if a["liffId"] == liff_id]
            return liff_apps[0] if liff_apps else None
        elif liff_url:
            return [a for a in apps if a["view"]["url"] == liff_url]
        else:
            return apps

    def add(self, liff_url, view_type, description=None, features_ble=None):
        data = {"view": {"url": liff_url, "type": view_type}, "description": description, "features": {"ble": features_ble}}
        ret = requests.post(self.endpoint_url, headers=self.headers, json=data)
        if ret.status_code != 200:
            raise ret.raise_for_status()
        return ret.json()["liffId"]

    def update(self, liff_id, liff_url=None, view_type=None, description=None, features_ble=None):
        data = {"view": {"url": liff_url, "type": view_type}, "description": description, "features": {"ble": features_ble}}
        ret = requests.put(self.endpoint_url + "/" + liff_id, headers=self.headers, json=data)
        if ret.status_code != 200:
            raise ret.raise_for_status()
    
    def delete(self, liff_id):
        ret = requests.delete(self.endpoint_url + "/" + liff_id, headers=self.headers)
        if ret.status_code != 200:
            raise ret.raise_for_status()


# LIFFの登録
if __name__ == "__main__":
    # 設定の取得
    config = Config("../minette.ini")
    host = config.get(key="host")
    channel_access_token = config.get(section="line_bot_api", key="channel_access_token")
    # LIFFの実体のURL。必ずHTTPSが必要
    liff_url = "https://{}/liff/example".format(host)
    # LIFFの表示サイズ。全画面：full / 80%くらい：tall / 半分くらい：compact
    view_type = "full"
    # 登録
    lm = LiffManager(channel_access_token)
    liff_id = lm.add(liff_url=liff_url, view_type=view_type)
    print("""LIFFの登録に成功しました！
    ----
    LIFFのURL: line://app/{0}
    ----
    LIFF ID: {0}
    URL: {1}
    TYPE: {2}
    """.format(liff_id, liff_url, view_type))
