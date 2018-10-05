import cv2
import numpy as np
import matplotlib.pyplot as pyplot

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
  