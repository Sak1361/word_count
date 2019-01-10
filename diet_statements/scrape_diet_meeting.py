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
    chairs = ["大島理森","赤松広隆","伊達忠一","郡司彰","山崎正昭","輿石東","川端達夫"]    #議長リスト
    if os.path.exists(path):
        a = int(input("ファイルあるけど上書きする？:yes(0) or no(1)："))
        if a:
            print("しゅーりょー")
            sys.exit()
        else:
            with open(path,'w') as f:
                f.write("")
    while True:
        keyword = '麻生太郎'
        startdate = '2018-01-01'
        #enddate = '2018-12-31'
        maxreco = '5'
        meeting = '本会議 予算委員会'
        #urllib.parse.quoteが日本語をコーディングしてくれる
        url = 'http://kokkai.ndl.go.jp/api/1.0/meeting?'+urllib.parse.quote('startRecord=' + start
                                                                           + '&maximumRecords=' + maxreco
                                                                           + '&speaker=' + keyword
                                                                           + '&nameOfMeeting=' + meeting
                                                                           + '&from=' + startdate)
                                                                           #+ '&until=' + enddate)
        obj = untangle.parse(url)
        art = obj.data.numberOfRecords.cdata
        for record in obj.data.records.record:
            name = record.recordData.meetingRecord.speechRecord.speaker.cdata
            if name == '' or name in chairs:    #発言者なしor議長の場合はパス
                pass
            else:
                speechreco = record.recordData.meetingRecord.speechRecord
                if not day == speechreco.date.cdata:
                    Reco += speechreco.date.cdata + "\n"        
                day = speechreco.date.cdata
                Reco += speechreco.speech.cdata
        Reco += '\n'

        with open(path, 'a+') as f:
            f.write(Reco)
        Reco = ""
        try:    #最後にエラーで終わるからここでにゃーん
            start = obj.data.nextRecordPosition.cdata
        except AttributeError:
            print("にゃーんえらー")
            break
        i += 5
        if i > int(art):
            print("件数到達")
            break
        print("{0}件中{1}件目".format(art,i))
    return Reco
        
if __name__ == '__main__':
    path = "demo.csv"
    r = scrape(path)
    # w =カキコ,r =読み,a =追加カキコ,w+ =全部消してカキコ,r+ =既に書かれている内容を上書き,a+ =既に書かれている内容に追記