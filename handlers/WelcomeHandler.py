from flask import render_template, __version__
import sys

class WelcomeHandler:

    def welcome(self):
        data = {
            'pyVersion': sys.version,
            'flaskVersion': __version__
        }
        return render_template('index.html', data=data)