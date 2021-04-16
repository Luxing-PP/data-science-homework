
def makeDate(year, month, day):

    str_year = str(year)+""
    if len(str(month)) == 2:
        str_month = str(month)+""
    else:
        str_month = "0"+str(month)
    if len(str(day)) == 2:
        str_day = str(day)+""
    else:
        str_day = "0"+str(day)
    return str_year+"-"+str_month+"-"+str_day


def utf8Filter(strList):
    strList = list(map(lambda x: x.encode('utf-8', 'ignore').decode("utf-8"), strList))
    return strList
