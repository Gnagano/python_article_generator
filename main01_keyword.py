import json
from janome.tokenizer import Tokenizer

# Chain / ChatOpenAI 
from chain.ChatOpenAIChain import MainKeywordGeneratorChain as mkc

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
  c_mk = mkc.MainKeywordGeneratorChain()
  problem = "勃起不全"
  solution = "バイアグラ"

  keywords = c_mk.get_response(problem=problem, solution=solution)
  
  res = []
  
  for keyword in keywords:
    keyword_modified = replace_particle_with_space(keyword)
    suggestKeywords = get_suggestions(keyword=keyword, lang="ja")
    res.append({"keyword": keyword_modified, "suggestKeywords": suggestKeywords})
  print(json.dumps(res, indent=2, ensure_ascii=False))

# スクリプトが直接実行された場合にのみmain()を呼び出す
if __name__ == '__main__':
  main()