from flask import Flask, jsonify, request, make_response, abort
import os
from converter import Converter
from task1 import extract_table
from task2 import extract_event
app = Flask(__name__)

api_root = '/ccks_pdf/'
save_path = r'C:\Users\Houking\Desktop\web_api\test'
exe_path = r'C:\Users\Houking\Desktop\CCKS\run\pdf2html.exe'


@app.route(api_root + 'annualreport/', methods=['POST'])
def annualreport():
    if not request.files:
        abort(404)
    file = request.files['file']
    pdf_path = os.path.join(save_path, file.filename)
    if os.path.exists(pdf_path):
        os.remove(pdf_path)
    file.save(pdf_path)
    converter = Converter(input=pdf_path, exe=exe_path, output=save_path)
    xml_path = converter.convert()
    if xml_path:
        res = extract_table(xml_path)
        return jsonify(res)
    else:
        return jsonify('{}')

@app.route(api_root + 'hrreport/', methods=['POST'])
def hrreport():
    if not request.files:
        abort(404)
    file = request.files['file']
    pdf_path = os.path.join(save_path, file.filename)
    if os.path.exists(pdf_path):
        os.remove(pdf_path)
    file.save(pdf_path)
    converter = Converter(input=pdf_path, exe=exe_path, output=save_path)
    xml_path = converter.convert()
    if xml_path:
        res = extract_event(xml_path)
        return jsonify(res)
    else:
        return jsonify('{}')


# 404处理
@app.errorhandler(404)
def not_found(_):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.run(host='10.108.17.11', port='5000')
