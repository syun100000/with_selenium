# インポート
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import pickle
from functools import wraps
from with_ollama import client
URL = 'https://with.is/welcome'
LOGIN_AFTER_URL = 'https://with.is/'
# envファイルから各情報を取得
# .envファイルを読み込む
from dotenv import load_dotenv
load_dotenv()
# 環境変数を取得
ID_TEL = os.getenv('ID_TEL')
PASSWORD = os.getenv('PASSWORD')
cookies_file = 'cookies.pkl'

def require_started(func):
    """
    Crawlerが起動しているかを確認するデコレータ
    """
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if not self.started:
            raise RuntimeError("Crawlerは起動していません。先にstart()メソッドを呼び出してください。")
        return func(self, *args, **kwargs)
    return wrapper

class Crawler:
    def __init__(self):
        self.url = URL
        self.driver = None
        self.service = None
        self.options = None
        self.wait = None
        self.started = False

    def setup_driver(self):
        # Chromeのオプションを設定
        self.options = Options()
        # self.options.add_argument('--headless')  # ヘッドレスモード
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        
        # ChromeDriverのパスを指定
        chrome_driver_path = os.path.join(os.getcwd(), '/opt/homebrew/bin/chromedriver')
        self.service = Service(chrome_driver_path)
        
        # WebDriverの初期化
        self.driver = webdriver.Chrome(service=self.service, options=self.options)
        self.wait = WebDriverWait(self.driver, 10)
    # 起動処理
    def start(self):
        self.setup_driver()
        self.driver.get(self.url)
        self.started = True
        self.driver.implicitly_wait(5)  # ページの読み込みを待つ
        # 例: ログイン処理
        self.load_cookies() # クッキーを読み込む
    def login(self):
        if not self.started:
            raise Exception("Crawler has not been started. Call start() method first.")
        print("ログイン処理を開始します")
        self.driver.find_element(By.CSS_SELECTOR,'body > div.sp-container > div.global-nav_header.for-pc.is-modest > div').click()
        self.driver.find_element(By.CSS_SELECTOR,'#sign-in-dialog > a.button.sms-button.mbm').click()
        time.sleep(2)
        phoneNumber_input = self.driver.find_element(By.NAME,'phoneNumber')
        print("電話番号を入力します")
        phoneNumber_input.send_keys(ID_TEL)
        time.sleep(2)
        print("送信ボタンをクリックします") #submit
        self.driver.find_element(By.CSS_SELECTOR,'#auth-container > div > form > div.firebaseui-card-actions > div > button.firebaseui-id-submit.firebaseui-button.mdl-button.mdl-js-button.mdl-button--raised.mdl-button--colored').click()
        input("recaptchaを解いてください。完了後にEnterを押してください。")
        input("SMS認証コードを入力してください。完了後にEnterを押してください。")
        self.save_cookies() # クッキーを保存する
        print("クッキーを保存しました")

    @require_started
    def save_cookies(self):
        cookies = self.driver.get_cookies() # クッキーを取得する
        pickle.dump(cookies, open(cookies_file, 'wb')) # クッキーを保存する

    @require_started
    def load_cookies(self):
        if os.path.exists(cookies_file):
            cookies = pickle.load(open(cookies_file, 'rb'))
            for cookie in cookies:
                self.driver.add_cookie(cookie)
            print("クッキーを読み込みました")
            # ページをリロードしてクッキーを適用する
            self.driver.get(LOGIN_AFTER_URL)
        else:
            print("クッキーが存在しません。ログインしてください。")
            self.login()

    @require_started
    def foryou(self):
        # 今日のおすすめをクリック
        self.driver.find_element(By.CSS_SELECTOR, 'body > div.sp-container.with-header > div.search-container > div.search-for-you-tabs.parallel-buttons > a:nth-child(2)').click()
        # おすすめ一覧を取得
        recomend_user_list = self.driver.find_element(By.CSS_SELECTOR, '#for-you-pickup-user')
        # 各ユーザーの要素ごとに取得
        user_elements = recomend_user_list.find_elements(By.CLASS_NAME, 'touching-effect-user-card')
        for user in user_elements:
            # 一番最初のaタグをクリック
            user.find_element(By.TAG_NAME, 'a').click()
            # ページが読み込まれるまで待機
            time.sleep(2)
            user_name = self.driver.find_element(By.CLASS_NAME,'profile_main-nickname').text
            user_age_address = self.driver.find_element(By.CLASS_NAME, 'profile_main-age-address').text
            # 年齢と住所を分解して変数に保存
            user_age, user_address = user_age_address.split(' ')
            user_age = int(user_age.replace('歳', ''))  # 年齢を整数に変換
            print(f"ユーザー名: {user_name}, 年齢: {user_age}, 住所: {user_address}")
            user_profile = self.driver.find_element(By.CLASS_NAME, 'profile-introduction_content').text
            print(f"ユーザープロフィール: {user_profile}")
            # いいねボタンをクリック
            self.driver.find_element(By.CLASS_NAME, 'button-like').click()
            #　初回はヘルプが出てくるので、タブを戻る
            time.sleep(2)  # ページが完全に戻るまで待機
            # input("test")
            # メッセージをつけるにチェックを入れる
            self.driver.find_element(By.CSS_SELECTOR,'#new_like > div.like-dialog_like-type-button.attached-message_checkbox').click()
            # 初回などにtitle-areaにメッセージ付きいいね！を送ろうというページが出てくるのででてきた場合は戻る
            # 前のタブに切り替え
            self.driver.switch_to.window(self.driver.window_handles[0])
            
            # AIにメッセージを作成してもらう
            ollama_client = client.OllamaClient()
            initial_message = ollama_client.create_initial_message(user_name, user_profile)
            print(f"AIが作成したメッセージ")
            print(initial_message)
            # メッセージを入力
            message_input = self.driver.find_element(By.ID,'message')
            message_input.send_keys(initial_message)
            # 送信ボタンをクリック
            input("メッセージを送信するにはEnterを押してください。")
            send_button = self.driver.find_element(By.NAME,'button')
            # 送信ボタンを画面内にスクロール（必要なら）
            self.driver.execute_script("arguments[0].scrollIntoView(true);", send_button)
            # JavaScriptでクリック（範囲外や被り対策）
            self.driver.execute_script("arguments[0].click();", send_button)
            time.sleep(3)  # ページが完全に戻るまで待機
#テスト
if __name__ == "__main__":
    crawler = Crawler()
    crawler.start()

    
    
    
    #degug
    input("完了")
    # # 終了処理
    crawler.driver.quit()