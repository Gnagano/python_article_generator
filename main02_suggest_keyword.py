import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
from xml.sax.saxutils import unescape

# Constant
from config.config import Config as c

def get_suggestions(keyword, lang="en"):
  url = f"{c.API_GOOGLE_SUGGEST_KEYWORDS}&q={quote(keyword)}&hl={lang}"
  response = requests.get(url)
  soup = BeautifulSoup(response.content, features="xml")
  suggestions = soup.find_all('suggestion')
  print(suggestions)
  data_values = [suggestion['data'] for suggestion in suggestions]
  return data_values

def main():
  suggestions = (get_suggestions("テスト", "ja"))
  print(suggestions)

# スクリプトが直接実行された場合にのみmain()を呼び出す
if __name__ == '__main__':
  main()