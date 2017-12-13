# -*- coding: utf-8 -*-

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib.pagesizes import letter, landscape
from datetime import date, timedelta
from urllib.request import urlopen
from PIL import Image
import reportlab.lib.colors as color
import jcal
import sys
import io

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
      
  while d.month == i.month:
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
  font = 'HeiseiKakuGo-W5'
  pdfmetrics.registerFont(UnicodeCIDFont(font))
  pdf_canvas.setFont(font, 20)
  pdf_canvas.drawString(config.space, config.title.height, "{0}年 {1}月のカレンダー".format(year, month))

def diff_month_color(day):
  #ffcdd2 red lighten-4
  if day.weekday() == 6: return color.HexColor("0xffcdd2")
  #bbdefb blue lighten-4 
  if day.weekday() == 5: return color.HexColor("0xbbdefb")
  # holiday #ef5350 red lighten-1
  if day in jcal.holiday(day.year): return color.HexColor("0xffcdd2")
  # transfer holiday on monday #ffcdd2 red lighten-4
  if (  day - timedelta(days=2) in jcal.holiday(day.year) or \
        day - timedelta(days=1) in jcal.holiday(day.year) ) and \
      day.weekday() == 0:
    return color.HexColor("0xffcdd2")
  # transfer holiday on tuesday #ffcdd2 red lighten-4
  if  day - timedelta(days=2) in jcal.holiday(day.year) and \
      day - timedelta(days=1) in jcal.holiday(day.year) and \
      day.weekday() == 1:
    return color.HexColor("0xffcdd2")
  #cfd8dc blue-grey lighten-4
  return color.HexColor("0xcfd8dc")   

def same_month_color(day):
  # sunday #ef5350 red lighten-1
  if day.weekday() == 6: return color.HexColor("0xef5350")
  # saturday #42a5f5 blue lighten-1 
  if day.weekday() == 5: return color.HexColor("0x42a5f5")
  # holiday #ef5350 red lighten-1
  if day in jcal.holiday(day.year): return color.HexColor("0xef5350")
  # transfer holiday on monday #ef5350 red lighten-1
  if (  day - timedelta(days=2) in jcal.holiday(day.year) or \
        day - timedelta(days=1) in jcal.holiday(day.year) ) and \
      day.weekday() == 0:
    return color.HexColor("0xef5350")
  # transfer holiday on tuesday #ef5350 red lighten-1
  if  day - timedelta(days=2) in jcal.holiday(day.year) and \
      day - timedelta(days=1) in jcal.holiday(day.year) and \
      day.weekday() == 1:
    return color.HexColor("0xef5350")
  return color.black

# カレンダーの日付を表示
def print_word(pdf_canvas, year, month):
  # # フォントを登録する
  pdfmetrics.registerFont(UnicodeCIDFont("HeiseiKakuGo-W5"))
  # ゴシック体をサイズ15で
  pdf_canvas.setFont("HeiseiKakuGo-W5", 20)
  calendar = get_calendar(year, month)

  step = config.step
  width = step * 7
  top  = config.title.height + config.image.height + config.space * 3
  left = (config.width - width)/2 + 2
  for i in range(0,5):
    for j in range(0,7):
      if month == calendar[i][j].month:
        pdf_canvas.setFillColor(same_month_color(calendar[i][j]))
      else:
        pdf_canvas.setFillColor(diff_month_color(calendar[i][j])) 
      pdf_canvas.drawString(j*step + left, i*step + top, str(calendar[i][j].day))

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

# 初期設定
def set_info(filename):
  # print(letter) # height, width
  pdf_canvas = canvas.Canvas("./calendar/{0}.pdf".format(filename), bottomup=False, pagesize=letter)  # 原点は左上
      
  pdf_canvas.setAuthor("4geru")
  pdf_canvas.setTitle(filename)
  pdf_canvas.setSubject(filename + 'のカレンダー')

  return pdf_canvas

if __name__ == '__main__':
  argv = sys.argv[1:]
  make(int(argv[0]), int(argv[1]), argv[2])