import MeCab
import re
def main():
    m = MeCab.Tagger('-Owakati')    #分かち書き
    n = MeCab.Tagger('-Ochasen')    #形態素解析
    a = input("分かち書き：")
    wakati = m.parse(a).strip() #stripで文字除去、引数なしは空文字除去
    keitai = n.parse(a).strip()
    print(type(wakati),wakati)
    print(keitai)
#    for addlist in keitai:
#        addlist = re.split('[\t,]', addlist)  # 空白と","で分割
#        if addlist[0] == 'EOS' or addlist[0] == '' or addlist[0] == 'ー':
#            pass
#        print(addlist[0],end = "\n")
if __name__ == '__main__':
    i = 1
    while i > 0:
        main()
        i = int(input("onemore? 0 or 1:"))
