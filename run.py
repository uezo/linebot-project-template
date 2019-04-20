from flask import Flask, request, abort, render_template, jsonify, redirect
from minette import Minette
from minette.dialog import DialogService
from minette.tagger.mecabservice import MeCabServiceTagger
from minette.channel.line import LineAdapter
from dialog_router import MyDialogRouter
from tasks.scheduler import MyScheduler
from dialogs.specialecho import SpecialEchoDialogService
from controllers.endpoint import bp as endpoint_bp
from controllers.messagelog import bp as messagelog_bp
from controllers.liff import bp as liff_bp


# BOTのインスタンス化
bot = Minette.create(
    config_file="./minette.ini",
    dialog_router=MyDialogRouter,
    default_dialog_service=SpecialEchoDialogService,
    tagger=MeCabServiceTagger,
    # task_scheduler=MyScheduler  #タスクスケジューラーを利用するにはこの行をコメントアウト
)

# LINEアダプターの設定
line_adapter = LineAdapter(bot)

# Webアプリケーションのセットアップ
app = Flask(__name__)
app.line_adapter = line_adapter
app.register_blueprint(endpoint_bp)
app.register_blueprint(messagelog_bp)
app.register_blueprint(liff_bp)

# Webアプリケーションの起動
if __name__ == "__main__":
    # LINE Messaging APIのWebhook URL: https://あなたのサーバ/line/endpoint
    # メッセージログのURL: https://あなたのサーバ/messagelog?key=password
    app.run(host="0.0.0.0", port=21212)
