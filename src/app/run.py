#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
from yokado_search.yokado_search import yokado_search
from life_search.life_search import life_search
from aeon_search.aeon_search import aeon_search
from shoplist.shoplist import shoplist


from flask import Flask

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# 店舗一覧api
app.register_blueprint(shoplist)
# 価格取得api
app.register_blueprint(yokado_search)
# 価格取得apiライフ
app.register_blueprint(life_search)
# 価格取得apiイオン
app.register_blueprint(aeon_search)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)