"""
LIFFの実体はHTTPSでアクセスするWebアプリケーションです。

事前にLINEログインチャンネルを作成し、LIFFを登録しておいてください
"""

from flask import (
    Blueprint,
    render_template,
    current_app
)

# メインから読み込むBlueprintの定義
bp = Blueprint("liff", __name__)


# LIFFの例
@bp.route("/liff/example")
def liff_example():
    liff_id = current_app.line_adapter.bot.config.get(section="liff", key="liff_id")
    return render_template("liff.html", liff_id=liff_id)
