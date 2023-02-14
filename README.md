# yeti
Image processing, generate animation, etc   
![yeti-1](https://user-images.githubusercontent.com/61795460/218634393-d48fac83-5b90-4ec7-9860-59b73c62a80f.png)

# 目的，できること（未実装な部分も含む全体像）
- ImageJやamiraにある不満点を解消する．
- トモグラフィ画像に関する様々なこと（アニメーション作成を含む）の処理をGUIで簡単操作する．
- タイムパフォーマンス: 無駄なファイル読み込み時間を無くす．可能な限りマルチスレッドによる高速処理を行う．
- 画像データのトレーサビリティ: 操作内容をログに保存する．
- CUI処理も可能とする．

# 現在できること
- (GUI)アニメーション作成
- (CUI)トリミング，拡張子変換

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
- メインの機能には影響がないが，exe化に伴う誤作動がいくつかある．
- [ここ](https://github.com/hokudai-paleo/yeti/releases)からyeti.zipをダウンロードする．
- フォルダの置き場所はどこでも良い．
- `yeti/dist/main.exe`をクリックして起動．
- ショートカットを作ると便利．
- ログファイルは`yeti/dist/logs`内に作られる．
- アンインストールしたいときはyetiフォルダを削除すればOK
## スクリプトからGUI実行
- `python main.py`
- 各種ライブラリのインストールが必要．
- ログファイルはリポジトリ内のLogsフォルダに保存される．
## CUI操作
```python
from imageprocess import ImageProcess as im

inputdir = r"C:\hogehoge\imagedir"
data1 = im(inputdir) # This is the general way

print(data1.filelist) # if you want to see the filelist
print(data1.nfiles) # if you want to see the number of files

outputdir = r"C:\hogehoge\outputdir"

data1.ConvertMultiImages(outputdir, "png") # You can skip "png", default=tif
data1.TrimMultiImages(500,600,700,800,50,60,outputdir, "jpg") # You can skip "jpg", default=tif
                     #(x1, x2, y1, y2, z1, z2, outputdir, outputfiletype)
```


# etymology
- パワフルな処理
- ログ（footprint）を残す
- 雪山をスキーで滑るかのようにスムースな操作性（を目指す）
- **YET** another **I**mageJ
