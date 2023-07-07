import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
from xml.sax.saxutils import unescape

def get_suggestions(keyword, lang="en"):
  url = f"https://www.google.co.jp/complete/search?output=toolbar&q={quote(keyword)}&hl={lang}"
  response = requests.get(url)
  soup = BeautifulSoup(response.content, features="xml")
  suggestions = soup.find_all('suggestion')
  data_values = [suggestion['data'] for suggestion in suggestions]
  return data_values

def main():
  suggestions = (get_suggestions("テスト", "ja"))
  print(suggestions)

# スクリプトが直接実行された場合にのみmain()を呼び出す
if __name__ == '__main__':
  main()