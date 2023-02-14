# yeti
Image processing, generate animation, etc

# 目的とできること（未実装な部分も含む全体像）
- トモグラフィ画像に関する様々なこと（アニメーション作成を含む）の処理をGUIで簡単操作する．
- ImageJにある不満点を解消する．
- タイムパフォーマンス: 無駄なファイル読み込み時間を無くす．可能な限りマルチスレッドによる高速処理を行う．
- 画像データのトレーサビリティ: 操作内容をログに保存する．

# 現在できること
- アニメーション作成

# 使い方
## ffmpeg
- 別途ダウンロード，PATH設定が必要．  
https://www.gyan.dev/ffmpeg/builds/
- ffmpegフォルダをC:/直下に作り，その中にbin, doc, presetsフォルダを置く．   
```
C:\
└── ffmpeg   
        ├── bin   
        ├── doc   
        └── presets   
```
- `C:\ffmpeg\bin`, `C:\ffmpeg\doc`,`C:\ffmpeg\presets`にPATHを通す．    
https://atmarkit.itmedia.co.jp/ait/articles/1805/11/news035.html
## 実行ファイルを使う方法
- [ここ](https://github.com/hokudai-paleo/yeti/releases)からyeti.zipをダウンロードする．
- フォルダの置き場所はどこでも良い．
- ショートカット(yeti.exe)をデスクトップに置くと便利．
- アンインストールしたいときはフォルダを削除すればOK．
## スクリプトから実行
- `python main.py`


# etymology
- パワフルな処理
- ログ（footprint）を残す
- YET another ImageJ
