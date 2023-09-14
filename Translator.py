from googletrans import Translator

import os, json, config
from fileManager import fileManager

class googleTranslator :
    def __init__(self, text = ""):
        self.parsedManager = fileManager(os.path.join(config.data_path,'parsed_text.json'))
        self.origin_text = text
        self.prepare()

    def translate(self, dest_language) :
        translator = Translator()
        translated_list = []
        totalLength = len(self.origin_text)

        for i, paragraph in enumerate(self.origin_text):
            try : 
                translated_text = translator.translate(paragraph['text'],dest = dest_language, src='en').text
                data = {
                    "page_index" : paragraph['page_index'],
                    "element_index" : paragraph['element_index'],
                    "text" : translated_text,
                    "position" : paragraph['position']
                }
                translated_list.append(data)

                print("Already processing {} / {}".format(i,totalLength))
            except Exception as e :
                print(f"Error occurred during translation: {e}")

        jsonFileManager = fileManager(os.path.join(config.data_path, 'translated_text.json'))
        jsonFileManager.storeTheFile(translated_list)

        backupManager = fileManager(os.path.join(config.data_path, 'backup_transText.json'))
        backupManager.storeTheFile(translated_list)

    def translate_merged(self, dest_language) :
        translator = Translator()

        try : 
            translated_text = translator.translate(self.origin_text,dest = dest_language, src='en').text
        except Exception as e :
            print(f"Error occurred during translation: {e}")
        return translated_text
        
    def prepare(self) :
        if self.origin_text == "" :
            self.origin_text = self.parsedManager.readTheFile()
        