from ollama import chat, ChatResponse
import os
from dotenv import load_dotenv
import pyperclip
# .envファイルを読み込む
load_dotenv()

def remove_non_bmp(text):
    # BMP外の文字を除去する（U+10000以上の文字を除外）
    return ''.join(c for c in text if ord(c) <= 0xFFFF)
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
    def create_initial_message(self, partner_name=None,partner_profile=None):
        if self.my_profile == "":
            raise ValueError("自分のプロフィールが設定されていません")
        if partner_profile == "":
            raise ValueError("相手のプロフィールが入力されていません")
        ai_prompt = f"私のプロフィールは{self.my_profile}です。"
        ai_prompt += f"相手の名前は{partner_name}です。"
        ai_prompt += f"相手のプロフィールは{partner_profile}です。"
        ai_prompt += "あなたはマッチングアプリで、相手に最初のメッセージを送るAIです。"
        ai_prompt += "このプロフィールをもとに、最初に相手が反応しやすいメッセージを作成してください。"
        ai_prompt += "相手のことはあなたではなくお名前でさん付けで呼んでください。"
        ai_prompt += "相手の名前は正しく呼んでください。"
        ai_prompt += "相手のプロフィールをよく理解して、自分と共通点がありそうであればそれを強調しなくても相手の興味を引くようなメッセージを作成してください。"
        ai_prompt += "文字数は150字以内でお願いします。"
        # モデルにプロンプトを送信
        count = 0
        while True:
            response: ChatResponse = chat(model=self.model_name, messages=[
                {
                    'role': 'user',
                    'content': ai_prompt,
                },
            ])
            res_len = len(response.message.content)
            count += 1
            if count > 10:
                raise ValueError("AIの生成が3回連続で200字を超えました。")
            if res_len < 200:
                break
            else:
                ai_prompt += "文字数は150字以内でお願いします。"
        return remove_non_bmp(response.message.content)

# DEBUG
if __name__ == "__main__":
    # OllamaClientのインスタンスを作成
    ollama_client = OllamaClient()

    # ユーザーから名前とプロフィールを手動入力
    partner_name = input("相手の名前を入力してください: ")
    # 改行2回で入力完了するように相手のプロフィールを入力
    print("相手のプロフィールを入力してください（改行2回で入力完了）:")
    partner_profile_lines = []
    while True:
        line = input()
        if line == "":
            break
        partner_profile_lines.append(line)
    partner_profile = "\n".join(partner_profile_lines)

    # AIでメッセージを生成
    initial_message = ollama_client.create_initial_message(partner_name, partner_profile)
    
    # 作成したメッセージを表示
    print("最初のメッセージ:", initial_message)

    # 自動でクリップボードにコピー
    try:
        pyperclip.copy(initial_message)
        print("メッセージをクリップボードにコピーしました。")
    except ImportError:
        print("pyperclipがインストールされていないため、クリップボードへのコピーは行いませんでした。")
