from sys import version
from flask import render_template, __version__

class WelcomeHandler:
    @staticmethod
    def welcome() -> str:
        data = {
            'pyVersion': version,
            'flaskVersion': __version__
        }
        return render_template('index.html', data=data)