from flask import render_template, __version__
import sys

class WelcomeHandler:
    @staticmethod
    def welcome() -> str:
        data = {
            'pyVersion': sys.version,
            'flaskVersion': __version__
        }
        return render_template('index.html', data=data)