from minette.dialog import DialogRouter
from minette.session import Priority
from dialogs.translation import TranslationDialogService
from dialogs.weather import WeatherDialogService


class MyDialogRouter(DialogRouter):
    # ルーティングテーブルの設定
    def configure(self):
        self.intent_resolver = {
            "TranslationIntent": TranslationDialogService,
            "WeatherIntent": WeatherDialogService,
        }

    # インテントの抽出
    def extract_intent(self, request, session, connection):
        # ユーザープロフィールの更新
        if request.channel == "LINE" and request.channel_detail == "Messaging" and session.is_new:
            self.helpers["line_adapter"].update_profile(request.user)

        # 「翻訳」に完全一致で翻訳を開始
        if request.text == "翻訳":
            return "TranslationIntent", {}, Priority.Highest

        # 「天気」を含むとき天気情報を開始
        if "天気" in request.text:
            return "WeatherIntent", {}, Priority.Highest
