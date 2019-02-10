
def main():
    with open("immigra2.txt","r")as f2:
        immigra2 = ""
        c = 0
        for line in f2:
            if line.find('○') == 0:
                if c:
                    yield immigra2
                    immigra2 = ""
                c = 1
            immigra2 += line
        yield immigra2

if __name__ == "__main__":
    addline = ""
    sameline = ""
    with open("immigra.txt","r")as f:
        text = f.read()
    for line in main():
        if line in text:
            sameline += line + "\n"
        else:
            addline += line + "\n"
    text = text + addline
    with open("immigran.txt","w")as f:
        f.write(text)