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
import config.config as c

# Prompt
from prompt.PromptGenerator import ArticlePromptGenerator as apg

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
  credentials = ServiceAccountCredentials.from_json_keyfile_dict(account, c.GSPREAD_SHEET_SCOPES)
  gc = gspread.authorize(credentials)
  worksheet = gc.open(c.GSPREAD_SHEET_SHEET_NAME).worksheet(c.GSPREAD_SHEET_WORKSHEET_NAME_ARTICLES)
  rows = worksheet.get_all_values()

  # Set start position of spreadsheet
  prompt_column = c.GSPREAD_SHEET_COLUMN_NUMBER_PROMPT
  answer_column = c.GSPREAD_SHEET_COLUMN_NUMBER_ANSWER
  start_row = c.GSPREAD_SHEET_ROW_NUMBER_PROMPT
  articles = []
  interval_timeout_retry = c.CHAT_GPT_TIME_OUT_RETRY_INTERVAL
  
  for prompt_row in range(c.GSPREAD_SHEET_ROW_NUMBER_PROMPT, len(rows) + 1):
    # Read row
    prompt = rows[prompt_row - 1][prompt_column - 1]
    current_answer = rows[prompt_row - 1][answer_column - 1]

    # Prevent overwrite
    if current_answer:
      print(f"Skipping row {prompt_row + 1} due to existing answer.")
      prompt_row += 1
      start_row += 1
      continue

    # Return article
    print (prompt)
    try:
      answer = getAnswerFromGPT(prompt)
      print("----new article----")
      print(answer)
      articles.append([answer])
      worksheet.update_cell(prompt_row, answer_column, str(answer).lstrip())
      prompt_row += 1
      time.sleep(c.CHAT_GPT_SLEEP_TIME)
    except Exception as e:
      print(f"An error occurred: {e}")
      print(f"--- Start time out retry interval {interval_timeout_retry} seconds ---")
      time.sleep(interval_timeout_retry)
      print(f"--- End time out retry interval ---")

  range_articles=f'B{start_row}:B{start_row + len(articles) - 1}' 
  worksheet.update(range_articles, articles)

def get_prompt_template_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        prompt_format = file.read()
    return prompt_format

def getAnswerFromGPT (prompt, model="gpt-3.5-turbo"):
  prompt_template = get_prompt_template_from_file('./prompt/article01.txt')
  prompt_formatted = prompt_template.format(prompt=prompt)

  response = openai.ChatCompletion.create(
    model=model,
    messages=[
      {"role": "user", "content": prompt_formatted},
    ]
  )
  return response['choices'][0]['message']['content']

def main_test():
  pg = apg.ArticlePromptGenerator()
  print(pg.generate_prompt(title="良いプロテインの選び方"))
  # article = getAnswerFromGPT("良いプロテインの選び方")
  # print(article)
  # format = get_prompt_format_from_file('./prompt/article01.txt')
  # print(format)

# スクリプトが直接実行された場合にのみmain()を呼び出す
if __name__ == '__main__':
    # main()
    main_test()