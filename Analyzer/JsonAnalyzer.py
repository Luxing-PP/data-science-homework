##不要用这个东西，没整好
import json


def resolveJson(path):
    file = open(path, "rb")
    fileJson = json.load(file)
    province = fileJson["province"]
    content = fileJson["content"]
    time = fileJson["time"]

    return (content, time, province)


def output(path):
    result = resolveJson(path)
    print(result)
    for x in result:
        for y in x:
            print(y)


if __name__ == '__main__':
    print('1');
