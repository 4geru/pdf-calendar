Pythonで2018年のカレンダーを作ってみた
こんにちは！Python Advent Calendar 13日目担当のしげるです。
最近はPythonを利用した機械学習が流行っています。その中で機械学習したデータをpdfなどの外部ファイルに出力することができたら新しい表現方法が増えるのではないでしょうか？

## 目的
pythonでpdf形式のカレンダーを作成する。
日付と画像(URL or path)を指定するだけで、簡単にカレンダーが作れる。

<table>
<tr><td><img src='https://qiita-image-store.s3.amazonaws.com/0/64677/bb82f6d6-fab5-326f-56dd-238ce22308c4.png' width='150px'></td>
<td><img src='https://qiita-image-store.s3.amazonaws.com/0/64677/4b51136a-7150-e50d-47eb-0510271fb61d.png' width='150px'></td>
<td><img src='https://qiita-image-store.s3.amazonaws.com/0/64677/0a49c3de-fe27-4e9c-f05e-d7bdf2561d47.png' width='150px'></td>
</tr>
</table>

## 環境構築
```
 $ pip3 install reportlab # pdfを表示するライブラリ
 $ pip3 install jcal # 祝日を表示するライブラリ
 $ git clone https://github.com/4geru/pdf-calendar.git
 $ python3 make_pdf.py 2018 1 image_path
```

## 文字の表示
### 色の修正
- フォントの色の設定 HexColorと単色で色を変更できます

```python:make_pdf.py
def same_month_color(weekday):
  #ef5350 red lighten-1
  if weekday == 0: return color.HexColor("0xef5350")
  #42a5f5 blue lighten-1 
  if weekday == 6: return color.HexColor("0x42a5f5")
  return color.black
```

- フォントの変更
フォントはUnicodeCIDFont'HeiseiKakuGo-W5'を使っているが、
[TTFont](http://www.llul.info/entry/2016/11/04/python%E3%81%A7ReportLab%E3%82%92%E4%BD%BF%E3%81%A3%E3%81%9FPDF%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB%E3%81%AE%E4%BD%9C%E3%82%8A%E6%96%B9%EF%BC%88%E3%83%81%E3%83%BC%E3%83%88%E7%9A%84%E3%81%AA%EF%BC%89)を利用すると、違うフォントも使えるようです。

### 文字の描画
```python:make_pdf.py
def print_title(pdf_canvas, year, month):
  font = 'HeiseiKakuGo-W5'
  pdfmetrics.registerFont(UnicodeCIDFont(font))
  pdf_canvas.setFont(font, 20)
  pdf_canvas.drawString(config.space, config.title.height, "{0}年 {1}月のカレンダー".format(year, month))
```

## 線の描画

pdf_canvas.lineで線の描画ができます

```python:make_pdf.py
# カレンダーの線の表示
def print_box(pdf_canvas):
  pdf_canvas.setStrokeColor(color.black)
  step = config.step
  top  = config.title.height + config.image.height + config.space * 2
  width = step * 7
  height = step * 5
  left = (config.width - width)/2
  for i in range(0,8):
    x = left + step * i
    pdf_canvas.line(x , top, x, top + height)
  for i in range(0,6):
    y = top + step * i
    pdf_canvas.line(left, y, config.width - left, y)
```

## 写真の表示

pdfで画像を表示する場合は、PILを使って、画像を表示します。
PILを使っただけだと左の図になってしまう。しかし、ImageをLoadした後に、transposeで上下逆に変更することにより、右の図のように表示できる。

<table><tr><td>
<img src="https://qiita-image-store.s3.amazonaws.com/0/64677/bf354ce7-108f-1f00-3c6c-267b5703d891.png" width="200px">
</td><td>
<img src="https://qiita-image-store.s3.amazonaws.com/0/64677/122f91df-5d1a-79db-ece0-8b13bfe53f88.png" width="200px">
</td></tr></table>

```python:make_pdf.py
# 画像
def print_image(pdf_canvas, img):
  image = ''
  if img.find('http') == -1:
    image = Image.open(img).transpose(Image.FLIP_TOP_BOTTOM)
  else:
    f = io.BytesIO(urlopen(img).read())
    image = Image.open(f).transpose(Image.FLIP_TOP_BOTTOM)

  # x,y,width,height
  width = image.width * config.image.height / image.height
  height = config.image.height
  top = config.title.height + config.space
  pdf_canvas.drawInlineImage(image,config.width/2-width/2,top-height, width, height)
```

## 参考
- pdf作成  
[PythonでPDFを生成したい そしてサイコロを作りたい](http://o-tomox.hatenablog.com/entry/2013/07/22/221158)

- 画像挿入  
[pythonでReportLabを使ったPDFファイルの作り方〜その２〜 - Live the Life you Love](http://www.llul.info/entry/2016/11/07/python%E3%81%A7ReportLab%E3%82%92%E4%BD%BF%E3%81%A3%E3%81%9FPDF%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB%E3%81%AE%E4%BD%9C%E3%82%8A%E6%96%B9%E3%80%9C%E3%81%9D%E3%81%AE%EF%BC%92%E3%80%9C)
[Python + Pillow(PIL)で画像の回転を行う(rotate, transpose) - Symfoware](http://symfoware.blog68.fc2.com/blog-entry-1533.html)
