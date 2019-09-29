from flask import Flask

from minette import (
    Minette,
    DialogRouter,
    MeCabServiceTagger
)
from minette.adapter.lineadapter import LineAdapter

from dialog_router import MyDialogRouter
from controllers.endpoint import bp as endpoint_bp
from controllers.messagelog import bp as messagelog_bp
from controllers.liff import bp as liff_bp

# BOTのインスタンス化
adapter = LineAdapter(
    config_file="./minette.ini",
    dialog_router=MyDialogRouter,
    tagger=MeCabServiceTagger,
)

# Webアプリケーションのセットアップ
app = Flask(__name__)
app.line_adapter = adapter
app.register_blueprint(endpoint_bp)
app.register_blueprint(messagelog_bp)   # 負荷が高いのでプロダクション環境ではBOT本体とは別インスタンスとすることが望ましい
app.register_blueprint(liff_bp)

# Webアプリケーションの起動
if __name__ == "__main__":
    # LINE Messaging APIのWebhook URL: https://あなたのサーバ/line/endpoint
    # メッセージログのURL: https://あなたのサーバ/messagelog?key=password
    app.run(host="0.0.0.0", port=12345)
