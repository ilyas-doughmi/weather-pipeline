import os


def bronzedata(path):
    jsonFile = []
    for file in os.listdir(path):
        if ".json" in file and "-failed.json" not in file:
            jsonFile.append(file)

    return jsonFile


if __name__ ==  "__main__":
   print( bronzedata("bronze"))