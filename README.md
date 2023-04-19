# モイシランクマッチングシステム

モイシランクのマッチングシステム

## 開発環境構築

### 依存パッケージ

Docker, Docker Compose

### 手順

1. docker compose でwebサーバー(nginx), apiサーバー, dbを起動する。
2. 下記にアクセスし、API仕様書が表示されることを確認する。

http://localhost:8000/docs

3. 下記コマンドを実行し、dbのマイグレーションを行う。

`docker compose exec api python migration.py upgrade head`

4. 下記にAPIをたたき、空の配列が返ってくることを確認する。

http://localhost:8000/matching/entries
