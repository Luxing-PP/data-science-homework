import csv
import databaseHelper

if __name__ == '__main__':
    database = databaseHelper.database()
    database.initialize()
    with open("../data/supplementTag.csv", "r", encoding='utf-8')as csvFile:
        res = csv.reader(csvFile, delimiter=',', quotechar='\"')
        for row in res:
            database.insert_eLexicon(row)
    database.close()
