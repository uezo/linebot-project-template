import traceback

from linebot import LineBotApi

from minette import DialogRouter
from minette import Priority

from dialogs.specialecho import SpecialEchoDialogService
from dialogs.translation import TranslationDialogService
from dialogs.weather import WeatherDialogService


class MyDialogRouter(DialogRouter):
    def __init__(self, config=None, timezone=None, logger=None,
                 default_dialog_service=None, **kwargs):
        super().__init__(
            config, timezone, logger, default_dialog_service, **kwargs)
        self.line_api = LineBotApi(
            channel_access_token=self.config.get(
                section="line_bot_api", key="channel_access_token"))

    # ルーティングテーブルの設定
    def register_intents(self):
        self.intent_resolver = {
            "TranslationIntent": TranslationDialogService,
            "WeatherIntent": WeatherDialogService,
            "EchoIntent": SpecialEchoDialogService
        }

    # インテントの抽出
    def extract_intent(self, request, context, connection):
        # ユーザープロフィールの更新
        self.update_profile(request, context)

        # 「翻訳」に完全一致で翻訳を開始
        if request.text == "翻訳":
            return "TranslationIntent"

        # 「天気」を含むとき天気情報を開始
        if "天気" in request.text:
            return "WeatherIntent"

        return "EchoIntent", {}, Priority.Low

    # ユーザープロフィールの更新
    def update_profile(self, request, context):
        if request.channel == "LINE" and request.channel_detail == "Messaging" and \
                request.user.channel_user_id is not None and context.is_new:
            try:
                profile = self.line_api.get_profile(request.user.channel_user_id)
                request.user.name = profile.display_name
                request.user.profile_image_url = profile.picture_url
            except Exception as ex:
                self.logger.error(
                    "Error occured in updating profile: "
                    + str(ex) + "\n" + traceback.format_exc())
