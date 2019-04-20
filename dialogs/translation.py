"""
このスキルでは、Microsoft Cognitive ServicesのTranslator Text APIを利用しています。

https://azure.microsoft.com/ja-jp/services/cognitive-services/translator-text-api/

こちらにサインアップして、APIキーを取得したら、minette.iniの以下の項目に設定してください。

translation_api_key = YOUR_COGNITIVE_SERVICE_KEY
"""

import requests
from minette.dialog import DialogService


class TranslationDialogService(DialogService):
    # Process logic and build session data
    def process_request(self, request, session, connection):
        if session.topic.is_new:
            session.topic.status = "start_translation"
        elif request.text == "翻訳終わり":
            session.topic.status = "end_translation"
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
            session.data["translated_text"] = res[0]["translations"][0]["text"]
            session.topic.status = "process_translation"

    # Compose response message
    def compose_response(self, request, session, connection):
        if session.topic.status == "start_translation":
            session.topic.keep_on = True
            return "英語に翻訳したい文章を入力してください"
        elif session.topic.status == "end_translation":
            return "翻訳を終了しました"
        elif session.topic.status == "process_translation":
            session.topic.keep_on = True
            return session.data["translated_text"]
