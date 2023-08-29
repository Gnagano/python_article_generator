import json
from janome.tokenizer import Tokenizer

# Chain / ChatOpenAI 
from chain.ChatOpenAIChain import MainKeywordGeneratorChain as mkc
from chain.ChatOpenAIChain import BlogThemeKeywordAssosicationScoreChain as btc

# Lib
from lib.google import get_suggestions

def replace_particle_with_space(text):
  t = Tokenizer()
  modified_sentence = ""
  for token in t.tokenize(text):
      if token.part_of_speech.startswith('助詞'):
        modified_sentence += ' '
      else:
        modified_sentence += token.surface
  return modified_sentence

def main():
  # Chain
  c_bt = btc.BlogThemeKeywordAssosicationScoreChain(version="1.0")
  problem = "勃起不全"
  solution = "バイアグラ"

  keywords = [
    "バカ",
    "勃起",
    "不能",
    "アホ",
  ]

  points = c_bt.get_response(problem=problem, solution=solution, keywords=keywords)
  print(points)
  
  # res = []
  
  # for keyword in keywords:
  #   keyword_modified = replace_particle_with_space(keyword)
  #   suggestKeywords = get_suggestions(keyword=keyword, lang="ja")
  #   res.append({"keyword": keyword_modified, "suggestKeywords": suggestKeywords})
  # print(json.dumps(res, indent=2, ensure_ascii=False))

# スクリプトが直接実行された場合にのみmain()を呼び出す
if __name__ == '__main__':
  main()