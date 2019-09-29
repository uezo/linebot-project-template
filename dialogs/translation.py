"""
このスキルでは、Microsoft Cognitive ServicesのTranslator Text APIを利用しています。

https://azure.microsoft.com/ja-jp/services/cognitive-services/translator-text-api/

こちらにサインアップして、APIキーを取得したら、minette.iniの以下の項目に設定してください。

translation_api_key = YOUR_COGNITIVE_SERVICE_KEY
"""

import requests
from minette.dialog import DialogService


class TranslationDialogService(DialogService):
    # Process logic and build context data
    def process_request(self, request, context, connection):
        if context.topic.is_new:
            context.topic.status = "start_translation"
        elif request.text == "翻訳終わり":
            context.topic.status = "end_translation"
        else:
            # 英語に翻訳（to=en）
            api_url = "https://api.cognitive.microsofttranslator.com/translate?api-version=3.0&to=en"
            # ヘッダにAPIキーをセット
            headers = {
                "Ocp-Apim-Subscription-Key": self.config.get("translation_api_key"),
                "Content-type": "application/json"
            }
            # リクエストの発話内容を送信データにセット
            data = [{"text": request.text}]
            # APIの呼び出しと結果のセッションへの格納
            res = requests.post(api_url, headers=headers, json=data).json()
            context.data["translated_text"] = res[0]["translations"][0]["text"]
            context.topic.status = "process_translation"

    # Compose response message
    def compose_response(self, request, context, connection):
        if context.topic.status == "start_translation":
            context.topic.keep_on = True
            return "英語に翻訳したい文章を入力してください"
        elif context.topic.status == "end_translation":
            return "翻訳を終了しました"
        elif context.topic.status == "process_translation":
            context.topic.keep_on = True
            return context.data["translated_text"]
