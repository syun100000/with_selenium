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
        self.driver.implicitly_wait(10)  # ページの読み込みを待つ
        time.sleep(5)  # ページが完全に読み込まれるまで待機
        self.driver.maximize_window()  # ウィンドウを最大化
        time.sleep(5)  # ページが完全に読み込まれるまで待機
    def login(self):
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
    def save_cookies(self):
        cookies = self.driver.get_cookies() # クッキーを取得する
        pickle.dump(cookies,open(cookies_file,'wb')) # クッキーを保存する
    def load_cookies(self):
        if os.path.exists(cookies_file):
            cookies = pickle.load(open(cookies_file,'rb'))
            for cookie in cookies:
                self.driver.add_cookie(cookie)
            print("クッキーを読み込みました")
            # ページをリロードしてクッキーを適用する
            self.driver.get(LOGIN_AFTER_URL)
        else:
            print("クッキーが存在しません。ログインしてください。")
            self.login()
    def foryou(self):
        # 今日のおすすめをクリック
        self.driver.find_element(By.CSS_SELECTOR,'body > div.sp-container.with-header > div.search-container > div.search-for-you-tabs.parallel-buttons > a:nth-child(2)').click()
        
        
#テスト
if __name__ == "__main__":
    crawler = Crawler()
    crawler.start()
    # ここで必要な操作を実行
    # 例: ページのタイトルを取得
    title = crawler.driver.title
    print(f"Page title: {title}")
    # 例: ログイン処理
    crawler.load_cookies() # クッキーを読み込む
    
    
    
    #degug
    input("完了")
    # # 終了処理
    crawler.driver.quit()