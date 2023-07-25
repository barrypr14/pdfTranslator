from io import StringIO
import os
import json 

from pdfminer.converter import TextConverter, PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTImage, LTText
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser


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

        with open(os.path.join(self.data_path, 'parsed_text_before.json'), 'w', encoding='utf-8') as file:
            json.dump(output_string.getvalue(),file)
        # split into paragraph
        split_to_paragraph = output_string.getvalue().split("\n\n")

        # remove new line character
        remove_newline = []
        for paragraph in split_to_paragraph :
            remove_newline.append(paragraph.replace("\n",""))

        with open(os.path.join(self.data_path, 'parsed_text.json'), 'w', encoding='utf-8') as file:
            json.dump(remove_newline,file)
        print("finish parse function")

    def prepare(self) :
        if os.path.isdir(self.upload_path) == False:
            os.mkdir('./upload')

        self.file.save(os.path.join(self.upload_path,self.file.filename))
        print("finish prepare function")
            
    def openParsed(self) :
        with open(os.path.join(self.data_path, 'parsed_text.json'), 'r', encoding='utf-8') as file:
            json_data = json.load(file)
