import math
import cv2
import numpy as np
from SolarPaperRecord import SolarPaperRecord

class SolarLongPaperRecord(SolarPaperRecord):
  
  paper_record = None
  
  def __init__(self, image = None, file_name = None, name = None):
    super(SolarLongPaperRecord, self).__init__(image, file_name, name)
    self.image_to_value = None # 圖形對應到數值的轉換矩陣(2x3)
    self.value_to_image = None # 數值對應到圖形的轉換矩陣(2x3)
    
    self.image_r = 1818.751407 # 估算出來氣壓表的弧線半徑
    self.image_x0 = -415.9618969 # 估算出來圓弧中心 x0, y0
    self.image_y0 = 1836.904949
    self.image_arc0 = -0.072588732 # 06:00時的弧度
    self.image_arc1 = -0.94388618 # 18:00時的弧度
    self.image_darc = (self.image_arc1 - self.image_arc0) / (12 * 60)
    self.min_r = 1784.658318 # 容許的最小燒孔與圓心距離
    self.max_r = 1892.667897 # 容許的最大燒孔與圓心距離
    
    self.value_region = (self.min_r, 0, self.max_r, 12 * 60)  # 圖形的裁切區域
    self.v_t0 = 6 # 起始時間(文字輸出用)
  
  def standard(self):
    if (SolarLongPaperRecord.paper_record == None):
      SolarLongPaperRecord.paper_record = SolarLongPaperRecord(file_name = '../sample/solar_long_00.jpg')
      print('create SolarLongPaperRecord standard');
    return SolarLongPaperRecord.paper_record
 