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
    index = int(request.form['index'])
    
    translated_text = fileManager.readTheFile(os.path.join(data_path, 'translated_text.json'))
    parsed_text = fileManager.readTheFile(os.path.join(data_path, 'parsed_text.json'))

    if 0 <= index < len(translated_text) :
        translated_text.pop(index)
        parsed_text.pop(index)

        # Save the modified lists back to JSON files
        fileManager.storeTheFile(os.path.join(data_path, 'translated_text.json'),translated_text)
        fileManager.storeTheFile(os.path.join(data_path, 'parsed_text.json'),parsed_text)

        return jsonify(success=True)

@app.route('/testTranslate')
def test():
    text = ['I am handsome','Can you help me','I like sex']
    translated_text = custom_library.translate_text(text,'zh-tw')
    return render_template('result.html',text=translated_text)

if __name__ == '__main__':
    app.run(host='localhost',port=4000,debug=True)