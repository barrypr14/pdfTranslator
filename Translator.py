from googletrans import Translator

import os, json
import fileManager
class googleTranslator :
    def __init__(self, dest_language, text=""):
        self.data_path = './data/'
        self.dest_language = dest_language
        self.origin_text = text
        self.prepare()

    def translate(self) :
        print("start translate")
        translator = Translator()
        translated_text = []

        for paragraph in self.origin_text.values():
            try : 
                translated_text.append(translator.translate(paragraph,dest = self.dest_language, src='en').text)
            except Exception as e :
                print(f"Error occurred during translation: {e}")

        translated_data = {index: item for index, item in enumerate(translated_text)}
        fileManager.storeTheFile(os.path.join(self.data_path, 'translated_text.json'),translated_data)

    def translate_merged(self) :
        print("start translate the text which is merged")
        translator = Translator()

        try : 
            translated_text = translator.translate(self.origin_text,dest = self.dest_language, src='en').text
        except Exception as e :
            print(f"Error occurred during translation: {e}")
        return translated_text
        
    def prepare(self) :
        if self.origin_text == "" :
            self.origin_text = fileManager.readTheFile(os.path.join(self.data_path, 'parsed_text.json'))