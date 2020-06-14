import csv, json

csvFilePath = "D:/Kuliah/Big Data/Merge/CrawlingJaktim.csv"
jsonFilePath = "CrawlingJaktim.json"

data = {}
with open(csvFilePath) as csvFile:
    csvReader = csv.DictReader(csvFile)
    for rows in csvReader:
        id = rows["id"]
        data[id] = rows

with open(jsonFilePath, "w") as jsonFile:
    jsonFile.write(json.dumps(data, indent = 4))