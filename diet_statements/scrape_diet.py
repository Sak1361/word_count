import urllib, untangle, urllib.parse, os, sys, re

def scrape(path):
    start = '1'
    i = 0
    Reco = ""
    day = ""
    pattern = "(.*)　(.*)" 
    chairs = ["大島理森","赤松広隆","伊達忠一","郡司彰","山崎正昭","輿石東","川端達夫","金子原二郎","向大野新治","冨岡勉","石田昌宏","郷原悟"]    #議長リスト
    if os.path.exists(path):
        a = int(input("ファイルあるけど上書きする？:yes(0) or no(1)："))
        if a:
            print("しゅーりょー")
            sys.exit()
        else:
            with open(path,'w') as f:
                f.write("")
    while True:
        #keyword = '安倍晋三'
        startdate = '2018-01-01'
        enddate = '2018-12-31'
        maxreco = '100'
        #meeting = '本会議'
        search = '入管法 改正'
        url = 'http://kokkai.ndl.go.jp/api/1.0/speech?'+urllib.parse.quote('startRecord=' + start
                                                                           + '&maximumRecords=' + maxreco
                                                                           #+ '&speaker=' + keyword
                                                                           + '&any=' + search
                                                                           #+ '&nameOfMeeting=' + meeting
                                                                           + '&from=' + startdate
                                                                           + '&until=' + enddate)
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
                reco_line = speechreco.speech.cdata
                if reco_line.find('○') == 0:    #名前の置き換え
                    sep = re.search(pattern,reco_line)
                    name = '○' + name
                    reco_line = reco_line.replace(sep.group(1),name)
                Reco += reco_line
        Reco += '\n'

        if not i%500:   #500件超えるならここでカキコ
            with open(path, 'a') as f:
                f.write(Reco)
            Reco = ""
        try:    #最後にエラーで終わるからここでにゃーん
            start = obj.data.nextRecordPosition.cdata
        except AttributeError:
            print("おわり")
            break
        i += 100
        print("{0}件中{1}件目".format(art,i))
    return Reco
        
if __name__ == '__main__':
    path = sys.argv[1]
    r = scrape(path)
    # w =カキコ,r =読み,a =追加カキコ,w+ =全部消してカキコ,r+ =既に書かれている内容を上書き,a+ =既に書かれている内容に追記
    with open(path, 'a') as f: #残りをかきこ
        f.write(r)
