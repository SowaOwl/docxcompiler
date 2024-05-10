from flask import Flask, render_template , __version__
import sys

app = Flask(__name__, template_folder='public/views')

@app.route('/')
def index():
    data = {
        'pyVersion': sys.version,
        'flaskVersion': __version__
    }
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, debug=True)