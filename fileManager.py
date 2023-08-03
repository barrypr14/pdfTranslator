import json

def storeTheFile(filePath, text) :
    with open(filePath, 'w', encoding='utf-8') as file:
        json.dump(text, file)

def readTheFile(filePath) :
    with open(filePath, 'r', encoding='utf-8') as file:
        read_text = json.load(file)
    return read_text