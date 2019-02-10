import MeCab, re, codecs, sys, os, json, urllib.request, mojimoji,jaconv
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup

def re_def(filepass):
    nameData = ""
    with codecs.open(filepass, 'r', encoding='utf-8', errors='ignore')as f:
        l = ""
        re_half = re.compile(r'[!-~]')  # 半角記号,数字,英字
        re_full = re.compile(r'[︰-＠]')  # 全角記号
        re_full2 = re.compile(r'[、。・’〜：＜＞＿｜「」｛｝【】『』〈〉“”○〇〔〕…――――─◇]')  #全角個別指定 
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
        pn_score = ""
        with open("pn_score.txt",'r') as f:
            for l in f:
                pn_score += l
        return pn_score
    pn_score = ''
    url = 'http://www.lr.pi.titech.ac.jp/~takamura/pubs/pn_ja.dic'
    with urllib.request.urlopen(url) as res:
        html = res.readline().decode("shift_jis",'ignore').rstrip('\r\n')
        while html:
            pn_score += html + '\n'
            html = res.readline().decode("shift_jis",'ignore').rstrip('\r\n')
    ###毎回呼ぶの面倒だからファイル作る
    with open("pn_score.txt","w") as f:
        f.write(pn_score)
    return pn_score

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

def counting(all_words):
    tagger = MeCab.Tagger('-Ochasen -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')
    tagger.parse('')
    meetings = ""
    matchs = 0
    score = 0
    all_words = re.split("[ \n]",all_words)
    for line in all_words:
        meetings += line + '\n'
    noun_words = []   #名詞
    verb_words = []   #動詞
    adjective_words = []  #形容詞
    adverb_words = [] #副詞
    count = 0
    ja_dict = match_score().split('\n')  #Matchpattern
    for w in ja_dict:   #品詞別に分ける
        w = w.split(':')
        if w[0] == '':
            break
        if w[2] == '動詞':
            verb_words.append(ja_dict[count])
        elif w[2] == '形容詞':
            adjective_words.append(ja_dict[count])
        elif w[2] == '副詞':
            adverb_words.append(ja_dict[count])
        else:
            noun_words.append(ja_dict[count])
        count += 1
    wakati = tagger.parse(meetings)
    wakati = re.split('[ ,\n]', wakati)
    for word in wakati:
        word = word.split('\t') #済み,スミ,済む,動詞-自立,五段・マ行,連用形
        try:    #長いワードだと例外が出る
            word[1] = jaconv.kata2hira(str(word[1]))    #カナなのでひらがなに直す
            word[3] = word[3].split('-')    #動詞-自立で、自立は必要ないから省く
            word[3] = word[3][0]
            if word[3] == '名詞':
                for noun in noun_words:
                    noun = noun.split(':')  #優れる:すぐれる:動詞:1
                    if word[0] == noun[0] and word[1] == noun[1]:
                        score += float( noun[3] )
                        matchs += 1
                        break
            elif word[3] == '動詞':
                for verb in verb_words:
                    verb = verb.split(':')
                    if word[0] == verb[0] and word[1] == verb[1]:
                        score += float( verb[3] )
                        matchs += 1
                        break
            elif word[3] == '形容詞':
                for adj in adjective_words:
                    adj = adj.split(':')
                    if word[0] == adj[0] and word[1] == adj[1]:
                        score += float( adj[3] )
                        matchs += 1
                        break
            elif word[3] == '副詞':
                for adverb in adverb_words:
                    adverb = adverb.split(':')
                    if word[0] == adverb[0] and word[1] == adverb[1]:
                        score += float( adverb[3] )
                        matchs += 1
                        break
        except IndexError:
            if not word == 'EOS' or not word == '':  #空でもEOSでもない場合print
                print(word)
    return score/len(wakati), matchs,len(wakati) 

def plot(res):
    name = []
    plt.figure(figsize=(15, 5)) #これでラベルがかぶらないくらい大きく
    plt.title('ネガポジ')
    leng = range(len(res))
    for ln,key,value in zip(leng,list(res.keys()),res.values()):
        name.append(key[1])
        if key[0] == '自民' or key[0] == '公明' or key[0] == '維新':
            plt.bar(ln,value, align='center',color='red',label="与党+維新")
        elif key[0] == '民間':
            plt.bar(ln,value, align='center',color='gray',label="参考人等")
        elif key[0] == '無属':
            plt.bar(ln,value, align='center',color='green',label="無所属")
        else:
            plt.bar(ln,value, align='center',color='blue',label="野党")
    plt.xticks(leng, name ,rotation=90)
    plt.tick_params(width=2, length=10) #ラベル大きさ 
    plt.ylim([0,-0.2])
    plt.tight_layout()  #整える
    handles, labels = plt.gca().get_legend_handles_labels() #汎用表示
    i =1
    while i<len(labels):
        if labels[i] in labels[:i]:
            del(labels[i])
            del(handles[i])
        else:
            i +=1
    plt.legend(handles, labels)
    plt.show()

def res_load(res_file):
    score = dict()
    with open(res_file,'r')as f:
        res = f.read().split('\n')
    for mem_list in res:
        mem_list = mem_list.split('：')
        try:
            if int(mem_list[8]) > 500:
                party = str(mem_list[0])
                name = str(mem_list[1])
                value = float(mem_list[2])
                score.update({(party,name):value})
        except IndexError:
            pass
    return score

def corrects(res):
    row = []
    swap = 0
    for key in list(res.keys()):
        if key[0] == '民間' or key[0] == '無属':
            pass
        elif key[0] == '自民' or key[0] == '公明' or key[0] == '維新':
            row.append(1)
        else:
            row.append(0)
    for i in range(len(row)):   #バブルソート
        for j in range(len(row)-1, i, -1):
            if row[j] < row[j-1]:
                row[j], row[j-1] = row[j-1], row[j]
                swap += 1
    validity = len(res) / (len(res) + swap) #スワップした回数を分母に足して確率を求める
    return round(validity*100,2)

if __name__ == '__main__':
    input_f = sys.argv[1]
    try:
        out_f = sys.argv[2]
    except IndexError:
        files = res_load(input_f)
        cor = corrects(files)
        print("正答率：",cor)
        plot(files)
        sys.exit()
    if os.path.exists(out_f):   #上書きの警告
        select = input("orverwrite?yes(0),no(1):")
        if not select=='0':
            sys.exit()
    res_dict = {}
    c = 1
    for name,words in re_def(input_f):
        score, hits, all_word = counting(words)
        if name in res_dict.keys():
            val = (res_dict[name][0] + score) / 2
            hit_p = (res_dict[name][2] + (hits/all_word)*100 ) / 2
            word = res_dict[name][1] + hits
            all_w = res_dict[name][3] + all_word
            score =[ val , word , hit_p , all_w]   #valueには（スコア、ヒット数、ヒット率、単語総数）
            res_dict.update({name:score})
        else:
            score = [score, hits ,(hits/all_word)*100,all_word]
            res_dict.update({name:score})
        #if not c%10:
        print(c,"件終了")
        c += 1
    reslut = {}
    lines = ''
    for key, value in sorted(res_dict.items(), key=lambda x: x[1]): #スコアを昇順+所属政党追加
        party = search_party(key)
        if party == 0:
            party = '民間'
        key = (party,key)
        if value[3] > 500:  #総単語数が200以下はplotしない
            reslut.update({key:value[0]})
        lines += "{}：{}：{}：ヒット数：{}：ヒット率：{}：単語総数：{}"\
            .format(key[0],key[1],round(value[0],4),value[1],round(value[2],2),value[3])
        lines += '\n'
    cor = corrects(reslut)
    lines += "正答率：{}%".format(cor)
    with open(out_f,'w')as f:
        f.write(lines)
    plot(reslut)   #plot