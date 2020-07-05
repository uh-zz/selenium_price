#!/usr/local/bin/python3
#ライフの価格取得
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from flask import Blueprint, jsonify, request

import re
import sys

# キャッシュを作らない
sys.dont_write_bytecode = True

life = Blueprint('life', __name__)

@life.route("/life/search", methods=['POST'])
def execSearch():

    # ネットスーパーURL
    URL = request.get_json()['url']

    # 検索ワード
    SEARCH_WORD = '鶏肉'

    # 産地
    DOMESTIC = 3
    # 産地名
    DOMESTIC_NAME = '国内産'

    # 商品名
    PRODUCT_NAME = 4
    # 税抜き価格
    PRICE = 0
    # 税込み価格
    TAX_INCLUDED_PRICE = 2
    # 100gあたり
    PER_100G_PRICE = 4


    SEARCH_BOX_ID = "searchTextId"
    SEARCH_BTN_ID = "searchSubmitId"
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

        # キーワードの入力 //変数化可能
        search_box = browser.find_element_by_id(SEARCH_BOX_ID)
        search_box.send_keys(SEARCH_WORD)

        # 検索実行 find_element_by_nameがid
        search_btn = browser.find_element_by_id(SEARCH_BTN_ID)
        search_btn.submit()

        # ページが表示されるまで待機
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".item_list"))
        )


        # 商品名と価格のリストを取得
        goods_list =browser.find_elements_by_css_selector(
            ".item_detail"
        )
        print("goods_list", goods_list)

        total_item = []
        for item in goods_list:
            print("item", item )

            # 全角スペース削除
            detail_item = item.text.replace('\u3000', '')
            print("detail_item", detail_item)
            # リスト化
            detail_item = detail_item.splitlines()
            print("detail_item", detail_item)

            # 精肉以外はスルー
            if DOMESTIC_NAME != detail_item[DOMESTIC]:
                continue
                print("DOMESTIC_NAME ", detail_item[DOMESTIC] )


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

@life.route("/life/shoplist", methods=['GET'])
def execGetShopList():

    # 店舗一覧
    URL = 'https://www.life-netsuper.jp/'

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

        # ページが表示されるまで待機
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".entry_title"))
        )
                        
        # 関東圏
        kanto_json = formatShopList(browser, "disp1")
        # 関西圏
        kansai_json = formatShopList(browser, "disp2")
      
        # 2つのリストを結合
        kanto_json.extend(kansai_json)

        result = {
            "Content-Type": "application/json",
            "shop_list": kanto_json            
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

# レスポンス用に店舗リストを整形
def formatShopList(browser, div_name):
    table_list =browser.find_element_by_id(
        div_name
    )

    prefecture_list = table_list.find_elements_by_css_selector(
        ".anarea"
    )

    # 店舗
    shop_ul_list = table_list.find_elements_by_tag_name(
        'ul'
    )

      
    shop_list = []
    for shop_number in range(len(shop_ul_list)):
        
        shop_prefecture = prefecture_list[shop_number]
        shop_li_list = shop_ul_list[shop_number].find_elements_by_tag_name(
            'li'
        )

        # 各都道府県ごとに処理 
        for shop_li in shop_li_list:
            
            shop_p = shop_li.find_element_by_tag_name(
                'p'
            )
            shop_a = shop_li.find_element_by_tag_name(
                'a'
            )
            shop_json = {
                "prefecture": shop_prefecture.get_attribute("textContent"),
                "shop_name": shop_p.get_attribute("textContent"),
                "url": shop_a.get_attribute('href')
            }

            shop_list.append(shop_json)

    return shop_list