from io import StringIO
import os, json

from pdfminer.converter import TextConverter, PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTImage, LTText, LTTextLine,LTRect
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

import fileManager
class PdfParser :
    def __init__(self, file) :
        self.file = file
        self.data_path = './data/'
        self.upload_path = './upload/' 
        self.pdf_path = self.upload_path + self.file.filename
        self.prepare()

    def parse(self) :
        output_string = StringIO()

        with open(self.pdf_path, 'rb') as in_file:
            parser = PDFParser(in_file)
            doc = PDFDocument(parser)
            rsrcmgr = PDFResourceManager()
            device = TextConverter(rsrcmgr, output_string, laparams=LAParams(char_margin=10))
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            for page in PDFPage.create_pages(doc):
                interpreter.process_page(page)
            device.close()

        fileManager.storeTheFile(os.path.join(self.data_path, 'parsed_text_before.json'),output_string.getvalue())
        # split into paragraph
        split_to_paragraph = output_string.getvalue().split("\n\n")

        # remove new line character
        remove_newline = []
        for paragraph in split_to_paragraph :
            remove_newline.append(paragraph.replace("\n"," "))

        parsed_data = {index: item for index,item in enumerate(remove_newline)} 
        print("the type of parsed data in parser module => ",type(parsed_data))
        fileManager.storeTheFile(os.path.join(self.data_path, 'parsed_text.json'),parsed_data)
        print("finish parse function")

    def prepare(self) :
        if os.path.isdir(self.upload_path) == False:
            os.mkdir('./upload')

        self.file.save(os.path.join(self.upload_path,self.file.filename))
        print("finish prepare function")
            
    def openParsed(self) :
        with open(os.path.join(self.data_path, 'parsed_text.json'), 'r', encoding='utf-8') as file:
            json_data = json.load(file)

