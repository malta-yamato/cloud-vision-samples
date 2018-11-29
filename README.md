
# English

## Overview

Python 3 (3.6 or higher) sample code for using the Cloud Vision API of GCP (Google Cloud Platform). Please clone the source code. Or when installing as a package, specify the repository with the pip command as follows.

pip install git+https://github.com/malta-yamato/cloud-vision-samples.git

When pip is used, the entry point of the command is also created. Please refer to the source code for details.

You need to obtain the API key to use the sample. If you do not use GCP yet, you will need to sign up. Please refer to the following for how to obtain the API key.

https://cloud.google.com/docs/authentication/api-keys

Of course, you need to enable this API. If you further use the API you will be charged on a metered basis. For APIs please read Google Sites carefully.


pip After installation you can use the Cloud Vision API with commands.

request_vision [image file name] --key [API key] --types [annotation type]:[maximum number of results]

Example) Annotate the logo in the image of google.jpg (The result is 1 piece)

request_vision google.jpg --key AIza... --types LO:1

We still display the result in json, but I would like to add functions sequentially.

#### Annotation type
FACE_DETECTION -> Face Detection (Abbreviation: F) <BR>
LANDMARK_DETECTION -> Landmark detection (Abbreviation: LM) <BR>
LOGO_DETECTION -> Logo Detection (Abbreviation: LO) <BR>
LABEL_DETECTION -> Label detection (Abbreviation: LA) <BR>
TEXT_DETECTION -> Text detection (Abbreviation: T) <BR>
SAFE_SEARCH_DETECTION -> Safe Image Detection (Abbreviation: S) <BR>


It is troublesome to enter the API key every time to execute the command. In that case, you can specify it with the environment variable GOOGLE_CLOUD_VISION_API_KEY before executing the command.

set GOOGLE_CLOUD_VISION_API_KEY=AIza...
(Such as MS-DOS)

export GOOGLE_CLOUD_VISION_API_KEY=AIza...
(Bash etc.)

Please like it.

It is not recommended to embed API key in source code etc. when using this script. This script is supposed to be executed on the local PC, and it is not possible to set usage restrictions by running applications or domains as API keys. So it means that you can issue API requests as much as you need with this API key. It is sad that inadvertent leakage of the API key and misuse of the cloud will result in misuse. Please keep in mind that saving the API key to a specific file is a risk.
Although it is a problem, if the virus check etc is solid, it is also probable that you make a permanent setting with Windows environment variable setting screen or .bashrc (.bash_profile) etc. (I am doing it Self-responsibility with demons!)



This script was created with reference to the following!

https://cloud.google.com/vision/docs/using-python
# 日本語

## 概要

GCP(Google Cloud Platform) の Cloud Vision API を利用するためのPython3(3.6以上)サンプルコードです。ソースコードをクローンしてください。またはパッケージとしてインストールする場合は以下のようにpipコマンドでリポジトリを指定します。

pip install git+https://github.com/malta-yamato/cloud-vision-samples.git

pipを使用した場合はコマンドのエントリポイントも作成されます。詳細はソースコードをご参照ください。

サンプルを使用するためにAPIキーを取得する必要があります。まだGCPを利用していない方はサインアップが必要になります。APIキーを取得する方法は以下をご参考下さい。

https://cloud.google.com/docs/authentication/api-keys

もちろん、このAPIを有効にする必要があります。さらにAPIを使用すれば従量制での課金がされます。APIについてはGoogleサイトを良くお読みください。


pipインストール後はコマンドにより、Cloud Vision API を使用することができます。

request_vision [イメージファイル名] --key [APIキー] --types [アノテーションタイプ]:[結果の最大数]

例) google.jpg の画像中にあるロゴをアノテーション(結果は1個まで)

request_vision google.jpg --key AIza... --types LO:1

まだ結果をjsonで表示するだけですが、機能を順次追加していきたいです。

####アノテーションタイプ
FACE_DETECTION -> 顔検出 (省略形: F)<BR>
LANDMARK_DETECTION -> ランドマーク検出  (省略形: LM)<BR>
LOGO_DETECTION -> ロゴ検出  (省略形: LO)<BR>
LABEL_DETECTION -> ラベル検出  (省略形: LA)<BR>
TEXT_DETECTION -> テキスト検出  (省略形: T)<BR>
SAFE_SEARCH_DETECTION -> セーフ画像検出  (省略形: S)<BR>


コマンドを実行するのに毎回APIキーを入力するのは面倒です。その場合はコマンド実行前に環境変数 GOOGLE_CLOUD_VISION_API_KEY で指定できます。

set GOOGLE_CLOUD_VISION_API_KEY=AIza...
(MS-DOSとか)

または、

export GOOGLE_CLOUD_VISION_API_KEY=AIza...
(Bashとか)

のようにしてください。

このスクリプトを利用するにあたりAPIキーをソースコード等に埋め込むのはお勧めしません。このスクリプトはローカルPCで実行することを想定しており、実行アプリケーションやドメインによる使用制限をAPIキーに設定することができません。ですから、このAPIキーを持っているだけで幾らでもAPIリクエストを発行できるということです。うっかりAPIキーを漏洩させて不正利用されてクラウド死することは悲しいです。特定のファイルにAPIキーを保存するのはリスクとなりますのでお気をつけください。
程度問題ですがウィルスチェック等がしっかりしているなら、Windowsの環境変数設定画面または.bashrc(.bash_profile)等で恒久的な設定をするのもありかなと思います（自分はそうしていますが、悪魔で自己責任で！）



このスクリプトは以下を参考に作成しました！

https://cloud.google.com/vision/docs/using-python
