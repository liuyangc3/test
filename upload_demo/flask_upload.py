#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'web'

import os.path

from flask import Flask
from flask import render_template
from flask import request
from flask.views import MethodView

from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/tmp/upload'


class Upload(MethodView):
    def get(self):
        return render_template('index.html')

    def post(self):
        _file = request.files['file']
        _filename = secure_filename(_file.filename)
        try:
            _file.save(os.path.join(UPLOAD_FOLDER, _filename))
            return 'OK'
        except IOError, e:
            return '保存文件[%s]失败: %s' % (_filename, e), 405


app = Flask(__name__)
app.add_url_rule('/upload', view_func=Upload.as_view('publish'))

if __name__ == '__main__':
    app.run()
