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

curl http://localhost:5001/search -X POST -H "Content-Type: application/json" -d '{}'
```

## Author

[uh-zz](https://github.com/uh-zz)
