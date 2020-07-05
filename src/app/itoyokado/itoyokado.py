#!/usr/local/bin/python3
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from flask import Blueprint, jsonify, request

import re

itoyokado = Blueprint('itoyokado', __name__)

@itoyokado.route("/itoyokado/search", methods=['POST'])
def execSearch():

    # ネットスーパーURL
    URL = request.get_json()['url']

    # 検索ワード
    SEARCH_WORD = '鶏肉'

    # 産地
    DOMESTIC = 0
    # 産地名
    DOMESTIC_NAME = '国産'
    # 商品名
    PRODUCT_NAME = 1
    # 税抜き価格
    PRICE = 2
    # 税込み価格
    TAX_INCLUDED_PRICE = 3
    # 100gあたり
    PER_100G_PRICE = 4

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

        # キーワードの入力
        search_box = browser.find_element_by_id("searchtxt")
        search_box.send_keys(SEARCH_WORD)

        # 検索実行
        search_btn = browser.find_element_by_name("search")
        search_btn.submit()

        # ページが表示されるまで待機
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".goodslist"))
        )    

        # 店舗名
        shop_name =browser.find_element_by_css_selector(
            ".shopname"
        )

        # 商品名と価格のリストを取得
        goods_list =browser.find_elements_by_css_selector(
            ".goodsitem"
        )

        total_item = []
        for item in goods_list:

            # 全角スペース削除
            detail_item = item.text.replace('\u3000', '')
            # リスト化
            detail_item = detail_item.splitlines()

            # 精肉以外はスルー
            if DOMESTIC_NAME != detail_item[DOMESTIC]:
                continue

            # ディクショナリー内で整形
            json_item = {
                'product': detail_item[PRODUCT_NAME],
                'price': convertPrice(detail_item[PRICE]),
                'tax_included_price': convertPrice(detail_item[TAX_INCLUDED_PRICE]),
                'per_100g': convertPrice(detail_item[PER_100G_PRICE])
            }

            print("json_item:", json_item)

            total_item.append(json_item)

        result = {
            "Content-Type": "application/json",
            "shop_name": shop_name.text,
            "total_item": total_item
        }

        return jsonify(result)

        # スクリーンショット
        # browser.save_screenshot('images/' + dtstr + '.png')

    except NoSuchElementException as e:
        print("NoSuchElementException!!!")

        reslut = {
            "Content-Type": "application/json",
            "Error": "NoSuchElementException"
        }

        return jsonify(result)
    finally:
        # 終了
        browser.close()
        browser.quit()

@itoyokado.route("/itoyokado/shoplist", methods=['GET'])
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

# 文字列から価格を抽出
def convertPrice(str_price):
    search_price = re.findall('[\d.]+', str_price)
    return int(float(search_price[-1]))