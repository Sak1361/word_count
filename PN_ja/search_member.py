import re,sys
from bs4 import BeautifulSoup

def search(search_n):
    re_sub = re.compile(r'[︰-＠]')  #全角記号
    re_space = re.compile(r'[　 +]')    #全半空白
    search_n = re_space.sub('',search_n)
    for page in range(1,100):
        try:
            html = open(r"/Users/sak1361/repository/scrape_diet-member/pages/diet-member_{}.html".format(page),'r')
        except FileNotFoundError:
            return 0
        soup = BeautifulSoup(html, "html.parser")
        for res in soup.find_all(class_="ContentsData"):
            name = res.find(class_="Name").text.replace('\u3000','')    #タブを削除
            name = re_sub.sub(' ',name) #カッコを取り除く
            name = name.split(' ')  #リスト化（名前、年齢、読み仮名）
            if name[0] == search_n or name[2] == search_n:
                party = res.find(class_="Party").text
                return party