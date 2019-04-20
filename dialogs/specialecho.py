from minette.dialog import DialogService


# リクエスト情報やセッション情報を使ったおうむ返し
class SpecialEchoDialogService(DialogService):
    def compose_response(self, request, session, connection):
        # 前回の発話内容をセッションから取得
        previous_text = session.data.get("previous_text", "")

        # 今回の発話内容をセッションに格納
        session.data["previous_text"] = request.text

        # 発話内容から名詞を抽出
        noun = [w.surface for w in request.words if w.part == "名詞"]

        # この対話を継続することでセッション情報を維持
        session.topic.keep_on = True

        # 応答メッセージの組み立て
        ret = "こんにちは、{}さん。今回は'{}'って言ったね。前回は'{}'って言ってたよ".format(
            request.user.name, request.text, previous_text
        )
        ret += "\n含まれる名詞: {}".format("、".join(noun)) if noun else ""
        return ret
