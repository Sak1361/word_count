import MeCab, re, codecs, sys, os, json, urllib.request
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup

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
        yield nameData,l

def match_wago():
    if os.path.exists("pn_wago.csv"):
        with open("pn_wago.csv",'r') as f:
            wago = f.read().split('\n')
        return wago
    ###用語###
    pn_path1 = 'http://www.cl.ecei.tohoku.ac.jp/resources/sent_lex/wago.121808.pn'
    pn_file1 = urllib.request.urlopen(pn_path1)
    wago = BeautifulSoup(pn_file1,'html.parser')
    wago = str(wago).split('\n')
    nega_word , posi_word = '',''
    extra = [" だ"," です"," と"," の"] #余分と思うから除く
    for wago_list in wago:
        wago_list = wago_list.split('\t')
        if "ネガ" in wago_list[0] and wago_list[1]:
            for ex in extra:
                wago_list[1] = wago_list[1].replace(ex,"")
            if not 'n\t'+wago_list[1] in nega_word:
                nega_word += 'n\t' + wago_list[1] + '\n'
        elif "ポジ" in wago_list[0] and wago_list[1]:
            for ex in extra:
                wago_list[1] = wago_list[1].replace(ex,"")
            if not 'p\t'+wago_list[1] in posi_word:
                posi_word += 'p\t' + wago_list[1] + '\n'
    wago = posi_word + nega_word
    #毎回呼ぶの面倒だからファイル作る
    with open("pn_wago.csv","w") as f:
        f.write(wago)
    wago = wago.split('\n')
    return wago
    
def match_noun():
    if os.path.exists("pn_noun.csv"):
        with open("pn_noun.csv",'r') as f:
            pn_noun = f.read().split('\n')
        return pn_noun
    tagger = MeCab.Tagger('-Owakati -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')
    ###名詞###
    pn_path = 'http://www.cl.ecei.tohoku.ac.jp/resources/sent_lex/pn.csv.m3.120408.trim'
    pn_file = urllib.request.urlopen(pn_path)
    pn_noun = BeautifulSoup(pn_file,'html.parser')
    pn_noun = str(pn_noun).split('\n')
    posi_noun,nega_noun,even_noun = '','',''
    for noun_list in pn_noun:
        noun_list = noun_list.split('\t')
        noun_list[0] = tagger.parse(noun_list[0])   #分かち書きする
        noun_list[0] = noun_list[0][:-2]    #空白の削除
        if noun_list[0] == '\n' or noun_list[0] in '"':
            pass
        elif noun_list[1] and noun_list[1] == 'p':
            posi_noun += 'p\t' + noun_list[0] + '\n'
        elif noun_list[1] and noun_list[1] == 'n':
            nega_noun += 'n\t' + noun_list[0] + '\n'
        elif noun_list[1] and noun_list[1] == 'e':
            even_noun += 'e\t' + noun_list[0] + '\n'
        elif noun_list[1] and noun_list[1] == '?p?n':   #?が混じってるのでeに入れてあげる
            even_noun += 'e\t' + noun_list[0] + '\n'
    pn_noun = posi_noun + nega_noun + even_noun
    #毎回呼ぶの面倒だからファイル作る
    with open("pn_noun.csv","w") as f:
        f.write(pn_noun)
    pn_noun = pn_noun.split('\n')
    return pn_noun

def matching(all_words):
    #print("総文字数:{0}".format(len(all_words)))
    tagger = MeCab.Tagger('-Owakati -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')
    pn_wago = match_wago()  #Matchぱたーん
    pn_noun = match_noun()
    meetings = "" 
    p_match, n_match, e_match, sum_words = 0,0,0,0
    match_words = pn_wago + pn_noun
    all_words = re.split("[ \n]",all_words)
    for line in all_words:
        meetings += line + '\n'
    wakati = tagger.parse(meetings)#.split("\n")
    wakati = re.split('[ ,\n]', wakati)
    wakati = iter(wakati) #イテレータに
    while True:
        try:
            word = next(wakati)
            sum_words += 1
        except StopIteration:
            break
        for pn in match_words:
            pn = pn.split('\t')
            if pn[0] == '':
                pass
            elif ' ' in pn[1]:    #空白の有無
                pn[1] = pn[1].split(' ')
                num = 0
                while True:
                    if pn[1][num] == word:
                        if len(pn[1]) == num+1:
                            if pn[0] == 'p':
                                p_match += 1
                            elif pn[0] == 'n':
                                n_match += 1
                            elif pn[0] == 'e':
                                e_match += 1
                            break
                        else:
                            word = next(wakati)
                            sum_words += 1
                            num += 1
                    else:
                        break
            else:
                if pn[1] == word:
                    if pn[0] == 'p':
                        p_match += 1
                    elif pn[0] == 'n':
                        n_match += 1
                    elif pn[0] == 'e':
                        e_match += 1
    return p_match,n_match,e_match,sum_words

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
        p_match, n_match, e_match, sum_words = matching(words)
        hits = p_match + n_match + e_match
        score = (p_match+e_match) - (n_match+e_match)
        if name in res_dict.keys():
            val = res_dict[name][0] + score
            matchs = res_dict[name][1] + hits
            #hit_p = ( res_dict[name][2] + (hits/sum_words)*100) ) /2
            hit_p = res_dict[name][2] + sum_words
            score =[ val , matchs , hit_p ]   #（スコア、ヒット数、ヒット率）
            res_dict.update({name:score})
        else:
            score = [score, hits , sum_words ]
            res_dict.update({name:score})
        if not c%10:
            print(c,"行終了")
        c += 1
    lines = ""
    for key, value in sorted(res_dict.items(), key=lambda x: x[1]): #スコアを昇順に
        if value[1] < 100:
            del res_dict[key]
        else:
            lines += "{0}：{1}：ヒット数：{2}：総数：{3}".format(key,value[0],value[1],round(value[2],2))
            lines += '\n'
    with open(out_f,'w')as f:
        f.write(lines)

    plot(res_dict,set(agrees),set(disagrees))   #plot