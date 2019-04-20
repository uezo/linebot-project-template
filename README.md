# LINEBOT Project Template

本格的なLINEBOTを爆速で開発するためのプロジェクトテンプレート。コンテキスト管理やユーザー管理、自然言語解析処理、メッセージログ閲覧といった機能が最初から組み込まれているほか、LIFFやリッチメニューのサンプル、翻訳スキルと天気予報スキルのサンプルコードも同梱しています。

# 事前準備

本手順を実施する前に、インターネットからアクセスできる環境を準備するのと、LINE Messaging APIの利用に必要な手続きを完了する必要があります。既にLINE BOTを運用していて適当な`Channel Secret`と`Channel Access Token`をお持ちの方は依存ライブラリのインストールのみでOKです。

## PCをインターネットからアクセスできるようにする

LINEからリクエストを受信するため、[ngrok](https://ngrok.com)を導入してPCにインターネット経由でアクセスできるようにします。Azureの仮想マシンやAWSのEC2インスタンスなど既にお持ちの場合は本手順は必須ではありませんが、お手元のPCで実機デバッグできる方が便利です。

[ngrokのダウンロードページ](https://ngrok.com/download)からご自身の環境に適したバイナリをダウンロードしてパスを通してください。Macの場合は以下のコマンドでもインストールできます。

```
$ brew install ngrok
```

インストールが完了したら以下のコマンドを実行して動作確認します。`Ctrl+C`で終了できますが、URLが都度変わりますのでチャットボットを動作させるまで終了しないようにしてください。

```
$ ngrok http 21212
```

以下のように表示されたら起動成功です。この例では、`https://9b41ad02.ngrok.io`にアクセスすると、あなたのPCの`localhost:21212`にリクエストがトンネルされることを意味しています。

```
ngrok by @inconshreveable                                       (Ctrl+C to quit)
                                                                                
Session Status                online                                            
Account                       Yuji Ueki (Plan: Pro)                             
Update                        update available (version 2.3.25, Ctrl-U to update
Version                       2.2.8                                             
Region                        United States (us)                                
Web Interface                 http://127.0.0.1:4041                             
Forwarding                    http://9b41ad02.ngrok.io -> localhost:21212       
Forwarding                    https://9b41ad02.ngrok.io -> localhost:21212      
                                                                                
Connections                   ttl     opn     rt1     rt5     p50     p90       
                              2       0       0.03    0.01    0.00    0.01
```


## LINE Messaging APIの準備

APIを利用するためのアカウントを作成し、各種設定を行います。ゴールは`Channel Secret`と`Channel Access Token`を取得し、先ほど作成したURLをWebhookに設定することです。

- プロバイダとMessaging APIのチャネルを作成。この記事を見ればすぐにできます→ [LINEのBot開発 超入門（前編） ゼロから応答ができるまで](https://qiita.com/nkjm/items/38808bbc97d6927837cd#channelを作成する)
- Webhook URLを設定。このURLめがけてユーザーが発話した内容をLINEが送ってくれます。設定する値は先の例だと https://9b41ad02.ngrok.io/line/endpoint となります


## 依存ライブラリのインストール

PyPIからLINE公式のPythonSDKとチャットボットフレームワークのMinetteをインストールします。今回のプロジェクトテンプレートは[Minette for Python](https://github.com/uezo/minette-python)というチャットボットフレームワークを活用するものです。

```
pip install line-bot-sdk minette requests flask
```

# プロジェクトテンプレートの入手と設定

このリポジトリをCloneするか、ZIPでダウンロードして解凍したら適当なディレクトリ（ユーザーホーム直下とか）に配置してください。配置が完了したらディレクトリ内に移動して設定ファイル`minette.ini`を編集します。ここにLINE Developersで取得したChannel SecretとChannel Access Tokenを設定してください。

``` minette.ini
[line_bot_api]
channel_secret = YOUR_CHANNEL_SECRET
channel_access_token = YOUR_CHANNEL_ACCESS_TOKEN
```

# 実行

これで準備は完了しました。チャットボットを起動してLINEアプリから話しかけてみましょう。

```
$ python run.py

2019-04-17 21:48:01,443 - minette.core - WARNING - Do not use MeCabService tagger for the production environment. This is for trial use only. Install MeCab and use MeCabTagger instead.
2019-04-17 21:48:01,444 - minette.core - INFO - Create 16 worker thread(s)
 * Serving Flask app "run" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://0.0.0.0:21212/ (Press CTRL+C to quit)
```

おうむ返しに加えて、前回発話内容の表示、ユーザー名の表示、そして発話に含まれる名詞の抽出をしてくれると思います。つまり、コンテキスト情報の管理や自然言語解析処理（形態素解析）がすぐに利用できるということをお分かりいただけたかと思います。

<img src="https://github.com/uezo/linebot-project-template/blob/master/images/screenshot01.png" alt="実行結果" height="333">

※起動時にメッセージが出力される通り、**形態素解析機能の`MeCabService tagger`は本番利用には適していません**。ご自身の環境に[MeCab]をインストールして、`MeCabTagger`をご利用いただくか、以下の通り`run.py`を編集して形態素解析をオフにしてください。

``` run.py
# BOTのインスタンス化
bot = Minette.create(
    config_file="./minette.ini",
    dialog_router=MyDialogRouter,
    default_dialog_service=SpecialEchoDialogService,
    # tagger=MeCabServiceTagger,    # ⭐️この行をコメントアウト
)
```

なお[Minette](https://github.com/uezo/minette-python)では1つの話題ごとに1つの処理部品（クラス）を用意するような構造になっています。今回のおうむ返し＋αのコードの中身は以下の通りです。

``` SpecialEchoDialog.py
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
```

# 自分でスキルを追加する

[Minette](https://github.com/uezo/minette-python)では`DialogRouter`と呼ばれる部品でユーザーの意図を解釈し、コンテキストを踏まえて適切と思われる話題にリクエストを振り分けます。そして、`DialogService`と呼ばれる話題毎の処理部品でリクエストを処理し、応答メッセージをユーザーに返します。

ここでは純粋なおうむ返し対話処理部品の`DialogService`を作成し、それを`DialogRouter`に登録するという流れで説明していきます。

## DialogServiceの作成

このテンプレートでは`dialogs`フォルダの中に各対話処理部品をまとめていますので、ここに`echo.py`を追加したら、以下の通りコードを追加してください。

``` echo.py
from minette.dialog import DialogService

class EchoDialogService(DialogService):
    def compose_response(self, request, session, connection):
        return "You said: {}".format(request.text)
```

簡単に解説すると、`compose_response`メソッドは応答メッセージを組み立てる処理で、定型文に`request`オブジェクトの`text`プロパティの値を埋め込んだものを戻り値としています。

## DialogRouterへの登録

作成したおうむ返しスキルをどのようなときに呼び出すか、ということを設定します。プロジェクトの最上位ディレクトリに戻って、`dialog_router.py`を開いて以下の通りコードを追加します。

まずは冒頭に先ほど作成した`EchoDialogService`のインポート文を追加。

``` dialog_router.py
from dialogs.echo import EchoDialogService      # ⭐ ️追加 1
```

続いて、`configure`メソッドでインテント`EchoIntent`に`EchoDialogService`を紐づけるように設定。

``` dialog_router.py
    # ルーティングテーブルの設定
    def configure(self):
        self.intent_resolver = {
            "TranslationIntent": TranslationDialogService,
            "WeatherIntent": WeatherDialogService,
            "EchoIntent": EchoDialogService     # ⭐ ️追加 2
        }
```

最後に、発話内容が「おうむ」で始まっているときに`EchoIntent`として解釈するよう、`extract_intent`メソッドの末尾に追加。戻り値の2つ目はエンティティ、3つ目はこのインテントの処理優先度を示しています。今回はHighestを指定していますので、いかなる話題も中断されておうむ返しをしてくれるようになります。

``` echo.py
        # ⭐ ️以下、追加 3

        # 「おうむ」から始まるときおうむ返し
        if request.text.startswith("おうむ"):
            return "EchoIntent", {}, Priority.Highest
```

なおこの`extract_intent`から[LUIS](https://www.luis.ai/home)などを呼び出し、その結果をそのままリターンすることでインテリジェントチャットボットを作ることができます。個人的にはルールベースとそれら自然言語処理サービスとを組み合わせることで、シナリオ進行に制御をきかせつつ柔軟な解釈も可能にするというのがオススメです。

## 動作確認

これで準備は整いました。`Ctrl+C`でチャットボットを停止し、`run.py`を実行して再起動したらLINEアプリで会話を試してみてください。

<img src="https://github.com/uezo/linebot-project-template/blob/master/images/screenshot02.png" alt="実行結果" height="333">


# メッセージログの確認

品質のよいチャットボットに育て上げていくためには、ユーザーの発話に対して適切な回答を返せているか、冗長な対話シナリオになっていないかということを確認し、日々改善を行っていくことがとても重要です。

そういった取り組みを支援するため、このテンプレートでは対話のログをブラウザベースでいつでもどこでも確認できるような仕組みを提供しています。チャットボットが起動した状態で、今回の例だと https://9b41ad02.ngrok.io/messagelog?key=password にアクセスすることで閲覧できます。**アクセスキーのパラメータ`key`は`minette.ini`で変更することができますので、必ず変更しましょう。**

<img src="https://github.com/uezo/linebot-project-template/blob/master/images/screenshot03.png" alt="メッセージログ" height="333">

ユーザーとチャットボットそれぞれの発話内容に加えて、インテント、話題とそのステータス、処理時間などが表示されます。エンティティが抽出された場合はその内容も記録されるため、発話内容をどのように解釈し、どのような処理を行ったかがわかるようになっています。


# さいごに

作例として、翻訳スキルと天気予報スキルの対話処理部品のサンプル実装を同梱しますので参考にしてみてください。またデータベースはデフォルトでSQLiteになっていますが、SQL DatabaseとMySQLにも対応していますので処理負荷などを考慮してそれらのデータベースを利用することをお勧めします。利用方法は[Minetteのexamplesの設定ファイル](https://github.com/uezo/minette-python/blob/master/examples/minette.ini)を参照してください。

その他解説はしょりすぎな部分が多々あるかと思いますので、不明点がありましたらIssueに投げていただくかTwitter: [@uezochan](https://twitter.com/uezochan)までお気軽にお問い合わせください。

なお[Minette](https://github.com/uezo/minette-python)を使って以下のチャットボットを開発しました。よかったらお友だちになってください！[あにBOT](https://twitter.com/uezochan/status/1116683189689315330)はこのテンプレートで実質2〜3日くらいで作ったものです。荒削りなのでこれから育てます。

- [いもうとBOT](http://imoutobot.com)
- [あにBOT](https://twitter.com/uezochan/status/1116683189689315330)


それでは、Enjoy creating awesome LINEBOT!


# 参考: Minetteの主な特長

このプロジェクトテンプレートのベースとなるフレームワーク[Minette for Python](https://github.com/uezo/minette-python)の主な特長は以下の通りです。

- コンテキスト管理　発話をまたいで情報を引き継ぐ機能。インタラクティブな対話を可能にします
- ユーザー管理　LINEのユーザーIDをキーに自動的にユーザー情報を保存し、スキル内で利用することができます
- 形態素解析　発話内容は自動的にMeCabによる形態素解析が行われ、スキルの中で利用することができます
- メッセージログ　ユーザーとBOTの話した内容やその際のトピック、コンテキスト情報、エンティティなどが記録されます
- スケジューラ　定期的なタスクを実行する機能。Cron等を利用することなくすべてチャットボットのリソースで完結します
- 並列処理　長時間かかる処理を行っていても他のユーザーのリクエストに応答できます（LINEのみ）。並列処理してもコンテキストの整合性は保たれます
- 統一的なアーキテクチャ　LINEもClovaも同じアーキテクチャで開発することができます

