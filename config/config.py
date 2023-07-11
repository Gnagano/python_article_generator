class Config:
  # Google Spread Sheet
  GSPREAD_SHEET_SHEET_NAME="viagra01_test"
  GSPREAD_SHEET_SCOPES=['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

  # Google Spread Sheet / Worksheet
  GSPREAD_SHEET_WORKSHEET_NAME_ARTICLES="articles"
  GSPREAD_SHEET_COLUMN_NUMBER_PROMPT= 1
  GSPREAD_SHEET_COLUMN_NUMBER_ANSWER= 2
  GSPREAD_SHEET_ROW_NUMBER_PROMPT= 2

  # Chat GPT
  CHAT_GPT_SLEEP_TIME = 3
  CHAT_GPT_TIME_OUT_RETRY_INTERVAL = 60 # 1 minute

  # Google
  API_GOOGLE_SUGGEST_KEYWORDS = "https://www.google.co.jp/complete/search?output=toolbar"