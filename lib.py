from gensim.models import Word2Vec
import MeCab

m = MeCab.Tagger("-Owakati")

# モデルの学習（サンプルのため、ダミーデータを使用）
sentences = ["勃起不全をバイアグラで解決する", "勃起不全 女性"]
sentences = [m.parse(sentence).split() for sentence in sentences]

model = Word2Vec(sentences, min_count=1)

# 単語間の類似度の計算
similarity = model.wv.similarity('勃起不全', 'バイアグラ')
print(similarity)