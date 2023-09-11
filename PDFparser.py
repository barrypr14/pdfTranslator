import os, json, re

from pdfminer.high_level import extract_pages
from pdfminer.layout import LAParams, LTTextBox

from fileManager import fileManager, pdfFileManager
import config

class PdfParser :
    def __init__(self, file) :
        self.file = file
        self.pdfManager = pdfFileManager(file)
        self.prepare()

    def prepare(self) :
        self.pdfManager.prepare()
            
    def openParsed(self) :
        with open(os.path.join(self.data_path, 'parsed_text.json'), 'r', encoding='utf-8') as file:
            json_data = json.load(file)

    def parseWithOutBound(self) :
        main_content = []

        pdfPath = self.pdfManager.getPdfPath()
        for page_index, page_layout in enumerate(extract_pages(pdfPath, laparams= LAParams(char_margin=10))) :
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
        jsonFileManager = fileManager(os.path.join(config.data_path, 'parsed_text.json'))
        jsonFileManager.storeTheFile(sorted_data)

def filter_figure_captions(text) :
    if not re.match(r'^(Fig|Table)\.?\s*\d+', text, re.IGNORECASE) :
        return False
    return True


