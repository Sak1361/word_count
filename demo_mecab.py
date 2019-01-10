import MeCab

wakati = MeCab.Tagger('-Owakati')    #分かち書き
neo_wakati = MeCab.Tagger('-Owakati -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd') #追加辞書を適用
word = input("分かち書き：")

wakati = wakati.parse(word).strip()
neo_wakati = neo_wakati.parse(word).strip()

print('通常辞書：' + wakati)
print('追加辞書：' + neo_wakati)