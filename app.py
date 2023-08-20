import os
import json
from flask import Flask, request, redirect, session, url_for, render_template, jsonify
import custom_library

from PDFparser import PdfParser
from Translator import googleTranslator
import fileManager

app = Flask(__name__)
app.jinja_env.filters['zip'] = zip

upload_path = './upload/'
data_path = './data/'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return 'No file part in the request'
    
    file = request.files['file']

    if file.filename == '' :
        return 'No selected file'
    
    if file:
        if os.path.isdir(data_path) == False :
            os.mkdir('./data')

        # Create a module to parse the PDF file
        parser = PdfParser(file)
        parser.parse()

        # parser = PdfParser(file)
        # parser.parseWithLayout()

        # Crate a module to translate the text
        trans = googleTranslator('zh-tw')
        trans.translate()

        return redirect(url_for('result'))
   
@app.route('/result')
def result():
    json_data_translated = fileManager.readTheFile(os.path.join(data_path, 'translated_text.json'))
    json_data_parsed = fileManager.readTheFile(os.path.join(data_path, 'parsed_text.json'))
    return render_template('result.html',text=json_data_translated, origin=json_data_parsed)

@app.route('/delete', methods=['POST'])
def delete() :
    indices = request.form.getlist('indices[]')
    indices = [int(index) for index in indices]

    translated_text = fileManager.readTheFile(os.path.join(data_path, 'translated_text.json'))
    parsed_text = fileManager.readTheFile(os.path.join(data_path, 'parsed_text.json'))
    
    try:
        for index in indices :
            if 0 <= index < len(translated_text) :
                translated_text.pop(str(index))
                parsed_text.pop(str(index))

        # Save the modified lists back to JSON files
        fileManager.storeTheFile(os.path.join(data_path, 'translated_text.json'),translated_text)
        fileManager.storeTheFile(os.path.join(data_path, 'parsed_text.json'),parsed_text)

        return jsonify(success=True)
    except:
        return jsonify(success=False, error='Invalid index')

@app.route('/translate', methods=['POST'])
def translate():
    print("start to translate a new merged text")
    text = request.form['text']
    indices = request.form.getlist('indices[]')
    indices = [int(index) for index in indices]

    translated_text = fileManager.readTheFile(os.path.join(data_path, 'translated_text.json'))
    parsed_text = fileManager.readTheFile(os.path.join(data_path, 'parsed_text.json'))
    try :
        translator = googleTranslator('zh-tw',text=text)
        translated_merged_text = translator.translate_merged()
        print("the type of the translated_text from the fileManager is {}".format(type(translated_text)))
        for index in indices :
            if 0 <= index < len(translated_text) and index != indices[0] :
                del translated_text[str(index)]
                del parsed_text[str(index)]
                print("delete the {} in the parsed_text.json".format(index))
        
        translated_text[indices[0]] = translated_merged_text
        parsed_text[indices[0]] = text

        # Save the modified lists back to JSON files
        fileManager.storeTheFile(os.path.join(data_path, 'translated_text.json'),translated_text)
        fileManager.storeTheFile(os.path.join(data_path, 'parsed_text.json'),parsed_text)        

        return jsonify(success=True, text=translated_merged_text)
    except :
        return jsonify(success=False, erro='Invalid merged')

if __name__ == '__main__':
    app.run(host='localhost',port=4000,debug=True)