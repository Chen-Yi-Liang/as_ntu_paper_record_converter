import math
import cv2
import numpy as np
from PaperRecord import PaperRecord

class HumidityPaperRecord(PaperRecord):
  
  paper_record = None
  
  def __init__(self, image):
    super(HumidityPaperRecord, self).__init__(image)
    self.image_to_value = None # 圖形對應到數值的轉換矩陣(2x3)
    self.value_to_image = None # 數值對應到圖形的轉換矩陣(2x3)
    self.value_region = (0, 0, 100, 25 * 60)  # 圖形的裁切區域
    
    self.image_r = 1183.637 # 估算出來氣壓表的弧線半徑
    self.image_x0 = 483. # 估算出來氣壓表 08:00 的圓弧中心 x0, y0
    self.image_y0 = 135.
    self.value_p0 = 52. # 估算出來氣壓表 08:00 的圓弧中心數值
    self.value_min0 = 0.  # 直接對應08:00
    self.dy_dmin = 85.04 / 60. # 每分鐘對應的y差值
    self.darc_dp = 0.005346 # 每個弧度對應的氣壓差值
  
  def standard(self):
    if (HumidityPaperRecord.paper_record == None):
      img = cv2.imread('../sample/temp_00.png')
      HumidityPaperRecord.paper_record = HumidityPaperRecord(img)
      print('create HumidityPaperRecord standard');
    return HumidityPaperRecord.paper_record
  
  # 過濾出紙張背景色彩
  def mask_background(self):
    img = self.src_image
    return cv2.inRange(img, np.array([0xE1, 0xE1, 0xE1]), np.array([0xFF, 0xFF, 0xFF]))
  
  # 過濾出紅色線
  def mask_red_line(self):
    img = self.src_image
    
    # 濾除 r,g,b >= 0xE1 的部分
    mask_white = self.mask_background()
    
    # 濾除 r <= 0x9F的部分
    mask_dark = cv2.inRange(img, np.array([0x00, 0x00, 0x00]), np.array([0xFF, 0xFF, 0x9F]))
    
    # 濾除 g > r & b > r 的部分
    r_cof = 1.03 #紅色比重係數
    mask_r = img[:,:,2] / r_cof
    mask_c = np.logical_and(img[:,:,1] > mask_r, img[:,:,0] > mask_r)
    mask_c = np.asarray(mask_c, dtype = "uint8") * 0xFF
    
    return cv2.bitwise_not(cv2.bitwise_or(cv2.bitwise_or(mask_white, mask_dark), mask_c))
  
  # 過濾出網格點的mask計算
  def mask_grid(self):
    return self.mask_red_line()
  
  # 過濾出文字與紀錄線的mask計算(白色表示為文字與紀錄線)
  def mask_text(self):
    mask = np.logical_not(np.logical_or(self.mask_red_line(), self.mask_background()))
    return np.asarray(mask, dtype = "uint8") * 0xFF

  # 計算兩點是否可以算是折線的連線
  def can_connect(self, p1, p2):
    dy = abs(p1[0] - p2[0])
    dx = abs(p1[1] - p2[1])
    return (dx > 0 and dx * 0.4 > dy)
    
  # 計算圖形與數值之間的彼此轉換矩陣
  def create_image_value_matrix(self):
    if self.image_matrix is None:
      self.match()
      
  # 轉換圖片上的座標到數值座標
  def value_coordiante(self, image_coordiante):
    self.create_image_value_matrix()
    v0 = self.image_matrix @ np.array([image_coordiante[0], image_coordiante[1], 1])
    dx = v0[0] - self.image_x0
    arc = math.asin(dx / self.image_r)
    p = arc / self.darc_dp + self.value_p0
    arc_dy = (1 - math.cos(arc)) * self.image_r
    dy = v0[1] - self.image_y0 - arc_dy
    min = dy / self.dy_dmin + self.value_min0
    return np.array([p, min,1])

  # 轉換數值座標到圖片上的座標
  def image_coordiante(self, value_coordiante):
    self.create_image_value_matrix()
    
    p = value_coordiante[0]
    arc = (p - self.value_p0) * self.darc_dp
    x = math.sin(arc) * self.image_r + self.image_x0

    min = value_coordiante[1]
    arc_dy = (1 - math.cos(arc)) * self.image_r
    dy = (min - self.value_min0) * self.dy_dmin
    y = dy + self.image_y0 + arc_dy
    
    return self.image_matrix_inv @ np.array([x, y, 1])
 