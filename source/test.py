import cv2
import numpy as np
import matplotlib.pyplot as pyplot
from RainPaperRecord import RainPaperRecord
from PressurePaperRecord import PressurePaperRecord
from TemperaturePaperRecord import TemperaturePaperRecord
from HumidityPaperRecord import HumidityPaperRecord

# 畫出該圖的數值接受區域
def draw_value_region(p, image):
  pts = []
  pts.append(p.image_coordiante([p.value_region[0], p.value_region[1]])[0:2])
  pts.append(p.image_coordiante([p.value_region[0], p.value_region[3]])[0:2])
  pts.append(p.image_coordiante([p.value_region[2], p.value_region[3]])[0:2])
  pts.append(p.image_coordiante([p.value_region[2], p.value_region[1]])[0:2])
  cv2.polylines(image,[np.int32(pts)],True,255,1, cv2.LINE_AA)
  return image

# 在圖上 x,y 標出數值
def draw_value(p, image, x, y):
  i = p.image_coordiante([y, x])
  s = "%.2f" % y
  cv2.putText(image, s, (int(i[0]) + 10, int(i[1])), cv2.FONT_HERSHEY_SIMPLEX, 1.,(255,0,0), 1, cv2.LINE_AA)
  
# 內插計算值
def interpolation_data(c, y):
  for i in range(len(c)):
    if c[i][1] >= y:
      if i <= 0: return None
      y0 = c[i-1][1]
      y1 = c[i][1]
      x0 = c[i-1][0]
      x1 = c[i][0]
      return ((y1-y)*x0 + (y-y0)*x1)/(y1-y0)
  return None
  
# 畫出該圖的數值點
def draw_data(p, image):
  c = p.max_value_line()
  for v in c:
    i = p.image_coordiante(v)
    cv2.circle(image, (int(i[0]), int(i[1])), 1, (0, 255, 0))
    # print("%02d:%02d %f" % ((v[1]//60) + 8, v[1]%60, v[0]))
    
  for i in range(p.value_region[1], p.value_region[3], 60):
    x = interpolation_data(c, i)
    if x is None: continue
    draw_value(p, image, i, x) 
    
  return image

def show_draw_data(p, name):
  image = p.src_image.copy()
  draw_data(p, image)
  draw_value_region(p, image)
  
  out_name = "../out/" + name + "_out.png"
  cv2.imwrite(out_name, image)
  image = cv2.resize(image, (0,0), fx=0.3, fy=0.3)
  cv2.imshow(name, image)
    
def test_rain():
  rain01 = RainPaperRecord(cv2.imread('../sample/rain_01.png'))
  rain02 = RainPaperRecord(cv2.imread('../sample/rain_02.png'))
  rain03 = RainPaperRecord(cv2.imread('../sample/rain_03.png'))
  show_draw_data(rain01, 'rain_01')
  show_draw_data(rain02, 'rain_02')
  show_draw_data(rain03, 'rain_03')
  cv2.waitKey(0)
  
def test_pressure():
  #p01 = PressurePaperRecord(cv2.imread('../sample/pressure_01.png'))
  #p02 = PressurePaperRecord(cv2.imread('../sample/pressure_02.png'))
  #p03 = PressurePaperRecord(cv2.imread('../sample/pressure_03.png'))
  p04 = PressurePaperRecord(cv2.imread('../sample/pressure_04.png'))
  #show_draw_data(p01, 'pressure_01')
  #show_draw_data(p02, 'pressure_02')
  #show_draw_data(p03, 'pressure_03')
  show_draw_data(p04, 'pressure_04')
  cv2.waitKey(0)
  
def test_temperature():
  #t01 = TemperaturePaperRecord(cv2.imread('../sample/temp_01.png'))
  #t02 = TemperaturePaperRecord(cv2.imread('../sample/temp_02.png'))
  #t03 = TemperaturePaperRecord(cv2.imread('../sample/temp_03.png'))
  #t04 = TemperaturePaperRecord(cv2.imread('../sample/temp_04.png'))
  t05 = TemperaturePaperRecord(cv2.imread('../sample/temp_05.png')) 
  #show_draw_data(t01, 'temp_01')
  #show_draw_data(t02, 'temp_02')
  #show_draw_data(t03, 'temp_03')
  #show_draw_data(t04, 'temp_04')
  show_draw_data(t05, 'temp_05')
  cv2.waitKey(0)
  
def test_humidity():
  #t01 = HumidityPaperRecord(cv2.imread('../sample/temp_01.png'))
  #t02 = HumidityPaperRecord(cv2.imread('../sample/temp_02.png'))
  #t03 = HumidityPaperRecord(cv2.imread('../sample/temp_03.png'))
  #t04 = HumidityPaperRecord(cv2.imread('../sample/temp_04.png'))
  t05 = HumidityPaperRecord(cv2.imread('../sample/temp_05.png'))
  #show_draw_data(t01, 'humidity_01')
  #show_draw_data(t02, 'humidity_02')
  #show_draw_data(t03, 'humidity_03')
  #show_draw_data(t04, 'humidity_04')
  show_draw_data(t05, 'humidity_05')
  cv2.waitKey(0)
  
#test_pressure()
p = PressurePaperRecord(cv2.imread('../sample/pressure_04.png'))
img2 = p.mask_text()
img2 = cv2.resize(img2, (0,0), fx=0.5, fy=0.5)
cv2.imshow('text_image', img2)
cv2.waitKey(0)

  
'''
img = cv2.imread('../sample/rain_01.png')
#p = PressurePaperRecord(img)
p = RainPaperRecord(img)

img2 = img.copy()
c = p.max_value_line()
for v in c:
  i = p.image_coordiante(v)
  cv2.circle(img2, (int(i[0]), int(i[1])), 1, (0, 255, 0))
#img2 = p.match_image()
#img2 = p.mask_text()
img2 = cv2.resize(img2, (0,0), fx=0.3, fy=0.3)
cv2.imshow('text_image', img2)
cv2.waitKey(0)
'''
