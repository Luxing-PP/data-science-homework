def blabla():
    weightslist=[]
    with open("../newelexicon", 'r', encoding='utf-8')as weights:
        for item in weights:
            item=item.replace('[','')
            item=item.replace(']','')
            item=item.rstrip()
            weightslist.append(float(item.split(',')[2]))
        weights.close()
    for item in weightslist:
        print(item)
if __name__ == '__main__':
    blabla()