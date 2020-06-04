#!/usr/local/bin/python3
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException

from flask import Blueprint, jsonify, request

import sys

# キャッシュを作らない
sys.dont_write_bytecode = True

shoplist = Blueprint('shoplist', __name__)

@shoplist.route("/shoplist", methods=['GET'])
def execGetShopList():

    # 店舗一覧
    URL = 'https://www.iy-net.jp/nspc/info/shoplist.do'

    # スクリーンショットのファイル名用に日付を取得
    # dt = datetime.datetime.today()
    # dtstr = dt.strftime("%Y%m%d%H%M%S")

    try:
        # HEADLESSブラウザに接続
        browser = webdriver.Remote(
            command_executor='http://selenium-hub:4444/wd/hub',
            desired_capabilities=DesiredCapabilities.CHROME)

        # 最初のページ
        browser.get(URL)
        
        # テーブル取得
        shop_table =browser.find_element_by_css_selector(
            "table.tableblock.bdright0.bdleft0.uAL.uLhL"
        )
        shop_table_trs = shop_table.find_elements_by_tag_name(
            'tr'
        )

        # 店舗一覧
        shop_list = []

        # エリアごとに処理
        for shop_table_tr in shop_table_trs:

            shop_table_tds = shop_table_tr.find_elements_by_tag_name(
                'td'
            )

            for shop_table_td in shop_table_tds:

                # 都道府県
                shop_prefectures = shop_table_td.find_elements_by_tag_name(
                    'p'
                )
                # 店舗
                shop_names = shop_table_td.find_elements_by_tag_name(
                    'ul'
                )

                # 各都道府県ごとに処理
                for shop_number in range(len(shop_prefectures)):
                    
                    shop_prefecture = shop_prefectures[shop_number]
                    shop_name = shop_names[shop_number]

                    shops = shop_name.find_elements_by_tag_name(
                        'li > a'
                    )

                    for shop in shops:
                        shop_json = {
                            "prefecture": shop_prefecture.text,
                            "shop_name": shop.text,
                            "url": shop.get_attribute('href')
                        }

                        shop_list.append(shop_json)

        result = {
            "Content-Type": "application/json",
            "shop_list": shop_list
        }

        return jsonify(result)
    finally:
        # 終了
        browser.close()
        browser.quit()