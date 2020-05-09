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

docker-compose up -d

# 鶏肉価格取得API
curl http://localhost:5001/search -X POST -H "Content-Type: application/json" -d '{}'

# 店舗URL取得API
curl http://localhost:5001/shoplist

```

## Author

[uh-zz](https://github.com/uh-zz)
