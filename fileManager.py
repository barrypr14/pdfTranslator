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

    def addData(self,item_list) :
        data = self.readTheFile()
        for item in item_list :
            data.append(item)
        data = sorted(data, key=lambda x: (x['page_index'], x['position'][0], -x['position'][3]))
        self.storeTheFile(data)

    def getData(self, pageIndex: int, elementIndex: int, category) :
        data = self.readTheFile()
        for element in data :
            if element['page_index'] == pageIndex and element['element_index'] == elementIndex :
                item = element
                break
        
        if category == 'position' :
            return item['position']
        elif category == 'data' :
            return item
    
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
    
def checkDirExist(path) :
    if os.path.isdir(path) == False :
        os.mkdir(path)

class Log :
    def __init__(self, indices: list, mergedIndex: tuple, action: str) -> None:
        self.indices = indices
        self.mergedIndex = mergedIndex
        self.action = action 
class LogHistory :
    def __init__(self) -> None:
        self._history = []
        # self._history = [Log([(1,3),(2,5)],(1,3),'merge'),Log([(4,2)],(-1,-1),'delete')]

    def back(self) -> Log :
        if len(self._history) > 0 :
            log = self._history.pop()
            return log
        else :
            return Log([],(-1,-1),'none')

    def push(self, log: Log) :
        self._history.append(log)

    def getHistory(self) :
        return self._history