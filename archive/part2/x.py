#https://blockexplorer.minepi.com/


# BeautifulSoupをインポート
import requests
import bs4
from bs4 import BeautifulSoup

#「手っ取り早くPython3.xをダウンロードして使ってみる(Mac)！はじめてのPython」のURLを指定
url = "https://programmer-life.work/python/use-python3-mac"

# ページのHTML(ソース)を取得
html = requests.get(url)

# BeautifulSoupで解析(=parser)
soup = BeautifulSoup(html.content, "html.parser")

# テキストファイルへ結果を書き込み

# 書き込むファイルを指定
fileName = "test.txt"
# ファイルを開く
with open(fileName, "a") as f:
    for element in soup.find_all("a"):
        url = str(element.get("href"))
        f.write(url+"\n")