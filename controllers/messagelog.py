from flask import Blueprint, current_app, request, abort, render_template

# メインから読み込むBlueprintの定義
bp = Blueprint("messagelog", __name__)


# メッセージログのハンドラー
@bp.route("/messagelog", methods=["GET"])
def messagelog():
    # BOTインスタンスの取得
    bot = current_app.line_adapter.minette
    # パスワードのチェック
    if request.args.get("key", "") != bot.config.get("messagelog_password"):
        abort(401)
    # メッセージログの取得と表示
    ml = bot.get_message_log(count=int(request.args.get("count", 20)))
    return render_template("messagelog.html", ml=ml)
