import re ,sys
import matplotlib.pyplot as plt
import numpy as np

def compare(score_f,pn_f):
    name = []
    score_l = []
    pn_l = []
    for score in score_f:
        score = score.split('：')
        if score[0] == '':
            pass
        elif int(score[7]) > 400:
            for pn in pn_f:
                pn = pn.split('：')
                if pn[0] == '' or int(pn[7]) < 400:
                    pass
                elif pn[0] == score[0]:
                    name.append(score[0])
                    score_l.append(score[1])
                    pn_l.append(pn[1])
                    break
    return name, score_l, pn_l

def plot(name,score_l,pn_l):
    plt.figure(figsize=(15, 5)) #これでラベルがかぶらないくらい大きく
    plt.title('比較')
    leng = np.arange(len(name))   #intで使いたいからnumpyの連番に
    #leng = range(len(score_dict))
    plt.xticks(leng, name,rotation=90)
    plt.tick_params(width=2, length=5) #ラベル大きさ 
    _, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    ax1.bar(leng-0.2,score_l,color='Cyan',width=0.5)
        #plt.bar(ln+3,value[1], align='center',color='Yellow')
    ax2.bar(leng+0.2,pn_l, color='blue',width=0.5)
    plt.tight_layout()  #整える
    plt.show()

if __name__ == "__main__":
    file1 = sys.argv[1]
    file2 = sys.argv[2]
    with open(file1,'r')as f1,open(file2,'r')as f2:
        f_file = f1.read().split('\n')
        s_file = f2.read().split('\n')
    n,s,p = compare(f_file,s_file)
    plot(n,s,p)