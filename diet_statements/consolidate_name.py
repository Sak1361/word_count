import re,sys

def main(m_path,name_path):
    with open(name_path,'r')as f:
        names = f.read().split('\n')
    i = 0
    l = ""
    pattern = "(.*)　(.*)"  #全角スペースで分ける
    with open(m_path,'r')as f:
        for line in f:
            if line.find('○',0,5) == 0:
                if i:
                    yield l
                    l = ""
                sep = re.search(pattern,line)
                nameData = '○' + names[i]
                line = line.replace(sep.group(1),nameData)
                i += 1
            l += line
        yield l

if __name__ == "__main__":
    minute_f = sys.argv[1]
    name_f = sys.argv[2]
    count = 0
    sentence = ""
    for line in main(minute_f,name_f):
        sentence += line + '\n'
    with open(minute_f,'w')as f:
        f.write(sentence)
    