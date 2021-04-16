import json

def jsonreadprovince():
    with open("../data/keycom.json", "r", encoding='utf-8') as load_json:
        L_json = json.loads(load_json.read())
        list1 = []
        for j in L_json:
            list1.append(j['province'])
    return list1
def jsonreadtime():
    with open("../data/keycom.json", "r", encoding='utf-8') as load_json:
        L_json = json.loads(load_json.read())
        list1 = []
        for j in L_json:
            list1.append(j['time'])
    return list1
def jsonread():
    with open("../data/keycom.json", "r", encoding='utf-8') as load_json:
        # 读组件
        # 解析为 LIST 里面放着一堆字典
        L_json = json.loads(load_json.read())

        # 改组件 （你只要把这个改好的加到list里其实就能对上写组件的接口）
        change = L_json[0]
        change['newkey'] = "new Value"  # 因为python 处理成了 字典其实改json 等于改字典
    #    data = json.dumps(change, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)
    #    print(data)
    #   m = json.loads(data)
    #   for key in m:
    #       print("{}And{}".format(key, m[key]))

    #    listA = []
        listB=  []
        for j in L_json:
            data = json.dumps(j, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)
        #    listA.append(data)
        #    print(j['content'])
            listB.append(j['content'])
        return listB

def jsonwrite(listA):
    with open("../data/vCom.json", "a", encoding='utf-8') as output_json:
        # 写组件
        output = ",\n".join(listA)
        output_json.write("[\n")
        output_json.write(output)
        output_json.write("]")

#     你可以把前面那个读组件的文件改成这个output的，就可以测试有没有写对
if __name__ == '__main__':
    list=jsonreadtime()
    print(len(list))
    for item in list:
        print(item)