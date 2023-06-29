import gspread
import json
import os
from oauth2client.service_account import ServiceAccountCredentials
import time

# LLM
import openai
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

# GSpread
from oauth2client.service_account import ServiceAccountCredentials
import gspread

# Constant
from config.config import Config as c

# Error
from error.errorReporter import error_console_report
from error.retry import sleep_for_retry

# Prompt
from prompt.PromptGenerator import ArticlePromptGenerator as apg
from prompt.PromptGenerator import ArticleTagPromptGenerator as tpg

DIR = dir_path = os.path.dirname(os.path.abspath(__file__))
ACCOUNT_PATH = abs_path = os.path.join(dir_path, 'credentials/service_account.json')

def get_google_credentials():
  with open (ACCOUNT_PATH) as f:
    account = json.load(f)
  return account

def getAnswerFromGPT (prompt, model="gpt-3.5-turbo"):
  chat = ChatOpenAI(model=model, temperature=0)
  msg = chat([HumanMessage(content=prompt)])
  return msg.content

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
  outputs = []
  interval_timeout_retry = c.CHAT_GPT_TIME_OUT_RETRY_INTERVAL
  
  # PromptGeneartor
  pg_a = apg.ArticlePromptGenerator()
  pg_t = tpg.ArticleTagPromptGenerator()

  for prompt_row in range(c.GSPREAD_SHEET_ROW_NUMBER_PROMPT, len(rows) + 1):
    retry = True
    while retry:
      # Read row
      title = rows[prompt_row - 1][prompt_column - 1]
      current_answer = rows[prompt_row - 1][answer_column - 1]

      # Prevent overwrite
      if current_answer:
        print(f"Skipping row {prompt_row + 1} due to existing answer.")
        prompt_row += 1
        start_row += 1
        retry = False
        continue

      # Return article
      print (title)
      try:

        # Create prompt
        prompt_article= pg_a.generate_prompt(title=title)
        prompt_tag = pg_t.generate_prompt(title=title)

        # Create answer from GPT
        article = getAnswerFromGPT(prompt_article)
        tag = getAnswerFromGPT(prompt_tag)

        # Console output
        print("----new article----")
        print(article)
        print(tag)

        # Update outputs
        outputs.append([article, tag])
        
        # If no exception, then no need to retry
        retry = False

        # Sleep 
        time.sleep(c.CHAT_GPT_SLEEP_TIME)
      except Exception as e:
        error_console_report(e)
        sleep_for_retry(interval_timeout_retry)

  print(f" article--->{len(outputs)}")
  range_articles=f'B{start_row}:C{start_row + len(outputs) - 1}' 
  worksheet.update(range_articles, outputs)


def main_test():
  # PromptGeneartor
  pg_a = apg.ArticlePromptGenerator()
  pg_t = tpg.ArticleTagPromptGenerator()

  title="test"
  prompt_article= pg_a.generate_prompt(title=title)
  prompt_tag = pg_t.generate_prompt(title=title)

  print(prompt_article)
  print(prompt_tag)

# スクリプトが直接実行された場合にのみmain()を呼び出す
if __name__ == '__main__':
  main()
  # main_test()