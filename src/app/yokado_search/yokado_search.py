#!/usr/local/bin/python3
#ヨーカドーの価格取得
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from flask import Blueprint, jsonify, request

import re

yokado_search = Blueprint('yokado_search', __name__)

@yokado_search.route("/yokado_search", methods=['POST'])
def execSearch():

    # ネットスーパーURL
    URL = request.get_json()['url']
    print("URL", URL)

    # 検索ワード
    SEARCH_WORD = '鶏肉'
    print("SEARCH_WORD", SEARCH_WORD)

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
    print("PER_100G_PRICE", PER_100G_PRICE)

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
        print("search_box ", search_box )
        search_box.send_keys(SEARCH_WORD)
        print("SEARCH_WORD", SEARCH_WORD)

        # 検索実行
        search_btn = browser.find_element_by_name("search")
        search_btn.submit()

        # ページが表示されるまで待機
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".item_list"))
        )

        # # 店舗名
        # shop_name =browser.find_element_by_css_selector(
        #     ".shopname"
        # )
        # print("shop_name", shop_name)

        # 商品名と価格のリストを取得
        goods_list =browser.find_elements_by_css_selector(
            ".item_detail"
        )
        print("item_detail", goods_list)

        total_item = []
        for item in goods_list:
            print("item", item)
            # 全角スペース削除
            detail_item = item.text.replace('\u3000', '')
            print("detail_item", detail_item)
            # リスト化
            detail_item = detail_item.splitlines()
            print("detail_item", detail_item)

            # 精肉以外はスルー
            if DOMESTIC_NAME != detail_item[DOMESTIC]:
                print("DOMESTIC_NAME", DOMESTIC_NAME )
                print("detail_item", detail_item[DOMESTIC])
                continue

            # ディクショナリー内で整形
            json_item = {
                'product': detail_item[PRODUCT_NAME],
                'price': convertPrice(detail_item[PRICE]),
                'tax_included_price': convertPrice(detail_item[TAX_INCLUDED_PRICE]),
                'per_100g': convertPrice(detail_item[PER_100G_PRICE])
            }
            print("detail_item[PRODUCT_NAME]", detail_item[PRODUCT_NAME])
            print("detail_item[PRODUCT_NAME]", detail_item[PRICE])
            print("detail_item[PRODUCT_NAME]", detail_item[TAX_INCLUDED_PRICE])
            print("detail_item[PRODUCT_NAME]", detail_item[PER_100G_PRICE])
            print("json_item:", json_item)

            total_item.append(json_item)

        result = {
            "Content-Type": "application/json",
            "shop_name": shop_name.text,
            "total_item": total_item
        }
        print("result", result)

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


# 文字列から価格を抽出
def convertPrice(str_price):
    search_price = re.findall('[\d.]+', str_price)
    return int(float(search_price[-1]))