# yeti
Image processing, generate animation, etc   
![yeti-1](https://user-images.githubusercontent.com/61795460/218634393-d48fac83-5b90-4ec7-9860-59b73c62a80f.png)                  
icon generated by DALL•E 2

# 目的
- ImageJやamiraにある不満点を解消する．
- トモグラフィ画像に関する様々なこと（アニメーション作成を含む）の処理をGUIで簡単操作する．
- タイムパフォーマンス: ”待ち”の時間を減らす．処理前のプレビュー機能等を実装することで，長時間処理を待たないと結果が見れない，といったことをなくす．可能な限りマルチスレッドによる高速処理を行う．
- トレーサブルな画像処理: 操作内容をログに保存する．（さらには，画像ファイルタグにログを埋め込みたい）
- CUI処理も可能とする．

# 現在できること
- (GUI: exeファイルあるいはスクリプトから実行)アニメーション作成
![image](https://user-images.githubusercontent.com/61795460/218638281-c3ef9bec-6786-4842-b73f-a55437ac672b.png)
- (CUI)トリミング，拡張子変換のマルチスレッド処理を数行で実行する
![image](https://user-images.githubusercontent.com/61795460/218956300-bf3ef4b9-5e0c-40a8-b5b4-306ef1bb297b.png)

# 使い方
## ffmpeg
- 以下からダウンロードする．  
https://www.gyan.dev/ffmpeg/builds/
- ffmpegフォルダをC:/直下に作り，その中にbin, doc, presetsフォルダを置く．   
```
C:\
└── ffmpeg   
        ├── bin   
        ├── doc   
        └── presets   
```
- `C:\ffmpeg\bin`にPATHを通す．    
https://atmarkit.itmedia.co.jp/ait/articles/1805/11/news035.html
## 実行ファイルを使う方法
- [ここ](https://github.com/ytakeda-paleo/yeti/releases)から最新版の`yeti.zip`をダウンロードする．
- フォルダの置き場所はどこでも良い．
- `yeti/dist/main/yeti.exe`をクリックして起動．
- `yeti.exe`を`main`フォルダから移動するとアプリは動かなくなる．ショートカットを作成することで対応してほしい．
- ログファイルは`yeti/dist/main/logs`内に作られる．
- アンインストールしたいときはyetiフォルダを削除すればOK
## スクリプトからGUI実行
- `git clone https://github.com/ytakeda-paleo/yeti.git`
- `python main.py`
- 各種ライブラリのインストールが必要．
- ログファイルはリポジトリ内のlogsフォルダに保存される．
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

# Known issues and things to be fixed
- ファイル選択時にクリックした画像から画像情報を取得する．`initial image info` >> `clicked image info`
- ffmpegをzipに含める．
        - ライセンスの問題？      
- Mac版を作る？

# feedbacks(thanks!)
- トリミングでは画像上に矩形をドラッグできてほしい
- logは入力フォルダ内に残せるようにしてほしい（選択できるようにする）
- アニメーションのナンバリングは番号だけもありえる
# For coders
- exe-fication: `pyinstaller main.py --noconsole -i .\icon.ico -n yeti`
- ffmpegとtkinterに関するtips: https://qiita.com/ytakeda-paleo/items/c3d33aef9d1c715702de
