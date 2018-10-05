import cv2
import numpy as np
import matplotlib.pyplot as pyplot
from SolarPaperRecord import SolarPaperRecord

# 繪製一般輸出結果
def show_draw_data(p, show_image = True, write_image = False):
  if issubclass(type(p), SolarPaperRecord):
    show_draw_solar_data(p, show_image, write_image)
  else:
    show_draw_normal_data(p, show_image, write_image)

# 繪製除日照圖以外輸出結果
def show_draw_normal_data(p, show_image = True, write_image = False):
  image = p.src_image.copy()
  draw_data(p, image)
  draw_value_region(p, image)
  
  if write_image:
    out_name = "../out/" + p.name + "_out.png"
    cv2.imwrite(out_name, image)
    
  if show_image:
    image = cv2.resize(image, (0,0), fx=0.3, fy=0.3)
    cv2.imshow(p.name, image)
    
# 繪製日照計圖輸出結果
def show_draw_solar_data(p, show_image = True, write_image = False):
  image = p.src_image.copy()
  draw_solar_data(p, image) 
  
  if write_image:
    out_name = "../out/" + p.name + "_out.png"
    cv2.imwrite(out_name, image)
  
  if show_image:
    image = cv2.resize(image, (0,0), fx=0.3, fy=0.3)
    cv2.imshow(p.name, image)

# 繪製圖形比對的match結果圖
def draw_match(paperRecord, name, show_image = True, write_image = False):

  match_image = paperRecord.match_image()

  if write_image:
    out_name = "../out/" + name + "_match_out.png"
    cv2.imwrite(out_name, match_image)
  
  if show_image:
    match_image = cv2.resize(match_image, (0,0), fx=0.3, fy=0.3)
    cv2.imshow(name + '_match', match_image)

# 輸出數值結果到檔案
def write_csv(paperRecord, name):
  out_name = "../out/" + name + "_out.csv"
  file = open(out_name, "w+")
  values = paperRecord.max_value_line()
  for v in values:
    file.write("%02d:%02d,%f\n" % ((v[1]//60) + paperRecord.v_t0, v[1]%60, v[0]))
  file.close()

# 輸出日照計數值結果到檔案
def write_solar_csv(paperRecord, name):
  out_name = "../out/" + name + "_out.csv"
  file = open(out_name, "w+")
  # 計算出太陽燒灼點
  solar_data = paperRecord.solar_data()
  
  # 繪製出燒灼點的兩端點
  for i in range(len(solar_data)):
    v = solar_data[i]
    if v is not None:
      file.write("%02d:%02d,%f\n" % ((i//60) + paperRecord.v_t0, i%60, v[0] - v[1]))
  file.close()

# 繪製過濾出文字部分
def write_mask_text(paperRecord, name, show_image = True, write_image = False):
  mask_text = paperRecord.mask_text()
  mask_text = cv2.bitwise_not(mask_text)

  if write_image:
    out_name = "../out/" + name + "_text_out.png"
    cv2.imwrite(out_name, mask_text)
  
  if show_image:
    mask_text = cv2.resize(mask_text, (0,0), fx=0.3, fy=0.3)
    cv2.imshow(name + '_text', mask_text)

#
# 以下為private functions
#

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
