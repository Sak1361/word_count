import re,sys,MeCab,jaconv
from bs4 import BeautifulSoup

def search_party(search_name):
    tagger = MeCab.Tagger('-Oyomi -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')#読み仮名のみ
    tagger.parse('')
    re_sub = re.compile(r'[︰-＠]')  #全角記号
    re_space = re.compile(r'[　 +]')    #全半空白
    search_name = re_space.sub('',search_name)
    read_name = tagger.parse(search_name)
    read_name = jaconv.kata2hira(str(read_name)).strip('\n')    #改行が混じるからとる
    for page in range(1,100):
        try:
            html = open(r"/Users/sak1361/repository/scrape_diet-member/pages/diet-member_{}.html"\
                .format(page),'r')  #完全パスの方が良い
        except FileNotFoundError:
            return 0
        soup = BeautifulSoup(html, "html.parser")
        for res in soup.find_all(class_="ContentsData"):
            name = res.find(class_="Name").text.replace('\u3000','')    #タブを削除
            name = re_sub.sub(' ',name) #カッコを取り除く
            name = name.split(' ')  #リスト化（名前、年齢、読み仮名）
            if name[0] == search_name or name[2] == search_name or read_name == name[2]:
                party = res.find(class_="Party").text
                return party
if __name__ == "__main__":
    name = sys.argv[1]
    print(search_party(name))