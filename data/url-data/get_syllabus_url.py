from bs4 import BeautifulSoup
import csv

# HTMLファイルを読み込む
html_file_path = 'syllabus.html'  # ここにHTMLファイルのパスを指定
with open(html_file_path, 'r', encoding='utf-8') as file:
    html_content = file.read()

# BeautifulSoupを使用してHTMLを解析
soup = BeautifulSoup(html_content, 'html.parser')

# URLを取得
urls = []
for a_tag in soup.find_all('a', href=True):
    if 'https://www.wsl.waseda.jp/syllabus/JAA104.php' in a_tag['href']:
        urls.append(a_tag['href'])

# CSVに保存
output_csv = "urls.csv"
with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    # 各URLを書き出す（ヘッダーなし）
    for url in urls:
        writer.writerow([url])

print(f"CSVファイル '{output_csv}' に出力しました。")