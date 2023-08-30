import json, os

class fileManager() :
    def __init__(self,file_path) :
        self.file_path = file_path
        self.upload_path = './upload'
        
    def storeTheFile(self,text) :
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump(text, file)

    def readTheFile(self) -> list:
        with open(self.file_path, 'r', encoding='utf-8') as file:
            read_text = json.load(file)
        return read_text
    
    def deleteData(self,deleted_indices) :
        data = self.readTheFile()
        data = [obj for obj in data if (obj['page_index'],obj['element_index']) not in deleted_indices]
        self.storeTheFile(data)

    def addData(self,item) :
        data = self.readTheFile()
        data.append(item)
        data = sorted(data, key=lambda x: (x['page_index'], x['position'][0], -x['position'][3]))
        self.storeTheFile(data)

    def getFirstRangeData(self, indices) :
        data = self.readTheFile()
        for element in data :
            if element['page_index'] == indices[0][0] and element['element_index'] == indices[0][1] :
                position = element['position']
        return position
    
class pdfFileManager() :
    def __init__(self, file) -> None:
        self.upload_path = './upload'
        self.file = file
    def prepare(self) -> None:
        if os.path.isdir(self.upload_path) == False:
            os.mkdir(self.upload_path)

        self.file.save(os.path.join(self.upload_path,self.file.filename))
    
    def getPdfPath(self) -> str:
        return  os.path.join(self.upload_path,self.file.filename)