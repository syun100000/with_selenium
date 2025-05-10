from ollama import chat, ChatResponse
import os
from dotenv import load_dotenv

# .envファイルを読み込む
load_dotenv()

# ベースプロンプト
bese_prompt = ""


class OllamaClient:
    def __init__(self):
        # .envからモデル名とURLを取得
        self.model_name = os.getenv('OLLAMA_MODEL')
        self.my_profile = os.getenv('MY_PROFILE')

        # モデル名が設定されていない場合は例外をスロー
        if not self.model_name:
            raise ValueError("OLLAMA_MODELが設定されていません。環境変数を確認してください。")

        print(f"モデル: {self.model_name}")

    # 自分のプロフィールと相手のプロフィールを参照しはじめのメッセージを作成
    def create_initial_message(self, partner_name,partner_profile):
        if self.my_profile == "":
            raise ValueError("自分のプロフィールが設定されていません")
        if partner_profile == "":
            raise ValueError("相手のプロフィールが入力されていません")
        ai_prompt = f"私のプロフィールは{self.my_profile}です。"
        ai_prompt += f"相手の名前は{partner_name}です。"
        ai_prompt += f"相手のプロフィールは{partner_profile}です。"
        ai_prompt += "あなたはマッチングアプリで、相手に最初のメッセージを送るAIです。"
        ai_prompt += "このプロフィールをもとに、最初に相手が反応しやすいメッセージを作成してください。"
        ai_prompt += "相手のプロフィールをよく理解して、自分と共通点がありそうであればそれを強調しなくても相手の興味を引くようなメッセージを作成してください。"
        ai_prompt += "文字数は300字以内でお願いします。"
        # モデルにプロンプトを送信
        response: ChatResponse = chat(model=self.model_name, messages=[
            {
                'role': 'user',
                'content': ai_prompt,
            },
        ])
        return response.message.content

# DEBUG
if __name__ == "__main__":
    # OllamaClientのインスタンスを作成
    ollama_client = OllamaClient()
    partner_name = "なな"
    partner_profile = (
        "はじめまして、こんにちは。\n"
        "東京出身のななといいます🧸\n\n"
        "好きなことは食べることと寝ること🐑とゲームで\n"
        "休みの日は美味しいものを探したり、お昼寝したりゲームしていることが多いです。\n\n"
        "周りには大人っぽいと言って貰えることが事多いですが、\n"
        "私自身はほんとかな？と感じています\n\n"
        "恋愛では、信頼の中で相手に委ねて、安心して甘えられるような関係が理想です。\n"
        "主導権を持って引っ張ってくれる相手に安心します！\n\n"
        "表面的な優しさより、ちゃんと見て、理解して大事にしてくれる人とゆっくり深く関係を育てられたら嬉しいです。\n\n"
        "興味もっていただけたらメッセください！\n"
    )
    # 最初のメッセージを作成
    initial_message = ollama_client.create_initial_message(partner_name, partner_profile)
    
    # 作成したメッセージを表示
    print("最初のメッセージ:", initial_message)
