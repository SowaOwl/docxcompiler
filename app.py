from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Привет, мир! Это мое первое Flask приложение.'

# Если этот скрипт запускается напрямую, а не импортируется
if __name__ == '__main__':
    app.run(debug=True)