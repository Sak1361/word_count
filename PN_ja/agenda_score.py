import MeCab, re, codecs, sys, os, json, urllib.request
import matplotlib.pyplot as plt

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
                nameData = nameData.replace("君","")
                nameData = nameData.replace("○","")
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

def match_score():
    if os.path.exists("pn_ja.txt"):
        text = ""
        with open("pn_score.txt",'r') as f:
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
    with open("pn_score.txt","w") as f:
        text_dic = json.dumps(ja_dic,ensure_ascii=False, indent=2 )
        f.write(text_dic)
    return ja_dic

def counting(all_words):
    #print("総文字数:{0}".format(len(all_words)))
    ja_dict = match_score()  #Matchぱたーん
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

def plot(dicts,agrees,disagrees):
    res_dicts = {}
    for key, value in sorted(res_dict.items(), key=lambda x: x[1]): #スコアを昇順に
        res_dicts.update({key:value})
    dicts_value = list(res_dicts.values())  #valueが複数なのでリスト化
    score,hitsum,hitratio = [],[],[]
    i = 0
    while i < len(dicts_value):
        score.append(dicts_value[i][0])
        hitsum.append(dicts_value[i][1])
        hitratio.append(dicts_value[i][2])
        i += 1
    plt.figure(figsize=(15, 5)) #これでラベルがかぶらないくらい大きく
    plt.title('ネガポジ')
    for j,key in zip(range(len(dicts)),dicts.keys()):
        if key in disagrees:
            plt.bar(j,score[j], align='center',color='blue')
        elif key in agrees:
            plt.bar(j,score[j], align='center',color='red')
        else:
            plt.bar(j,score[j], align='center',color='green')
    plt.xticks(range(len(dicts)), list(dicts.keys()),rotation=90)
    plt.tick_params(width=2, length=10) #ラベル大きさ 
    plt.tight_layout()  #整える
    plt.show()

if __name__ == '__main__':
    input_f = sys.argv[1]
    out_f = sys.argv[2]
    res_dict = {}
    agrees,disagrees = [],[]
    c = 1
    for name,words in re_def(input_f):
        if "修正案に賛成" in words: #修正案に賛成＝＝現改正案に反対
            disagrees.append(name)
        elif "反対の" in words: #反対派
            disagrees.append(name)
        elif "賛成の" in words: #賛成派
            agrees.append(name)
        score, hits, nohit = counting(words)
        if name in res_dict.keys():
            val = (res_dict[name][0] + score) / 2
            score = (res_dict[name][2] + (hits/(hits + nohit))*100 ) / 2
            word = res_dict[name][1] + hits
            score =[ val , word , score ]   #valueには（スコア、ヒット数、ヒット率）
            res_dict.update({name:score})
        else:
            score = [score, hits ,(hits/(hits + nohit))*100]
            res_dict.update({name:score})
        if not c%10:
            print(c,"行終了")
        c += 1
    lines = ""
    for key, value in sorted(res_dict.items(), key=lambda x: x[1]): #スコアを昇順に
    #for key,value in res_dict.items():
        if value[1] < 100:
            del res_dict[key]
        else:
            lines += "{0}：{1}：ヒット数：{2}：ヒット率：{3}".format(key,round(value[0],4),value[1],round(value[2],2))
            lines += '\n'
    with open(out_f,'w')as f:
        f.write(lines)

    plot(res_dict,set(agrees),set(disagrees))   #plot