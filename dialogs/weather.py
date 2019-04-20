"""
このスキルでは、以下のAPIを利用しています。

- OpenWeatherMap https://openweathermap.org/api
- Microsoft Translator Text API https://azure.microsoft.com/ja-jp/services/cognitive-services/translator-text-api/

それぞれにサインアップして、APIキーを取得したら、minette.iniの以下の項目に設定してください。

weather_api_key = YOUR_WEATHER_SERVICE_KEY
translation_api_key = YOUR_COGNITIVE_SERVICE_KEY
"""

import requests
from minette.dialog import DialogService


class WeatherDialogService(DialogService):
    # 翻訳
    def translate(self, text, to_lang):
        api_url = "https://api.cognitive.microsofttranslator.com/translate?api-version=3.0&to=" + to_lang
        headers = {
            "Ocp-Apim-Subscription-Key": self.config.get("translation_api_key"),
            "Content-type": "application/json"
        }
        data = [{"text": text}]
        res = requests.post(api_url, headers=headers, json=data).json()
        return res[0]["translations"][0]["text"]

    # エンティティの抽出。リクエスト都度呼び出される
    def extract_entities(self, request, session, connection):
        areas = [w for w in request.words if w.part_detail2 == "地域"]
        return {"area": areas[0].surface if areas else ""}

    # Process logic and build session data
    def process_request(self, request, session, connection):
        session.data["area"] = request.entities["area"]
        if session.data["area"]:
            params = {
                "APPID": self.config.get("weather_api_key"),
                "q": self.translate(session.data["area"], "en")
            }
            res = requests.get("http://api.openweathermap.org/data/2.5/forecast", params=params).json()
            session.data["weather"] = self.translate(res["list"][0]["weather"][0]["main"], "ja")
        elif "終" in request.text:
            session.topic.status = "weather_end"

    # Compose response message
    def compose_response(self, request, session, connection):
        if session.data.get("weather", None):
            return "{}の天気は{}です".format(session.data["area"], session.data["weather"])
        elif session.topic.status == "weather_end":
            return "天気を中止します"
        else:
            session.topic.keep_on = True
            return "どこの天気を調べますか？"
