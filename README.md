selenium_price
====

## Description
- ネットスーパーから商品名、価格を取得するアプリ

## Requirement
- git
- docker

## Usage

```
git clone https://github.com/uh-zz/selenium_price.git

cd selenium_price

<!-- 以下のコマンドを実行して"shared-network"があることを確認 -->
docker network ls

<!-- 上記のネットワークがなければ以下のコマンドを実行 -->
docker network create shared-network

docker-compose up -d

<!-- 鶏肉価格取得API ヨーカドー -->
curl http://localhost:5001/yokado_search -X POST -H "Content-Type: application/json" -d '{"url":"(店舗URL)"}'
<!-- 鶏肉価格取得API ライフ　-->
curl http://localhost:5001/life_search -X POST -H "Content-Type: application/json" -d '{"url":"(店舗URL)"}'
<!-- 鶏肉価格取得API イオン　-->
curl http://localhost:5001/aeon_search -X POST -H "Content-Type: application/json" -d '{"url":"(店舗URL)"}'

<!-- 店舗URL取得API -->
curl http://localhost:5001/shoplist


<!-- 例　-->
ヨーカド
curl http://localhost:5001/yokado_search -X POST -H "Content-Type: application/json" -d '{"url":"https://www.iy-net.jp/nspc/shoptop.do?shopcd=00239"}
'

イオン
curl http://localhost:5001/aeon_search -X POST -H "Content-Type: application/json" -d '{"url":"https://shop.aeon.com/netsuper/01050000060350/"}'

ライフ
curl http://localhost:5001/life_search -X POST -H "Content-Type: application/json" -d '{"url":"https://www.life-netsuper.jp/kamakuraoofunamohru/"}

```

## Author

[uh-zz](https://github.com/uh-zz)
