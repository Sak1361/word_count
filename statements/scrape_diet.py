import urllib
import untangle
import urllib.parse
from bs4 import BeautifulSoup
import os
import sys

def scrape(path):
    start = '1'
    i = 0
    Reco = ""
    day = ""
    chairs = ["大島理森","赤松広隆","伊達忠一","郡司彰","山崎正昭","輿石東","川端達夫","金子原二郎","向大野新治","冨岡勉","石田昌宏"]    #議長リスト
    if os.path.exists(path):
        a = int(input("ファイルあるけど上書きする？:yes(0) or no(1)："))
        if a:
            print("しゅーりょー")
            sys.exit()
        else:
            with open(path,'w') as f:
                f.write("")
    while True:
        #keyword = '麻生太郎'
        startdate = '2009-01-01'
        #enddate = '1998-12-31'
        maxreco = '100'
        #meeting = '本会議'
        search = '公職選挙法の改正'
        #search = '解任決議 反対の立場から'
        #urllib.parse.quoteが日本語をコーディングしてくれる
        url = 'http://kokkai.ndl.go.jp/api/1.0/speech?'+urllib.parse.quote('startRecord=' + start
                                                                           + '&maximumRecords=' + maxreco
                                                                           #+ '&speaker=' + keyword
                                                                           + '&any=' + search
                                                                           #+ '&nameOfMeeting=' + meeting)
                                                                           + '&from=' + startdate)
                                                                           #+ '&until=' + enddate)
        obj = untangle.parse(url)
        art = obj.data.numberOfRecords.cdata
        for record in obj.data.records.record:
            name = record.recordData.speechRecord.speaker.cdata
            if name == '' or name in chairs:    #発言者なしor議長の場合はパス
                pass
            else:
                speechreco = record.recordData.speechRecord
                if not day == speechreco.date.cdata:
                    Reco += speechreco.date.cdata + "\n"            
                day = speechreco.date.cdata
                Reco += speechreco.speech.cdata
        Reco += '\n'

        if not i%300:   #300件超えるならここでカキコ
            with open(path, 'a') as f:
                f.write(Reco)
            Reco = ""
        try:    #最後にエラーで終わるからここでにゃーん
            start = obj.data.nextRecordPosition.cdata
        except AttributeError:
            print("にゃーんえらー")
            break
        i += 100
        if i > int(art):
            print("件数到達")
            break
        print("{0}件中{1}件目".format(art,i))
    return Reco
        
if __name__ == '__main__':
    path = sys.argv[1]
    r = scrape(path)
    # w =カキコ,r =読み,a =追加カキコ,w+ =全部消してカキコ,r+ =既に書かれている内容を上書き,a+ =既に書かれている内容に追記
    with open(path, 'a') as f: #残りをかきこ
        f.write(r)