# モイシランクマッチングシステム

モイシランクのマッチングシステム

https://www.figma.com/file/lKdUgm3Tg9SqqlDGFNhFeL/%E3%83%A6%E3%83%BC%E3%82%B6%E3%83%BC%E3%82%B3%E3%83%9F%E3%83%A5%E3%83%8B%E3%83%86%E3%82%A3%E3%81%AE%E3%83%9E%E3%83%83%E3%83%81%E3%83%A1%E3%82%A4%E3%82%AD%E3%83%B3%E3%82%B0%E3%82%B7%E3%82%B9%E3%83%86%E3%83%A0?type=whiteboard&node-id=0-1&t=lN6JcrF3xmjDp4kp-0

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
