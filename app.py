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
        # parser = PdfParser(file)
        # parser.parse()

        parser = PdfParser(file)
        parser.parseWithOutBound()

        # Crate a module to translate the text
        trans = googleTranslator('zh-tw')
        trans.translate()

        # return redirect(url_for('test'))
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
    indices = [tuple(int(num) for num in index.split('-') )for index in indices]
    
    # Get the origin data 
    translated_text = fileManager.readTheFile(os.path.join(data_path, 'translated_text.json'))
    parsed_text = fileManager.readTheFile(os.path.join(data_path, 'parsed_text.json'))
    
    # Start to remove the index that is useless for user
    try:
        parsed_text = [obj for obj in parsed_text if (obj['page_index'],obj['element_index']) not in indices]
        translated_text = [obj for obj in translated_text if  (obj['page_index'],obj['element_index']) not in indices]
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
    indices = [tuple(int(num) for num in index.split('-') )for index in indices]

    indices = sorted(indices, key=lambda x : (x[0],x[1]))
    # Get the origin data 
    translated_text = fileManager.readTheFile(os.path.join(data_path, 'translated_text.json'))
    parsed_text = fileManager.readTheFile(os.path.join(data_path, 'parsed_text.json'))

    # Start to delete the content in the origin dictionary and put the new translated text in the corresponding index
    try :
        translator = googleTranslator('zh-tw',text=text)
        translated_merged_text = translator.translate_merged()
        
        # get the first element position
        for element in translated_text :
            if element['page_index'] == indices[0][0] and element['element_index'] == indices[0][1] :
                position = element['position']
        
        translated_data = {
            "page_index" : indices[0][0],
            "element_index" : indices[0][1],
            "text" : translated_merged_text,
            "position" : position
        }
        parsed_data = {
            "page_index" : indices[0][0],
            "element_index" : indices[0][1],
            "text" : text,
            "position" : position
        }
    
        # delete the origin selected data
        parsed_text = [obj for obj in parsed_text if (obj['page_index'],obj['element_index']) not in indices]
        translated_text = [obj for obj in translated_text if  (obj['page_index'],obj['element_index']) not in indices]
        # put the new data in the file
        translated_text.append(translated_data)
        parsed_text.append(parsed_data)

        # sort the file again to the correct order
        translated_text = sorted(translated_text, key=lambda x: (x['page_index'], x['position'][0], -x['position'][3]))
        parsed_text = sorted(parsed_text, key=lambda x: (x['page_index'], x['position'][0], -x['position'][3]))

        # Save the modified lists back to JSON files
        fileManager.storeTheFile(os.path.join(data_path, 'translated_text.json'),translated_text)
        fileManager.storeTheFile(os.path.join(data_path, 'parsed_text.json'),parsed_text)        

        return jsonify(success=True, text=translated_merged_text, indices = indices)
    except :
        return jsonify(success=False, error='Invalid merged')

@app.route('/download', methods=['GET'])
def download():
    translated_text = fileManager.readTheFile(os.path.join(data_path, 'translated_text.json'))
    parsed_text = fileManager.readTheFile(os.path.join(data_path, 'parsed_text.json'))

    try:
        doc = Document()
        doc.add_heading("The Translated text from PDFTranslator", level=1)
        for (trans_value, parse_value)in zip(translated_text,parsed_text):
            parse_value = parse_value['text'].replace('\f',' ')
            trans_value = trans_value['text'].replace('\f',' ')

            doc.add_paragraph("Origin / Translated Text", style='List Number')
            doc.add_paragraph(parse_value, style='Normal')
            doc.add_paragraph(trans_value, style='Normal')
        
        doc.save('./download/output.docx')
        return jsonify(success=True)
    except Exception as e:
        print(e)
        return jsonify(success=False, error = e)

@app.route('/test')
def test() :
    data = fileManager.readTheFile(os.path.join(data_path, 'parsed_text.json'))
    return render_template('test.html',text=data)

if __name__ == '__main__':
    app.run(host='localhost',port=4000,debug=True)