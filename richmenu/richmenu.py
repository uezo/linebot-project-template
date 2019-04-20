import requests
import json
from minette import Config


# リッチメニュー
class RichMenu:
    def __init__(self, name, chat_bar_text, size_full=True, selected=False):
        self.size = {"width": 2500, "height": 1686}
        if not size_full:
            self.size["height"] = 843
        self.selected = selected
        self.name = name
        self.chat_bar_text = chat_bar_text
        self.areas = []

    def add_area(self, x, y, width, height, action_type, text=None, uri=None, data=None):
        bounds = {"x": x, "y": y, "width": width, "height": height}
        action = {"type": action_type}
        if action_type == "postback":
            if text:
                action["text"] = text
            action["data"] = data
        elif action_type == "uri":
            action["uri"] = uri
        else:
            action["text"] = text
        self.areas.append({"bounds": bounds, "action": action})

    def to_json(self):
        dic = {"size": self.size, "selected": self.selected, "name": self.name, "chatBarText": self.chat_bar_text, "areas": self.areas}
        return json.dumps(dic)


# リッチメニュー操作ユーティリティ（おまけ）
class RichMenuManager:
    def __init__(self, channel_access_token, verify=True):
        self.headers = {"Authorization": "Bearer {%s}" % channel_access_token}
        self.verify = verify

    # リッチメニューの登録
    def register(self, richmenu, image_path=None):
        url = "https://api.line.me/v2/bot/richmenu"
        res = requests.post(url, headers=dict(self.headers, **{"content-type": "application/json"}), data=richmenu.to_json(), verify=self.verify).json()
        if image_path:
            self.upload_image(res["richMenuId"], image_path)
        return res

    # 画像のアップロード
    def upload_image(self, richmenu_id, image_path):
        url = "https://api.line.me/v2/bot/richmenu/%s/content" % richmenu_id
        image_file = open(image_path, "rb")
        return requests.post(url, headers=dict(self.headers, **{"content-type": "image/jpeg"}), data=image_file, verify=self.verify).json()

    # リッチメニュー一覧の取得
    def get_list(self):
        url = "https://api.line.me/v2/bot/richmenu/list"
        return requests.get(url, headers=self.headers, verify=self.verify).json()

    # リッチメニュー画像の取得
    def download_image(self, richmenu_id, filename=None):
        url = "https://api.line.me/v2/bot/richmenu/%s/content" % richmenu_id
        res = requests.get(url, headers=self.headers, verify=self.verify)
        if filename:
            with open(filename, "wb") as f:
                f.write(res.content)
        else:
            return res.content

    # リッチメニューの削除
    def remove(self, richmenu_id):
        url = "https://api.line.me/v2/bot/richmenu/%s" % richmenu_id
        return requests.delete(url, headers=self.headers, verify=self.verify).json()

    # すべてのリッチメニューの削除
    def remove_all(self):
        menus = self.get_list()
        for m in menus["richmenus"]:
            self.remove(m["richMenuId"])

    # ユーザーにリッチメニューを適用
    def apply(self, user_id, richmenu_id):
        url = "https://api.line.me/v2/bot/user/%s/richmenu/%s" % (user_id, richmenu_id)
        return requests.post(url, headers=self.headers, verify=self.verify).json()

    # ユーザーのリッチメニューを解除
    def detach(self, user_id):
        url = "https://api.line.me/v2/bot/user/%s/richmenu" % user_id
        return requests.delete(url, headers=self.headers, verify=self.verify).json()

    # ユーザーのリッチメニューを取得
    def get_applied_menu(self, user_id):
        url = "https://api.line.me/v2/bot/user/%s/richmenu" % user_id
        return requests.get(url, headers=self.headers, verify=self.verify).json()

    # デフォルトリッチメニューを設定
    def apply_default(self, richmenu_id):
        url = "https://api.line.me/v2/bot/user/all/richmenu/%s" % richmenu_id
        return requests.post(url, headers=self.headers, verify=self.verify).json()

    # デフォルトリッチメニューを取得
    def get_default(self):
        url = "https://api.line.me/v2/bot/user/all/richmenu"
        return requests.get(url, headers=self.headers, verify=self.verify).json()


# リッチメニューの登録
if __name__ == "__main__":
    # 設定の取得
    config = Config("../minette.ini")
    channel_access_token = config.get(section="line_bot_api", key="channel_access_token")
    # リッチメニュー のエリア定義
    rm = RichMenu(name="test_menu", chat_bar_text="リッチメニューの例", size_full=True, selected=True)
    rm.add_area(0, 0, 833, 843, "message", "メニューA")
    rm.add_area(833, 0, 833, 843, "message", "メニューB")
    rm.add_area(1666, 0, 834, 843, "message", "メニューC")
    rm.add_area(0, 833, 833, 843, "postback", data="name=menu_d&data=data_d")
    rm.add_area(833, 833, 833, 843, "postback", data="name=menu_e&payload=payload_e", text="メニューE")
    rm.add_area(1666, 833, 834, 843, "uri", uri="http://www.imoutobot.com")
    # 登録
    rmm = RichMenuManager(channel_access_token)
    menuinf = rmm.register(rm, "./richmenu_image.png")
    print("登録されたリッチメニューのID: " + menuinf["richMenuId"])
    # デフォルトに反映
    rmm.apply_default(menuinf["richMenuId"])
    # 反映の確認
    print("標準のリッチメニューのID: " + rmm.get_default()["richMenuId"])
