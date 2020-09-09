from flask import (
    Blueprint,
    current_app,
    request,
    abort,
    render_template
)

from minette.serializer import loads

# メインから読み込むBlueprintの定義
bp = Blueprint("messagelog", __name__)


# メッセージログのハンドラー
@bp.route("/messagelog", methods=["GET"])
def messagelog():
    # BOTインスタンスの取得
    bot = current_app.line_adapter.bot
    # パスワードのチェック
    if request.args.get("key", "") != bot.config.get("messagelog_password"):
        abort(401)
    # メッセージログの取得と表示（やっつけなのでプロダクションではクエリやテーブルをきちんとチューニングしてください）
    with bot.connection_provider.get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("select * from messagelog order by id desc limit 50")
        ml = []
        for r in cursor.fetchall():
            d = dict(zip([column[0] for column in cursor.description], r))
            d["request_json"] = loads(d["request_json"])
            d["context_json"] = loads(d["context_json"])
            d["response_json"] = loads(d["response_json"])
            ml.append(d)
    return render_template("messagelog.html", ml=ml)
