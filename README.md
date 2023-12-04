# モイシランクマッチングシステム

モイシランクのマッチングシステム

## 開発環境構築

### 依存パッケージ

Python3, Docker, Docker Compose, npm, openssl

### 手順

1. オレオレ証明書を作る
   - `./dev/make_ssl_certification.sh`を叩く。
1. docker compose でwebサーバー(nginx), apiサーバー, dbを起動する。
2. 下記にアクセスし、API仕様書が表示されることを確認する。

https://localhost/docs

3. 下記コマンドを実行し、dbのマイグレーションを行う。

`docker compose exec api python migration.py upgrade head`

4. 下記にAPIをたたき、空の配列が返ってくることを確認する。

http://localhost:8080/matching/entries
