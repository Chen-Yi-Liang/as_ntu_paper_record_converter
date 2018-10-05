import cv2
import numpy as np
import matplotlib.pyplot as pyplot
from RainPaperRecord import RainPaperRecord
from PressurePaperRecord import PressurePaperRecord
from TemperaturePaperRecord import TemperaturePaperRecord
from HumidityPaperRecord import HumidityPaperRecord
from SolarShortPaperRecord import SolarShortPaperRecord
from SolarLongPaperRecord import SolarLongPaperRecord
from SolarMediumPaperRecord import SolarMediumPaperRecord
from OldRainPaperRecord import OldRainPaperRecord
from PaperRecordTools import *

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

# 繪製日照計的數值點
def draw_solar_data(p, image):

  # 計算出太陽燒灼點
  solar_data = p.solar_data()
  
  # 繪製出燒灼點的兩端點
  for i in range(len(solar_data)):
    v = solar_data[i]
    if v is not None:
      n = p.image_coordiante((v[0], i))
      cv2.circle(image, (int(n[0]), int(n[1])), 3, (0, 0, 255))
      n = p.image_coordiante((v[1], i))
      cv2.circle(image, (int(n[0]), int(n[1])), 3, (0, 0, 255))
      
  # 分成12個小時個別統計資料數量(當作日照時數)
  hour_sum = np.zeros(12, np.float32)
  for i in range(len(solar_data)):
    v = solar_data[i]
    if v is not None:
      hour_sum[i // 60] += 1     
  hour_sum /= 60.
  
  # 每小時顯示統計日照時數
  for i in range(12):
    n = p.image_coordiante((p.image_r + 100, i * 60. + 30.))
    s = "%.02f" % hour_sum[i]
    cv2.putText(image, s, (int(n[0]), int(n[1])), cv2.FONT_HERSHEY_SIMPLEX, 1.,(0,0,255), 1, cv2.LINE_AA)

  return image
  
def show_draw_data(p, name):
  image = p.src_image.copy()
  draw_data(p, image)
  draw_value_region(p, image)
  
  out_name = "../out/" + name + "_out.png"
  #cv2.imwrite(out_name, image)
  image = cv2.resize(image, (0,0), fx=0.3, fy=0.3)
  cv2.imshow(name, image)
    
def show_draw_solar_data(p, name):
  image = p.src_image.copy()
  draw_solar_data(p, image) 
  out_name = "../out/" + name + "_out.png"
  #cv2.imwrite(out_name, image)
  image = cv2.resize(image, (0,0), fx=0.3, fy=0.3)
  cv2.imshow(name, image)
    
def test_rain():
  files = [\
    '../sample/rain_01.png',\
    '../sample/rain_02.png',\
    '../sample/rain_03.png']

  for file_name in files:
    r = RainPaperRecord(file_name)
    show_draw_data(r, r.name)

  cv2.waitKey(0)
  
def test_old_rain():
  files = [\
    '../sample/old_rain_01.jpg',\
    '../sample/old_rain_02.jpg',\
    '../sample/old_rain_03.jpg',\
    '../sample/old_rain_04.jpg',\
    '../sample/old_rain_05.jpg']
    
  for file_name in files:
    r = OldRainPaperRecord(file_name)
    show_draw_data(r, r.name)

  cv2.waitKey(0)
  
def test_pressure():
  files = [\
    '../sample/pressure_01.png',\
    '../sample/pressure_02.png',\
    '../sample/pressure_03.png',\
    '../sample/pressure_04.png'];
    
  for file_name in files:
    r = PressurePaperRecord(file_name)
    show_draw_data(r, r.name)

  cv2.waitKey(0)
  
def test_temperature():
  files = [\
    '../sample/temp_01.png',\
    '../sample/temp_02.png',\
    '../sample/temp_03.png',\
    '../sample/temp_04.png',\
    '../sample/temp_05.png'];
    
  for file_name in files:
    r = TemperaturePaperRecord(file_name)
    show_draw_data(r, r.name)

  cv2.waitKey(0)
  
def test_humidity():
  files = [\
    ['../sample/temp_01.png','humidity_01'],\
    ['../sample/temp_02.png','humidity_02'],\
    ['../sample/temp_03.png','humidity_03'],\
    ['../sample/temp_04.png','humidity_04'],\
    ['../sample/temp_05.png','humidity_05']];    
    
  for file in files:
    r = TemperaturePaperRecord(file_name = file[0], name = file[1])
    show_draw_data(r, r.name)

  cv2.waitKey(0)
  
def test_solar_short():
  files = [\
    '../sample/solar_short_01.jpg',\
    '../sample/solar_short_02.jpg',\
    '../sample/solar_short_03.jpg'];
    
  for file_name in files:
    r = SolarShortPaperRecord(file_name)
    show_draw_solar_data(r, r.name)

  cv2.waitKey(0)
  
def test_solar_long():
  files = [\
    '../sample/solar_long_01.jpg',\
    '../sample/solar_long_02.jpg'];
    
  for file_name in files:
    r = SolarLongPaperRecord(file_name)
    show_draw_solar_data(r, r.name)

  cv2.waitKey(0)
  
def test_solar_medium():
  files = [\
    '../sample/solar_medium_01.jpg',\
    '../sample/solar_medium_02.jpg'];
    
  for file_name in files:
    r = SolarMediumPaperRecord(file_name)
    show_draw_solar_data(r, r.name)

  cv2.waitKey(0)
 
#test_old_rain() 
#test_rain()
#test_pressure()
#test_temperature()
#test_humidity()
test_solar_long()
#test_solar_medium()
#test_solar_short()

#draw_match(OldRainPaperRecord(cv2.imread('../sample/old_rain_03.jpg')), 'old_rain_03', write_image = True)
#draw_match(PressurePaperRecord(cv2.imread('../sample/pressure_02.png')), 'pressure_02', write_image = True)
#draw_match(SolarShortPaperRecord(cv2.imread('../sample/solar_short_02.jpg')), 'solar_short_02', write_image = True)
#cv2.waitKey(0)

#write_csv(RainPaperRecord(cv2.imread('../sample/rain_02.png')), 'rain_02')
#write_csv(PressurePaperRecord(cv2.imread('../sample/pressure_02.png')), 'pressure_02')
#write_csv(TemperaturePaperRecord(cv2.imread('../sample/temp_03.png')), 'temp_03')
#write_csv(HumidityPaperRecord(cv2.imread('../sample/temp_03.png')), 'humidity_03')
#write_solar_csv(SolarLongPaperRecord(cv2.imread('../sample/solar_long_01.jpg')), 'solar_long_01')
#write_solar_csv(SolarMediumPaperRecord(cv2.imread('../sample/solar_medium_01.jpg')), 'solar_medium_01')
#write_solar_csv(SolarShortPaperRecord(cv2.imread('../sample/solar_short_01.jpg')), 'solar_short_01')

#write_mask_text(RainPaperRecord(cv2.imread('../sample/rain_02.png')), 'rain_02', write_image = True )
#write_mask_text(PressurePaperRecord(cv2.imread('../sample/pressure_02.png')), 'pressure_02', write_image = True)
#write_mask_text(TemperaturePaperRecord(cv2.imread('../sample/temp_03.png')), 'temp_03', write_image = True)
#write_mask_text(HumidityPaperRecord(cv2.imread('../sample/temp_03.png')), 'humidity_03', write_image = True)
#write_mask_text(SolarLongPaperRecord(cv2.imread('../sample/solar_long_01.jpg')), 'solar_long_01', write_image = True)
#write_mask_text(SolarMediumPaperRecord(cv2.imread('../sample/solar_medium_01.jpg')), 'solar_medium_01', write_image = True)
#write_mask_text(SolarShortPaperRecord(cv2.imread('../sample/solar_short_01.jpg')), 'solar_short_01', write_image = True)
#cv2.waitKey(0)

#p = OldRainPaperRecord(cv2.imread('../sample/old_rain_03.jpg'))

#text_image = p.mask_text()
#text_image = cv2.resize(text_image, (0,0), fx=0.3, fy=0.3)
#cv2.imshow('text_image', text_image)

#grid_image = p.mask_grid()
#grid_image = cv2.resize(grid_image, (0,0), fx=0.3, fy=0.3)
#cv2.imshow('grid_image', grid_image)
 
#cv2.waitKey(0)
 
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
