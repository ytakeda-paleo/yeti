# yeti
Image processing, generate animation, etc

# 目的とできること（の全体像）
- トモグラフィ画像に関する様々なこと（アニメーション作成を含む）の処理をGUIで簡単操作する．
- タイムパフォーマンス: 無駄なファイル読み込み時間を無くす．可能な限りマルチスレッドによる高速処理を行う．
- 画像データのトレーサビリティ: 操作内容をログに保存する．

# 現在できること
- アニメーション作成

# 使い方
## ffmpeg
- 別途ダウンロード，PATH設定が必要．  
https://www.gyan.dev/ffmpeg/builds/
## 実行ファイルを使う方法
- [ここ](https://github.com/hokudai-paleo/yeti/releases)からzipをダウンロードする．
## スクリプトから実行
- `python main.py`


# etymology
- パワフルな処理
- ログ（footprint）を残す
- YET another ImageJ
