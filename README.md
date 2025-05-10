# with_selenium
現在開発中
## 概要
本プロジェクトは、マッチングアプリ「with」のWebページをSeleniumを用いて自動操作し、ユーザー情報の取得や自動メッセージ送信を行うPythonスクリプト群です。AIによるメッセージ生成にはOllamaを利用しています。

## 主な機能
- Seleniumによるwithの自動ログイン・クッキー管理
- おすすめユーザーの自動取得とプロフィール情報の抽出
- Ollama APIを用いたAIによる初回メッセージ自動生成
- 生成メッセージの自動送信（手動確認あり）

## ディレクトリ構成
```
with_selenium/
├── .env                # 環境変数（APIキーやプロフィール等）
├── main.py             # メイン実行ファイル
├── constraints.txt     # 依存ライブラリバージョン指定
├── with_api/           # Seleniumによる自動化関連
│   ├── crawl.py
│   └── __int__.py
├── with_ollama/        # Ollamaクライアント関連
│   ├── client.py
│   └── __int__.py
└── README.md           # 本ドキュメント
```

## セットアップ方法

1. 必要なPythonパッケージのインストール
    ```sh
    pip install -r constraints.txt
    ```

2. `.env`ファイルを作成し、必要な情報（電話番号、パスワード、プロフィール等）を記載してください。

3. ChromeDriverのパスを環境に合わせて`with_api/crawl.py`内で修正してください。

## 実行方法

```sh
python main.py
```

- 初回実行時は手動でreCAPTCHAやSMS認証が必要です。
- 以降はクッキーによる自動ログインが可能です。

## 依存ライブラリ
- selenium
- python-dotenv
- ollama
- pyperclip
- その他`constraints.txt`参照

## 注意事項
- 本コードは学習・研究目的で作成されています。利用は自己責任でお願いします。
- withの利用規約や自動化禁止事項に十分ご注意ください。

## ライセンス
MITライセンス


