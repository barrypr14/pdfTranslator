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

        fileManager.storeTheFile(os.path.join(self.data_path, 'parsed_text.json'),remove_newline)
        print("finish parse function")

    def prepare(self) :
        if os.path.isdir(self.upload_path) == False:
            os.mkdir('./upload')

        self.file.save(os.path.join(self.upload_path,self.file.filename))
        print("finish prepare function")
            
    def openParsed(self) :
        with open(os.path.join(self.data_path, 'parsed_text.json'), 'r', encoding='utf-8') as file:
            json_data = json.load(file)

    def parseWithLayout(self) :
        output_string = StringIO()

        with open(self.pdf_path, 'rb') as in_file:
            parser = PDFParser(in_file)
            doc = PDFDocument(parser)
            rsrcmgr = PDFResourceManager()
            device = PDFPageAggregator(rsrcmgr, laparams=LAParams(char_margin=10))
            interpreter = PDFPageInterpreter(rsrcmgr, device)

            text_list = []

            for page in PDFPage.get_pages(in_file, check_extractable=True) :
                interpreter.process_page(page)

                layout = device.get_result()

                for element in layout :
                    if isinstance(element,LTTextBox) :
                        # Check if the LTTextBox is part of a table
                        is_table = any(isinstance(e, LTRect) for e in element._objs)
                        if not is_table :
                            text_list.append(element.get_text())
                            print(element._objs)

            device.close()
            print(len(text_list))

