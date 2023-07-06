# Chain / ChatOpenAI 
from chain.ChatOpenAIChain import MainKeywordGeneratorChain as mkc

def main():
  # Chain
  c_mk = mkc.MainKeywordGeneratorChain()
  problem = "勃起不全"
  solution = "バイアグラ"

  res = c_mk.get_response(problem=problem, solution=solution)

  print(res)

# スクリプトが直接実行された場合にのみmain()を呼び出す
if __name__ == '__main__':
  main()