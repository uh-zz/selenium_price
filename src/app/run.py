#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
from search.search import search
from shoplist.shoplist import shoplist

from flask import Flask

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# 店舗一覧api
app.register_blueprint(shoplist)
# 価格取得api
app.register_blueprint(search)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)