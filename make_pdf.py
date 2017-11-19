# -*- coding: utf-8 -*-

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib.pagesizes import letter, landscape
from datetime import date, timedelta
import reportlab.lib.colors as color
from PIL import Image
import sys

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

def make(year,month, img):
  pdf_canvas = set_info("{0:04d}-{1:02d}".format(year,month))
  print_title(pdf_canvas, year, month)
  print_image(pdf_canvas, img)
  print_box(pdf_canvas)    
  print_word(pdf_canvas, year, month)
  pdf_canvas.save()

def get_calendar(year, month):
  d = i = date(year, month, 1)
  pos = d.weekday()+1
  calendar = [[]]
  if pos != 7:
    i -= timedelta(days=pos)
    for w in range(0,pos):
      calendar[0].append(i)
      i += timedelta(days=1)
      
  while d.month >= i.month:
    last = len(calendar) - 1
    if len(calendar[last]) == 6:
      calendar[last].append(i)
      calendar.append([])
    else:
      calendar[last].append(i)
    i += timedelta(days=1)

  last = len(calendar) - 1
  if len(calendar[last]) <= 6:
    while len(calendar[last]) != 7:
      calendar[last].append(i)
      i += timedelta(days=1)
  # for w in calendar:
  #   for d in w:
  #     print(str(d), end=" | ")
  #   print()
  return calendar

def print_title(pdf_canvas, year, month):
  pdfmetrics.registerFont(UnicodeCIDFont("HeiseiKakuGo-W5"))
  pdfmetrics.registerFont(UnicodeCIDFont("HeiseiMin-W3"))
  pdf_canvas.setFont("HeiseiKakuGo-W5", 20)
  pdf_canvas.drawString(config.space, config.title.height, "{0}年 {1}月のカレンダー".format(year, month))

def diff_month_color(weekday):
  if weekday == 0:
    #ffcdd2 red lighten-4
    return color.HexColor("0xffcdd2")
  elif weekday == 6:
    #bbdefb blue lighten-4
    return color.HexColor("0xbbdefb")
  else :
    #cfd8dc blue-grey lighten-4
    return color.HexColor("0xcfd8dc")

def same_month_color(weekday):
  if weekday == 0:
    #ef5350 red lighten-1
    return color.HexColor("0xef5350")
  elif weekday == 6:
    #42a5f5 blue lighten-1
    return color.HexColor("0x42a5f5")
  else :
    return color.black

def print_word(pdf_canvas, year, month):
  # フォントを登録する
  pdfmetrics.registerFont(UnicodeCIDFont("HeiseiKakuGo-W5"))

  # ゴシック体をサイズ15で
  pdf_canvas.setFont("HeiseiKakuGo-W5", 20)
  calendar = get_calendar(year, month)

  step = config.step
  width = step * 7
  top  = config.title.height + config.image.height + config.space * 3
  left = (config.width - width)/2 + 2
  idx = 0
  for i in range(0,5):
    for j in range(0,7):
      if month == calendar[i][j].month:
        pdf_canvas.setFillColor(same_month_color(j))
      else:
        pdf_canvas.setFillColor(diff_month_color(j))        
      if calendar[i][j] == None:
        break
      pdf_canvas.drawString(j*step + left, i*step + top, str(calendar[i][j].day))
      idx += 1

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
def print_image(pdf_canvas, img):
  image = Image.open(img)
  image = image.transpose(Image.FLIP_TOP_BOTTOM)
  # x,y,width,height
  width = config.width - config.space * 2
  height = config.image.height
  top = config.title.height + config.space
  pdf_canvas.drawInlineImage(image,config.width/2-width/2,top-height, width, height)


# 初期設定
def set_info(filename):
  # print(letter) # height, width
  pdf_canvas = canvas.Canvas("./calendar/{0}.pdf".format(filename), bottomup=False, pagesize=letter)  # 原点は左上
      
  pdf_canvas.setAuthor("4geru")
  return pdf_canvas

if __name__ == '__main__':
  argv = sys.argv[1:]
  make(int(argv[0]), int(argv[1]), argv[2])