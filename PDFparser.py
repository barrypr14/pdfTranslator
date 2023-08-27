from io import StringIO
import os, json, re
from operator import attrgetter

from pdfminer.high_level import extract_pages
# from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams, LTTextBox
# from pdfminer.pdfdocument import PDFDocument
# from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
# from pdfminer.pdfpage import PDFPage
# from pdfminer.pdfparser import PDFParser

import fileManager
class PdfParser :
    def __init__(self, file) :
        self.file = file
        self.data_path = './data/'
        self.upload_path = './upload/' 
        self.pdf_path = self.upload_path + self.file.filename
        self.prepare()

    # def parse(self) :
    #     output_string = StringIO()

    #     with open(self.pdf_path, 'rb') as in_file:
    #         parser = PDFParser(in_file)
    #         doc = PDFDocument(parser)
    #         rsrcmgr = PDFResourceManager()
    #         device = TextConverter(rsrcmgr, output_string, laparams=LAParams(char_margin=10))
    #         interpreter = PDFPageInterpreter(rsrcmgr, device)
    #         for page in PDFPage.create_pages(doc):
    #             interpreter.process_page(page)
    #         device.close()

    #     fileManager.storeTheFile(os.path.join(self.data_path, 'parsed_text_before.json'),output_string.getvalue())
    #     # split into paragraph
    #     split_to_paragraph = output_string.getvalue().split("\n\n")

    #     # remove new line character
    #     remove_newline = []
    #     for paragraph in split_to_paragraph :
    #         remove_newline.append(paragraph.replace("\n"," "))

    #     parsed_data = {index: item for index,item in enumerate(remove_newline)} 
    #     print("the type of parsed data in parser module => ",type(parsed_data))
    #     fileManager.storeTheFile(os.path.join(self.data_path, 'parsed_text.json'),parsed_data)
    #     print("finish parse function")

    def prepare(self) :
        if os.path.isdir(self.upload_path) == False:
            os.mkdir('./upload')

        self.file.save(os.path.join(self.upload_path,self.file.filename))
        print("finish prepare function")
            
    def openParsed(self) :
        with open(os.path.join(self.data_path, 'parsed_text.json'), 'r', encoding='utf-8') as file:
            json_data = json.load(file)

    def parseWithOutBound(self) :
        main_content = []
        
        for page_index, page_layout in enumerate(extract_pages(self.pdf_path, laparams= LAParams(char_margin=10))) :
            page_height = page_layout.height
            header_threshold = 0.95 * page_height
            footer_threshold = 0.05 * page_height
            
            for index, element in enumerate(page_layout) :
                if isinstance(element, LTTextBox) :
                    x0, y0, x1, y1 = element.bbox
                    
                    # Remove the header and footer
                    if y1 >= header_threshold or y0 <= footer_threshold or len(element.get_text()) < 10:
                        continue
                    # Remove the text along with the Image
                    if filter_figure_captions(element.get_text()) :
                        continue
                    
                    # Deal with the two column pdf, but it should be improved
                    if page_layout.width/2 > x0 :
                        x0 = page_layout.width * 0.1
                    else :
                        x0 = page_layout.width / 2
                    
                    text = element.get_text().replace("\n"," ")
                    data = {
                        "page_index" : page_index,
                        "element_index" : index,
                        "text" : text,
                        "position" : [x0, y0, x1, y1]
                    }
                    main_content.append(data)
                    
        sorted_data = sorted(main_content, key=lambda x: (x['page_index'], x['position'][0], -x['position'][3]))
        fileManager.storeTheFile(os.path.join(self.data_path, 'parsed_text.json'),sorted_data)

def filter_figure_captions(text) :
    if not re.match(r'^(Fig|Table)\.?\s*\d+', text, re.IGNORECASE) :
        return False
    return True


