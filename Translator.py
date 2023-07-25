from googletrans import Translator

import os
import json 

class googleTranslator :
    def __init__(self, dest_language):
        self.data_path = './data/'
        self.dest_language = dest_language
        self.json_data = ""
        self.prepare()

    def translate(self) :
        print("start translate")
        translator = Translator()
        translated_text = []
        for paragraph in self.json_data :
            try : 
                translated_text.append(translator.translate(paragraph,dest = self.dest_language, src='en').text)
            except Exception as e :
                print(f"Error occurred during translation: {e}")
        
        with open(os.path.join(self.data_path, 'translated_text.json'),'w', encoding='utf-8') as file :
            json.dump(translated_text,file)

        
    def prepare(self) :
        with open(os.path.join(self.data_path, 'parsed_text.json'), 'r', encoding='utf-8') as file:
            self.json_data = json.load(file)