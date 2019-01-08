import MeCab
import re
import urllib.request
import codecs
import sys
import os
import json

def re_def(filepass):
    nameData = ""
    with codecs.open(filepass, 'r', encoding='utf-8', errors='ignore')as f:
        l = ""
        re_half = re.compile(r'[!-~]')  # 半角記号,数字,英字
        re_full = re.compile(r'[︰-＠]')  # 全角記号
        re_full2 = re.compile(r'[、。・’〜：＜＞＿｜「」｛｝【】『』〈〉“”○〇〔〕…――――─◇]')  # 全角で取り除けなかったやつ 
        re_url = re.compile(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-…]+')
        re_tag = re.compile(r"<[^>]*?>")    #HTMLタグ
        re_n = re.compile(r'\n')  # 改行文字
        re_space = re.compile(r'[\s+]')  #１以上の空白文字
        pattern = "(.*)　(.*)"  #全角スペースで分ける
        i = 0
        for line in f:
            #if '○' in line:
            if line.find('○',0,10) == 0:
                if i:
                    yield nameData,l
                    l = ""
                sep = re.search(pattern,line)
                nameData = sep.group(1)
                if not nameData:
                    print(line)
                nameData = nameData.replace("君","")
                line = line.replace(sep.group(1),"")
                i = 1
            line = re_half.sub("", line)
            line = re_full.sub("", line)
            line = re_url.sub("", line)
            line = re_tag.sub("",line)
            line = re_n.sub("", line)
            line = re_space.sub("", line)
            line = re_full2.sub(" ", line)
            l += line


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
            
def counting(all_words):
    #print("総文字数:{0}".format(len(all_words)))
    ja_dict = Match()  #Matchぱたーん
    tagger = MeCab.Tagger('-Owakati -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')
    meetings = "" 
    setcount = 0
    notMatch = 0
    score = 0
    all_words = re.split("[ \n]",all_words)
    for line in all_words:
        meetings += line + '\n'

    wakati = tagger.parse(meetings)#.split("\n")
    wakati = re.split('[ ,\n]', wakati)
    for Word in wakati:
        if Word in ja_dict.keys():
            score += float(ja_dict[Word])
            setcount += 1
        else:
            notMatch += 1
    return score/(setcount+notMatch), setcount, notMatch

if __name__ == '__main__':
    input_f = sys.argv[1]
    out_f = sys.argv[2]
    res_dict = {}
    for name,words in re_def(input_f):
        score, hits, nohit = counting(words)
        if name in res_dict.keys():
            val = (res_dict[name][0] + score) / 2
            score = (res_dict[name][2] + (hits/(hits + nohit)*100) ) / 2
            word = res_dict[name][1] + hits + nohit
            score =[ val , word , score ]
            res_dict.update({name:score})
        else:
            score = [score, hits+nohit ,hits/(hits + nohit)*100]
            res_dict.update({name:score})
    lines = ""
    for key, value in sorted(res_dict.items(), key=lambda x: x[1]): #スコアを昇順に
    #for key,value in res_dict.items():
        lines += "{0}：{1}：ヒット数：{2}：ヒット率：{3}".format(key,round(value[0],4),value[1],round(value[2],2))
        lines += '\n'
    with open(out_f,'w')as f:
        f.write(lines)
        
    #print("score平均：{0}、ヒット数：{1}、ヒット率：{2}％".format( round(score,4) ,hits ,round( hits/(hits + nohit)*100,4)))