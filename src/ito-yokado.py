#!/usr/local/bin/python3
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import datetime
import json

def execSearch(browser: webdriver):

    # ネットスーパーURL
    URL = 'https://www.iy-net.jp/nspc/shoptop.do?shopcd=00239'

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
        if False == DOMESTIC_NAME in detail_item[DOMESTIC]:
            continue

        # ディクショナリー内で整形
        json_item = {
            'product': detail_item[PRODUCT_NAME],
            'price': detail_item[PRICE],
            'tax_included_price': detail_item[TAX_INCLUDED_PRICE],
            'per_100g': detail_item[PER_100G_PRICE]
        }

        # jsonに変換してリストに追加        
        total_item.append(json.dumps(detail_item, ensure_ascii=False))

    print("total_item:", total_item)

    return total_item

    # スクリーンショット
    # browser.save_screenshot('images/' + dtstr + '.png')

if __name__ == '__main__':
    try:

        # HEADLESSブラウザに接続
        browser = webdriver.Remote(
            command_executor='http://selenium-hub:4444/wd/hub',
            desired_capabilities=DesiredCapabilities.CHROME)

        # ネットスーパー検索
        meat_list = execSearch(browser)
    finally:
        # 終了
        browser.close()
        browser.quit()

    # 取得した精肉情報をDBに格納
    # saveProduct(meat_list)
