from flask import Flask, render_template , __version__, Blueprint, request, jsonify
import sys
from handlers.DocxHandler import DocxHandler

docx_handler = DocxHandler()
app = Flask(__name__, template_folder='public/views')
api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/extract', methods=['POST'])
def api_test():
    if 'file' not in request.files:
        return 'No file'
    
    file = request.files['file']
    if file.filename.endswith('.docx'):
        try:
            return jsonify(docx_handler.extract(file))
        except Exception as e:
            return jsonify({"error": str(e)})
    else:
        return jsonify({"error": "Invalid file format. Please upload a .docx file."})


@app.route('/')
def index():
    data = {
        'pyVersion': sys.version,
        'flaskVersion': __version__
    }
    return render_template('index.html', data=data)

app.register_blueprint(api)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, debug=True)