# IPython log file

def res_load(res_file):
    score = []
    with open(res_file,'r')as f:
        res = f.read().split('\n')
    for mem_list in res:
        mem_list = mem_list.split('：')
        try:
            score.append(int(mem_list[8]))
        except IndexError:
            pass
    return score
    
row = res_load("res_fish.txt")
row
for i in range(len(row)):   #バブルソート
    for j in range(len(row)-1, i, -1):
        if row[j] < row[j-1]:
            row[j], row[j-1] = row[j-1], row[j]
        
row
len(row)
row[25]
row[26]
def res_load(res_file):
    row = []
    with open(res_file,'r')as f:
        res = f.read().split('\n')
    for mem_list in res:
        mem_list = mem_list.split('：')
        try:
            row.append(int(mem_list[8]))
        except IndexError:
            pass    
    for i in range(len(row)):   #バブルソート
        for j in range(len(row)-1, i, -1):
            if row[j] < row[j-1]:
                row[j], row[j-1] = row[j-1], row[j]
               
    
def res_load(res_file):
    row = []
    with open(res_file,'r')as f:
        res = f.read().split('\n')
    for mem_list in res:
        mem_list = mem_list.split('：')
        try:
            row.append(int(mem_list[8]))
        except IndexError:
            pass    
    for i in range(len(row)):   #バブルソート
        for j in range(len(row)-1, i, -1):
            if row[j] < row[j-1]:
                row[j], row[j-1] = row[j-1], row[j]
               
    l = len(row)/2
    return row , l
    
res_load("res_fish.txt")
def res_load(res_file):
    row = []
    with open(res_file,'r')as f:
        res = f.read().split('\n')
    for mem_list in res:
        mem_list = mem_list.split('：')
        try:
            row.append(int(mem_list[8]))
        except IndexError:
            pass    
    for i in range(len(row)):   #バブルソート
        for j in range(len(row)-1, i, -1):
            if row[j] < row[j-1]:
                row[j], row[j-1] = row[j-1], row[j]
               
    l = len(row)/2
    if type(l) == float:
        l = (row[l-0.5] + row[l+0.5])/2
    else:
        l = row[l]
    return l
    
    
res_load("res_fish.txt")
def res_load(res_file):
    row = []
    with open(res_file,'r')as f:
        res = f.read().split('\n')
    for mem_list in res:
        mem_list = mem_list.split('：')
        try:
            row.append(int(mem_list[8]))
        except IndexError:
            pass    
    for i in range(len(row)):   #バブルソート
        for j in range(len(row)-1, i, -1):
            if row[j] < row[j-1]:
                row[j], row[j-1] = row[j-1], row[j]
               
    l = len(row)/2
    if type(l) == "float":
        l = (row[l-0.5] + row[l+0.5])/2
    else:
        l = row[l]
    return l
    
    
res_load("res_fish.txt")
def res_load(res_file):
    row = []
    with open(res_file,'r')as f:
        res = f.read().split('\n')
    for mem_list in res:
        mem_list = mem_list.split('：')
        try:
            row.append(int(mem_list[8]))
        except IndexError:
            pass    
    for i in range(len(row)):   #バブルソート
        for j in range(len(row)-1, i, -1):
            if row[j] < row[j-1]:
                row[j], row[j-1] = row[j-1], row[j]
               
    l = len(row)/2
    if type(l) == float:
        l = (row[int(l-0.5)] + row[int(l+0.5)])/2
    else:
        l = row[l]
    return l
    
    
res_load("res_fish.txt")
res_load("res_water.txt")
res_load("res_immigrant.txt")
def res_load(res_file):
    row = []
    with open(res_file,'r')as f:
        res = f.read().split('\n')
    for mem_list in res:
        mem_list = mem_list.split('：')
        try:
            row.append(int(mem_list[8]))
        except IndexError:
            pass    
    for i in range(len(row)):   #バブルソート
        for j in range(len(row)-1, i, -1):
            if row[j] < row[j-1]:
                row[j], row[j-1] = row[j-1], row[j]
               
    l = len(row)/2
    if type(l) == float:
        l = (row[int(l-0.5)] + row[int(l+0.5)])/2
    else:
        l = row[l]
    return l,len(row)
    
res_load("res_immigrant.txt")
res_load("res_fish.txt")
res_load("res_water.txt")
log
get_ipython().system('log')
get_ipython().run_line_magic('log', '')
get_ipython().run_line_magic('logstart', '')
def res_load(res_file):
    row = []
    with open(res_file,'r')as f:
        res = f.read().split('\n')
    for mem_list in res:
        mem_list = mem_list.split('：')
        try:
            row.append(int(mem_list[8]))
        except IndexError:
            pass    
    for i in range(len(row)):   #バブルソート
        for j in range(len(row)-1, i, -1):
            if row[j] < row[j-1]:
                row[j], row[j-1] = row[j-1], row[j]
               
    l = len(row)/2
    if type(l) == float:
        l = (row[int(l-0.5)] + row[int(l+0.5)])/2
    else:
        l = row[l]
    return l,len(row)
    
get_ipython().run_line_magic('logstop', '')
