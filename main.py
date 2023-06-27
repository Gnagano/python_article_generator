import gspread
import json
import os
import openai
from oauth2client.service_account import ServiceAccountCredentials
import time

# GSpread
from oauth2client.service_account import ServiceAccountCredentials
import gspread

# Constant
from config.config import GSPREAD_SHEET_SHEET_NAME, GSPREAD_SHEET_SCOPES

DIR = dir_path = os.path.dirname(os.path.abspath(__file__))
ACCOUNT_PATH = abs_path = os.path.join(dir_path, 'credentials/service_account.json')

def get_google_credentials():
  with open (ACCOUNT_PATH) as f:
    account = json.load(f)
  return account

def getAnswerFromGPT (prompt):
  PROMPT_FORMAT = f"""
    Generate blog title with provided theme

    Theme:[{prompt}]

    Generates 3 blog chapters with the given title and list
    Generates a given title and a detailed book description of over 500 words
    Then use markdown. Use prefaces, headings, subheadings, bold, and summaries to organize information.

    Write the theme
    Write the preface with detailed information and more than 300
    Write Chapter 1 with detailed information and more than 500
    Write Chapter 2 with detailed information and more than 500
    Write Chapter 3 with detailed information and more than 500
    Write the summarie with detailed information and more than 500

    # Output Language
    日本語

    # Output Style
    <h2>プリフェース</h2>
    {{ プリフェースの文章 }}

    <h2>1.{{Chapter1のタイトル}}</h2>
    {{ Chapter1の文章 }}

    <h2>2.{{Chapter2のタイトル}}</h2>
    {{ Chapter2の文章 }}

    <h2>3.{{Chapter3のタイトル}}</h2>
    {{ Chapter3の文章 }}

    <h2>まとめ</h2>
    {{ Summarieの文章 }}
  """

  response = openai.ChatCompletion.create(
    # model="gpt-4",
    model="gpt-3.5-turbo",
    messages=[
      {"role": "user", "content": PROMPT_FORMAT},
    ]
  )
  return response['choices'][0]['message']['content']

def main():

  # Authorization
  account = get_google_credentials()
  credentials = ServiceAccountCredentials.from_json_keyfile_dict(account, GSPREAD_SHEET_SCOPES)
  gc = gspread.authorize(credentials)


  worksheet = gc.open(GSPREAD_SHEET_SHEET_NAME).worksheet('articles')

  prompt_column = 1
  answer_column = 2
  prompt_row = 2

  while worksheet.cell(prompt_row, prompt_column).value is not None:
    prompt = worksheet.cell(prompt_row, prompt_column).value
    current_answer = worksheet.cell(prompt_row, answer_column).value

    # Prevent overwrite
    if current_answer is not None:
      print(prompt_row)
      prompt_row += 1
      time.sleep(5)
      continue

    # Return article
    print (prompt)
    answer = getAnswerFromGPT(prompt)
    print("----new article----")
    print(answer)
    worksheet.update_cell(prompt_row, answer_column, str(answer).lstrip())
    prompt_row += 1

# スクリプトが直接実行された場合にのみmain()を呼び出す
if __name__ == '__main__':
    main()