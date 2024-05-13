from flask import Flask, render_template , __version__, Blueprint, request, jsonify
from handlers.DocxHandler import DocxHandler
from handlers.WelcomeHandler import WelcomeHandler

docx_handler = DocxHandler()
welcome_handler = WelcomeHandler()
app = Flask(__name__, template_folder='public/views')
api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/extract', methods=['POST'])
def extract():
    return docx_handler.extract(request)
    
@api.route('/fill-file', methods=['POST'])
def fill_file():
    return docx_handler.fill_file(request)

@app.route('/')
def index():
    return welcome_handler.welcome()

app.register_blueprint(api)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, debug=True)