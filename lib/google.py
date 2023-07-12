import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

# Constant
API_GOOGLE_SUGGEST_KEYWORDS = "https://www.google.co.jp/complete/search?output=toolbar"

def get_suggestions(keyword, lang="en"):
  url = f"{API_GOOGLE_SUGGEST_KEYWORDS}&q={quote(keyword)}&hl={lang}"
  response = requests.get(url)
  content = response.content.decode('shift_jis')
  soup = BeautifulSoup(content, features="xml")
  suggestions = soup.find_all('suggestion')
  data_values = [suggestion['data'] for suggestion in suggestions]
  return data_values