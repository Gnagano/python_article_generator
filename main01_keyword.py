import json

# Chain / ChatOpenAI 
from chain.ChatOpenAIChain import MainKeywordGeneratorChain as mkc

# Lib
from lib.google import get_suggestions

def main():
  # Chain
  c_mk = mkc.MainKeywordGeneratorChain()
  problem = "勃起不全"
  solution = "バイアグラ"

  keywordObjects = c_mk.get_response(problem=problem, solution=solution)

  res = []
  
  for keywordObject in keywordObjects:
    keyword = keywordObject["keyword"]
    suggestKeywords = get_suggestions(keyword=keyword, lang="ja")
    res.append({"keyword": keyword, "suggestKeywords": suggestKeywords})
  # print(res)
  print(json.dumps(res, indent=2, ensure_ascii=False))

# スクリプトが直接実行された場合にのみmain()を呼び出す
if __name__ == '__main__':
  main()