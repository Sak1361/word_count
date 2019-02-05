import MeCab, re, codecs, sys, os, json, urllib.request, mojimoji
import matplotlib.pyplot as plt
import search_party

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
        re_num = re.compile(r"[0-9]")
        pattern = "(.*)　(.*)"  #全角スペースで分ける
        i = 0
        for line in f:
            if re_num.match(line):  #半角数字は全角数字にする
                line = mojimoji.han_to_zen(line, ascii=False)
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
        yield nameData,l

def match_score():
    if os.path.exists("pn_score.txt"):
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
            key = str(sep[0])
            nextkey = str(sep[1])
            value = float(sep[3])
            ja_dic.update([(key,value)])
            if key != nextkey and nextkey not in ja_dic:
                ja_dic.update([(nextkey,value)])
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
    tagger.parse('')
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
    for key, value in sorted(dicts.items(), key=lambda x: x[1]): #スコアを昇順に
        if value[3] > 200:
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
    leng = range(len(res_dicts))
    for j,key in zip(leng,res_dicts.keys()):
        if key in disagrees:
            plt.bar(j,score[j], align='center',color='blue')
        elif key in agrees:
            plt.bar(j,score[j], align='center',color='red')
        else:
            plt.bar(j,score[j], align='center',color='green')
    plt.xticks(leng, list(res_dicts.keys()),rotation=90)
    plt.tick_params(width=2, length=10) #ラベル大きさ 
    plt.tight_layout()  #整える
    plt.show()

def res_load(res_file):
    score = dict()
    ruling = []
    opposition = []
    with open(res_file,'r')as f:
        res = f.read().split('\n')
    for mem_list in res:
        mem_list = mem_list.split('：')
        if mem_list[0] == '':
            break
        if int(mem_list[7]) < 200:
            pass
        else:
            score.update({str(mem_list[0]):float(mem_list[1])})
    for key in score.keys():
        party = search_party.search(key)
        if party == '自民' or party == '公明' or party == '維新':
            ruling.append(key)  #appendじゃないと一文字づつ
        elif party == '無属':
            pass
        else:
            opposition.append(key)
    #plot
    res_dicts = {}
    for key, value in sorted(score.items(), key=lambda x: x[1]): #スコアを昇順に
            res_dicts.update({key:value})
    plt.figure(figsize=(15, 5)) #これでラベルがかぶらないくらい大きく
    plt.title('ネガポジ')
    leng = range(len(res_dicts))
    for ln,key,value in zip(leng,res_dicts.keys(),res_dicts.values()):
        if key in ruling:
            plt.bar(ln,value, align='center',color='blue')
        elif key in opposition:
            plt.bar(ln,value, align='center',color='red')
        else:
            plt.bar(ln,value, align='center',color='green')
    plt.xticks(leng, list(res_dicts.keys()),rotation=90)
    plt.tick_params(width=2, length=10) #ラベル大きさ 
    plt.tight_layout()  #整える
    plt.show()

if __name__ == '__main__':
    input_f = sys.argv[1]
    try:
        out_f = sys.argv[2]
    except IndexError:
        res_load(input_f)
        sys.exit()

    res_dict = {}
    agrees,disagrees = [],[]
    c = 1
    for name,words in re_def(input_f):
        if "修正案に賛成" in words: #修正案に賛成＝＝現改正案に反対
            disagrees.append(name)
        elif "反対の立場から" in words or "反対討論" in words: #反対派
            if not ("賛成の立場から" in words and "賛成討論" in words):
                disagrees.append(name)
            else:
                agrees.append(name)
        elif "賛成の立場から" in words or "賛成討論" in words: #賛成派
            if not ("反対の立場から" in words and "反対討論" in words):
                agrees.append(name)
        score, hits, nohit = counting(words)
        if name in res_dict.keys():
            val = (res_dict[name][0] + score) / 2
            hit_p = (res_dict[name][2] + (hits/(hits + nohit))*100 ) / 2
            word = res_dict[name][1] + hits
            all_words = res_dict[name][3] + hits + nohit
            score =[ val , word , hit_p , all_words]   #valueには（スコア、ヒット数、ヒット率、単語総数）
            res_dict.update({name:score})
        else:
            score = [score, hits ,(hits/(hits + nohit))*100,hits+nohit]
            res_dict.update({name:score})
        if not c%10:
            print(c,"行終了")
        c += 1
    lines = ""
    for key, value in sorted(res_dict.items(), key=lambda x: x[1]): #スコアを昇順に
        lines += "{0}：{1}：ヒット数：{2}：ヒット率：{3}：単語総数：{4}".format(key,round(value[0],4),value[1],round(value[2],2),value[3])
        lines += '\n'
    with open(out_f,'w')as f:
        f.write(lines)

    plot(res_dict,set(agrees),set(disagrees))   #plot