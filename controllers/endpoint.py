from flask import (
    Blueprint,
    current_app,
    request
)

# メインから読み込むBlueprintの定義
bp = Blueprint("endpoint", __name__)


# LINE Messaging APIからのWebhookのリクエストハンドラー
@bp.route("/line/endpoint", methods=["POST"])
def line_endpoint():
    current_app.line_adapter.handle_http_request(request.data, request.headers)
    return "ok"
