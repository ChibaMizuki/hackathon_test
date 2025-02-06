import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import os

# WebDriverのセットアップ
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# 取得したいキーのリスト（※開講箇所は、CSV上では「開講場所」として扱う）
desired_keys = [
    "開講年度", "開講場所", "科目名", "担当教員", "学期曜日時限",
    "科目区分", "配当年次", "単位数", "使用教室", "キャンパス",
    "科目キー", "科目クラスコード", "授業で使用する言語", "授業方法区分",
    "大分野名称", "中分野名称", "小分野名称", "レベル", "授業形態",
    "教科書", "成績評価方法"
]

# CSVに保存するための準備
output_csv = "subject.csv"

# 既存のURLを取得
existing_urls = set()
if os.path.exists(output_csv):
    with open(output_csv, "r", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        try:
            next(reader)  # ヘッダーをスキップ
            for row in reader:
                if row:
                    existing_urls.add(row[0])
        except StopIteration:
            # ファイルが空の場合、ヘッダーを書き込む
            with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["URL"] + desired_keys)

# URLリストを読み込む
with open('urls.csv', 'r', encoding='utf-8') as url_file:
    urls = url_file.readlines()

# 各URLを処理
with open(output_csv, "a", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    if not existing_urls:  # 新規ファイルの場合はヘッダーを書き込む
        writer.writerow(["URL"] + desired_keys)

    for url in urls:
        url = url.strip()
        if not url or url in existing_urls:
            continue

        # URLにアクセス
        driver.get(url)
        time.sleep(3)  # ページが完全に読み込まれるまで待機

        # BeautifulSoupを使用してページの内容を解析
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # 全てのキーを nan で初期化した辞書を作成
        results = {key: "nan" for key in desired_keys}

        # 授業情報を含むテーブルを取得
        tables = soup.find_all("table", class_="ct-common ct-sirabasu")

        # 各テーブルの各行を処理
        for table in tables:
            for row in table.find_all("tr"):
                cells = row.find_all(['th', 'td'])
                if not cells or len(cells) < 2:
                    continue
                num_cells = len(cells)
                i = 0
                while i < num_cells - 1:
                    key_text = cells[i].get_text(strip=True)
                    value_text = cells[i + 1].get_text(strip=True)

                    # 「開講箇所」は「開講場所」として格納
                    if key_text == "開講箇所":
                        results["開講場所"] = value_text
                    elif key_text in results:
                        results[key_text] = value_text
                    i += 2

        # 各キーとその値を書き出す（desired_keys の順番で出力）
        writer.writerow([url] + [results[key] for key in desired_keys])

        time.sleep(2)  # 各URL処理後に3秒のインターバルを設ける

        print(f"URL '{url}' の情報をCSVに保存しました。")

print(f"CSVファイル '{output_csv}' に出力しました。")

# ブラウザを閉じる
driver.quit()