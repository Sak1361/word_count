import MeCab
import re
import urllib.request
import chardet
import codecs
import time
import argparse
import os
import json
from bs4 import BeautifulSoup

def re_def(filepass):
    with codecs.open(filepass, 'r', encoding='utf-8', errors='ignore')as f:
        l = ""
        re_half = re.compile(r'[!-~]')  # 半角記号,数字,英字
        re_full = re.compile(r'[︰-＠]')  # 全角記号
        re_full2 = re.compile(r'[、。・’〜：＜＞＿｜「」｛｝【】『』〈〉“”○〇〔〕…――――─◇]')  # 全角で取り除けなかったやつ 
        re_url = re.compile(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-…]+')
        re_tag = re.compile(r"<[^>]*?>")    #HTMLタグ
        re_n = re.compile(r'\n')  # 改行文字
        re_space = re.compile(r'[\s+]')  #１以上の空白文字
        re_matchday = re.compile(r'^\d{4}-\d{1,2}-\d{1,2}$')
        pattern = "(.*)　(.*)"  #全角スペースで分ける
        start_time = time.time()
        for line in f:
            if '○' in line: #○からスペースまで名前なので取り除く
                sep = re.search(pattern,line)
                line = line.replace(sep.group(1),"")
            if not re_matchday.match(line):  #日付データを削除対象外に
                line = re_half.sub("", line)
            line = re_full.sub("", line)
            line = re_url.sub("", line)
            line = re_tag.sub("",line)
            line = re_n.sub("", line)
            line = re_space.sub("", line)
            line = re_full2.sub(" ", line)
            l += line + '\n'
    end_time = time.time() - start_time
    print("無駄処理時間",end_time)
    return l

def Match():
    if os.path.exists("pn_ja.txt"):
        text = ""
        with open("pn_ja.txt",'r') as f:
            for l in f:
                text += l
        ja_dic = json.loads(text,encoding='utf-8')
        return ja_dic
    ja_dic = {}
    url = 'http://www.lr.pi.titech.ac.jp/~takamura/pubs/pn_ja.dic'
    with urllib.request.urlopen(url) as res:
        html = res.readline().decode("shift_jis",'ignore').rstrip('\r\n')
        while html:
            sep = html.split(':')
            ja_dic.update([(str(sep[0]),float(sep[3]))])
            html = res.readline().decode("shift_jis",'ignore').rstrip('\r\n')
    ###毎回呼ぶの面倒だからファイル作る
    with open("pn_ja.txt","w") as f:
        text_dic = json.dumps(ja_dic,ensure_ascii=False, indent=2 )
        f.write(text_dic)
    return ja_dic

def date_sep(all_words):
    day = ""
    meeting = ""
    re_day = re.compile(r'^\d{4}-\d{1,2}-\d{1,2}$')
    all_words = re.split("[ \n]",all_words)
    for line in all_words:
        if not line:
            pass
        if re_day.match(day) and re_day.match(line) and day != line:
            yield day ,meeting
            meeting = ""
            day = line
        elif re_day.match(line):
            day = line
        else:
            meeting += line + '\n'
            
def counting(all_words):
    print("総文字数:{0}\t({1}万字)".format(len(all_words), len(all_words)/10000))
    ja_dict = Match()  #Matchぱたーん
    #tagger = MeCab.Tagger('-Owakati -d /usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd')
    tagger = MeCab.Tagger('-Owakati -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')

    #while True:
    for day,wakati in date_sep(all_words):
        setcount = 0
        notMatch = 0
        score = 0
        wakati = tagger.parse(wakati)#.split("\n")
        wakati = re.split('[ ,\n]', wakati)
        for Word in wakati:
            if Word in ja_dict.keys():
                score += float(ja_dict[Word])
                setcount += 1
            else:
                notMatch += 1
        yield day, score/(setcount + notMatch), setcount, notMatch

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i', type=str)
    parser.add_argument('--out', '-o' , type=str)
    args = parser.parse_args()
    
    words = re_def(args.input)
    stime = time.time()
    for day , score , hitword , nohit in counting(words):
        hits = (hitword/(hitword+nohit) )*100
        print(day , round(score,4) ,hitword ,nohit ,"{0}%".format(round(hits,2)))
    etime = time.time() - stime
    print("処理時間:",etime)