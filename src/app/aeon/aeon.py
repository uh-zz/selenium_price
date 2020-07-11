#!/usr/local/bin/python3
#イオンの価格取得
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys


from flask import Blueprint, jsonify, request

import re

aeon = Blueprint('aeon', __name__)

@aeon.route("/aeon/search", methods=['POST'])
def execSearch():

    # 検索ワード
    SEARCH_WORD = '鶏肉'
    # 産地
    DOMESTIC = 0
    # 産地名
    DOMESTIC_NAME = '100gあたり'
    # 商品名
    PRODUCT_NAME = 0
    # 税抜き価格
    PRICE = 2
    # 税込み価格
    TAX_INCLUDED_PRICE = 4
    # 100gあたり
    PER_100G_PRICE = 0

    # スクリーンショットのファイル名用日付を取得
    # dt = datetime.datetime.today()
    # dtstr = dt.strftime("%Y%m%d%H%M%S")
    try:

        # HEADLESSブラウザに接続
        browser = webdriver.Remote(
            command_executor='http://selenium-hub:4444/wd/hub',
            desired_capabilities=DesiredCapabilities.CHROME)

        browser.implicitly_wait(2)

        paramURL = request.get_json()['url']
        if not paramURL:
            url = getShopURL(browser, request.get_json()['shop']) 
        else:
            url = paramURL

        browser.get(url)

        # キーワードの入力
        search_box = browser.find_element_by_id("search")
        search_box.send_keys(SEARCH_WORD)

        # 検索実行
        search_btn = browser.find_element_by_id("cx-search-button")
        search_btn.submit()

        # ページが表示されるまで待機
        WebDriverWait(browser, 100).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".breadcrumb-item-search"))
        )

        # # 店舗名
        shop_name =browser.find_element_by_css_selector(
            ".info-title"
        )

        # 商品名と価格のリストを取得
        goods_list =browser.find_elements_by_css_selector(
            ".product-item "
        )

        total_item = []
        for item in goods_list:
            # 全角スペース削除
            detail_item = item.text.replace('\u3000', '')
            # リスト化
            detail_item = detail_item.splitlines()

            # 精肉以外はスルー
            if DOMESTIC_NAME not in detail_item[DOMESTIC]:
                continue

            # ディクショナリー内で整形
            json_item = {
                'product': detail_item[PRODUCT_NAME],
                'price': convertPrice(detail_item[PRICE]),
                'tax_included_price': convertTaxedPrice(detail_item[TAX_INCLUDED_PRICE]),
                'per_100g': pickPricePer100g(detail_item[PER_100G_PRICE])
            }

            total_item.append(json_item)

        result = {
            "Content-Type": "application/json",
            "shop_name": shop_name.text,
            "total_item": total_item,
            "shop_url": url
        }

        return jsonify(result)

        # スクリーンショット
        # browser.save_screenshot('images/' + dtstr + '.png')

    except NoSuchElementException as e:
        print("NoSuchElementException!!!")

        NoSuchReslut = {
            "Content-Type": "application/json",
            "Error": "NoSuchElementException"
        }

        return jsonify(NoSuchReslut)
    except TimeoutException as e:
        print("TimeoutException!!!")

        TimeOutReslut = {
            "Content-Type": "application/json",
            "Error": "TimeoutException"
        }

        return jsonify(TimeOutReslut)
    finally:
        # 終了
        browser.close()
        browser.quit()

@aeon.route("/aeon/shoplist", methods=['GET'])
def execGetShopList():

    # 店舗一覧
    URL = 'https://shop.aeon.com/netsuper/store/available'
    GOOGLE_URL = 'https://google.com'
    PREFIX= '　ネットスーパー'

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
            EC.presence_of_element_located((By.CSS_SELECTOR, ".section-title-text"))
        )

        table_list =browser.find_elements_by_css_selector(
            ".box.box-square.round-less"
        )

        shop_list = []
        for shop_number in range(len(table_list)):
            
            table = table_list[shop_number]

            shop_prefecture = table.find_element_by_css_selector(
               ".box-header-title"
            )

            shop_li_list = table.find_elements_by_tag_name(
                'li'
            )

            # 各都道府県ごとに処理 
            for shop_li in shop_li_list:
                
                shop_name = shop_li.get_attribute("textContent").split("　")[1]


                shop_json = {
                    "prefecture": shop_prefecture.get_attribute("textContent"),
                    "shop_name": shop_name,
                    # "url": results[0]
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

def getShopURL(browser, shop_name):

    GOOGLE_URL = 'https://google.com'
    PREFIX= '　ネットスーパー'

    browser.get(GOOGLE_URL)

    input_box = browser.find_element_by_name(
        'q'
    )
    
    input_box.send_keys(shop_name + PREFIX)
    input_box.send_keys(Keys.RETURN)

    # ページが表示されるまで待機
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "result-stats"))
    )
    
    results = []
    [results.append(a.get_attribute('href')) for a in browser.find_elements_by_css_selector('.r a')]
    return results[0]

# 文字列から価格を抽出
def convertTaxedPrice(str_price):
    search_price = re.findall('[\d.]+', str_price)
    return int(float(search_price[0]))

def convertPrice(str_price):
    search_price = re.findall('[\d.]+', str_price)
    return int(search_price[-1])

def pickPricePer100g(str_price):
    search_price = re.findall('[\d.]+', str_price)
    return int(search_price[-2])