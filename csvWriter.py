import csv

def writeCSV(datalist, filepath):
    with open(filepath, 'w', encoding='utf8', newline='') as myfile:
        wr = csv.writer(myfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for row in datalist:
            wr.writerow(row)
