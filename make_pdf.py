# -*- coding: utf-8 -*-

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib.pagesizes import letter, landscape
import reportlab.lib.colors as color
from PIL import Image

class Point:
    def __init__(self, width, height):
        self.width  = width
        self.height = height

class Config:
    def __init__(self):
        self.height = 792
        self.width  = 612
        self.title  = Point(0,40)
        self.image  = Point(0,300)
        self.space  = 20
        self.step   = 75

config = Config()
print(config.height)


def make(year,month):
    pdf_canvas = set_info("{0:04d}-{1:02d}".format(year,month))
    print_title(pdf_canvas,'title')
    print_image(pdf_canvas)
    print_box(pdf_canvas)    
    print_word(pdf_canvas)
    pdf_canvas.save()


# 初期設定
def set_info(filename):
    # print(letter) # height, width
    pdf_canvas = canvas.Canvas("./{0}.pdf".format(filename), bottomup=False, pagesize=letter)  # 原点は左上
        
    pdf_canvas.setAuthor("4geru")
    return pdf_canvas

def print_title(pdf_canvas,word):
    pdfmetrics.registerFont(UnicodeCIDFont("HeiseiKakuGo-W5"))
    pdfmetrics.registerFont(UnicodeCIDFont("HeiseiMin-W3"))
    pdf_canvas.setFont("HeiseiKakuGo-W5", 20)
    pdf_canvas.drawString(config.space, config.title.height, "絵日記 2017/10/06(金) 名前 : さきさか しげる")

def print_word(pdf_canvas):
    # フォントを登録する
    pdfmetrics.registerFont(UnicodeCIDFont("HeiseiKakuGo-W5"))

    # ゴシック体をサイズ15で
    pdf_canvas.setFont("HeiseiKakuGo-W5", 20)
    step = 40
    idx = 0
    arr = ['1','2','3','4','5','6','7']
    # for i in range(0,8):


def print_box(pdf_canvas):
  # 普通の線
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

# 画像
def print_image(pdf_canvas):
    image = Image.open('./img/panda.jpeg')
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    # x,y,width,height
    print(config.width - 400)
    width = config.width - config.space * 2
    height = config.image.height
    top = config.title.height + config.space
    print(letter)
    pdf_canvas.drawInlineImage(image,config.width/2-width/2,top-height, width, height)

if __name__ == '__main__':
    make(2018,1)