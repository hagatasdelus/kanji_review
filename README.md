# クイズ型漢字復習App
## 概要
漢字をクイズ形式で復習するためのアプリケーションです。
## 特徴
- 漢字復習クイズ
- 漢字のDBへの登録・削除
- 登録漢字の検索・確認
- クイズの設定

## セットアップと起動方法
### 前提条件
- Docker
- Docker Compose

### ビルド
```
docker compose build
```
###　初回起動
```
docker compose up
```
### 再起動
```
docker compose restart
```
### 停止
```
docker compose stop
```
### 全停止(削除)
docker compose down
```
