import os
from flask import Flask, request, redirect, url_for, render_template, jsonify

from PDFparser import PdfParser
from Translator import googleTranslator
import fileManager
from docx import Document

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
    print("Let start removing the useless text")
    indices = request.form.getlist('indices[]')
    indices = [int(index) for index in indices]

    # Get the origin data 
    translated_text = fileManager.readTheFile(os.path.join(data_path, 'translated_text.json'))
    parsed_text = fileManager.readTheFile(os.path.join(data_path, 'parsed_text.json'))
    
    # Start to remove the index that is useless for user
    try:
        for index in indices :
            if 0 <= index < int(max(translated_text.keys())):
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
    print("Let start to translate a new merged text")
    text = request.form['text']
    indices = request.form.getlist('indices[]')
    indices = [int(index) for index in indices]

    # Get the origin data 
    translated_text = fileManager.readTheFile(os.path.join(data_path, 'translated_text.json'))
    parsed_text = fileManager.readTheFile(os.path.join(data_path, 'parsed_text.json'))

    # Start to delete the content in the origin dictionary and put the new translated text in the corresponding index
    try :
        translator = googleTranslator('zh-tw',text=text)
        translated_merged_text = translator.translate_merged()
        
        for index in indices :
            if 0 <= index < len(translated_text) and index != indices[0] :
                del translated_text[str(index)]
                del parsed_text[str(index)]
                print("delete the {} in the parsed_text.json".format(index))
        
        translated_text[str(indices[0])] = translated_merged_text
        parsed_text[str(indices[0])] = text

        # Save the modified lists back to JSON files
        fileManager.storeTheFile(os.path.join(data_path, 'translated_text.json'),translated_text)
        fileManager.storeTheFile(os.path.join(data_path, 'parsed_text.json'),parsed_text)        

        return jsonify(success=True, text=translated_merged_text)
    except :
        return jsonify(success=False, error='Invalid merged')

@app.route('/download', methods=['GET'])
def download():
    translated_text = fileManager.readTheFile(os.path.join(data_path, 'translated_text.json'))
    parsed_text = fileManager.readTheFile(os.path.join(data_path, 'parsed_text.json'))

    try:
        doc = Document()
        doc.add_heading("The Translated text from PDFTranslator", level=1)
        for index, (trans_key, trans_value) in enumerate(translated_text.items()):
            parse_value = parsed_text.get(trans_key,"").replace('\f',' ')
            trans_value = trans_value.replace('\f',' ')

            doc.add_paragraph(parse_value, style='Normal')
            doc.add_paragraph(trans_value, style='Normal')
        
        doc.save('./download/output.docx')
        return jsonify(success=True)
    except:
        return jsonify(success=False)

if __name__ == '__main__':
    app.run(host='localhost',port=4000,debug=True)