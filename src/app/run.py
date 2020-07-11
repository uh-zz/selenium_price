#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
from itoyokado.itoyokado import itoyokado
from life.life import life
from aeon.aeon import aeon

from flask import Flask

import sys

# キャッシュを作らない
sys.dont_write_bytecode = True

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

app.register_blueprint(itoyokado)
app.register_blueprint(life)
app.register_blueprint(aeon)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)