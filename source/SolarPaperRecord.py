import math
import cv2
import numpy as np
from PaperRecord import PaperRecord

class SolarPaperRecord(PaperRecord):
  
  def __init__(self, image = None, file_name = None, name = None):
    super(SolarPaperRecord, self).__init__(image, file_name, name)
    self.image_to_value = None # 圖形對應到數值的轉換矩陣(2x3)
    self.value_to_image = None # 數值對應到圖形的轉換矩陣(2x3)
    
    self.image_r = None # 估算出來氣壓表的弧線半徑
    self.image_x0 = None # 估算出來圓弧中心 x0, y0
    self.image_y0 = None
    self.image_arc0 = None # 06:00時的弧度
    self.image_arc1 = None # 18:00時的弧度
    self.image_darc = None
    self.min_r = None # 容許的最小燒孔與圓心距離
    self.max_r = None # 容許的最大燒孔與圓心距離
    
    self.value_region = None  # 圖形的裁切區域
  
  def standard(self):
    return None
  
  # 過濾出藍色與白色的區域
  def mask_blue_white(self):
    img = self.src_image
    # 濾除 g > r & b > r 的部分
    mask_r = img[:,:,2]
    mask_g = img[:,:,1]
    mask_b = img[:,:,0]
    mask_blue = np.logical_and(mask_b >  0x40, mask_b > mask_r * 1.2)
    mask_blue = np.asarray(mask_blue, dtype = "uint8") * 0xFF
    
    mask_white = cv2.inRange(img, np.array([0xB0, 0xB0, 0xB0]), np.array([0xFF, 0xFF, 0xFF]))

    return mask_blue | mask_white
  
  # 過濾出邊緣以外的區域
  def mask_not_text(self):
    bw = self.mask_blue_white()
    h,w = bw.shape[:2]
    # 從色個角落填滿，避免遺漏
    cv2.floodFill(bw, None, (0,0), 255)
    cv2.floodFill(bw, None, (0,h-5), 255)
    cv2.floodFill(bw, None, (w-5,0), 255)
    cv2.floodFill(bw, None, (w-5,h-5), 255)
    return bw
  
  # 過濾出文字與紀錄線的mask計算(白色表示為文字與紀錄線)
  def mask_text(self):
    return cv2.bitwise_not(self.mask_not_text())

  # 計算輸出太陽的資料
  def solar_data(self):
    text_array = self.text_value_coordiantes()
    
    yarray = []
    for i in range(12 * 60):
      yarray.append(None)
    
    for v in text_array:
      x = int(v[1])
      y = v[0]
      if yarray[x] is None:
        yarray[x] = (y, y)
      else:
        max_y = max(yarray[x][0], y)
        min_y = min(yarray[x][1], y)
        yarray[x] = (max_y,min_y)
      
    # 資料點的中心R應該要接近，檢查找出差異太大的
    avg_v = 0.
    c = 0
    for v in yarray:
      if v is not None:
        avg_v += v[0]
        avg_v += v[1]
        c += 2
    if c != 0:
      avg_v /= c
    
    # 刪除可能錯誤的點
    for i in range(len(yarray)):
      v = yarray[i]
      if v is not None:
        if abs((v[0] + v[1]) / 2 - avg_v) > 50:
          # 刪除偏離avg太遠的
          yarray[i] = None
        elif v[0] - v[1] < 2:
          # 刪除長度太小的點(視為雜訊)
          yarray[i] = None
    
    return yarray
    
  # 計算圖形與數值之間的彼此轉換矩陣
  def create_image_value_matrix(self):
    if self.image_matrix is None:
      self.match()
      
  # 轉換圖片上的座標到數值座標
  def value_coordiante(self, image_coordiante):
    self.create_image_value_matrix()
    if self.image_matrix is None:
      return None
    
    # 投影轉換    
    v0 = self.image_matrix @ np.array([image_coordiante[0], image_coordiante[1], 1])
    
    dx = v0[0] - self.image_x0
    dy = v0[1] - self.image_y0
    
    r = math.sqrt(dx * dx + dy * dy)
    arc = math.atan2(dy, dx)
    min = (arc - self.image_arc0) / self.image_darc
    return np.array([r, min,1])

  # 轉換數值座標到圖片上的座標
  def image_coordiante(self, value_coordiante):
    self.create_image_value_matrix()
    if self.image_matrix is None:
      return None
    
    r = value_coordiante[0]
    min = value_coordiante[1]
    arc = (min * self.image_darc) + self.image_arc0
    x = r * math.cos(arc) + self.image_x0
    y = r * math.sin(arc) + self.image_y0
    
    return self.image_matrix_inv @ np.array([x, y, 1])
 