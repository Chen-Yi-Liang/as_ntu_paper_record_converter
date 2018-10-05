import math
import cv2
import numpy as np
from SolarPaperRecord import SolarPaperRecord

class SolarShortPaperRecord(SolarPaperRecord):
  
  paper_record = None
  
  def __init__(self, image = None, file_name = None, name = None):
    super(SolarShortPaperRecord, self).__init__(image, file_name, name)
    self.image_to_value = None # 圖形對應到數值的轉換矩陣(2x3)
    self.value_to_image = None # 數值對應到圖形的轉換矩陣(2x3)
    
    self.image_r = 1839.405597 # 估算出來氣壓表的弧線半徑
    self.image_x0 = -1220.778387 # 估算出來圓弧中心 x0, y0
    self.image_y0 = 733.3035731
    self.image_arc0 = 0.577829514 # 06:00時的弧度
    self.image_arc1 = -0.279984979 # 18:00時的弧度
    self.image_darc = (self.image_arc1 - self.image_arc0) / (12 * 60)
    self.min_r = 1788.921004 # 容許的最小燒孔與圓心距離
    self.max_r = 1881.141387 # 容許的最大燒孔與圓心距離
    
    self.value_region = (self.min_r, 0, self.max_r, 12 * 60)  # 圖形的裁切區域
    self.v_t0 = 6 # 起始時間(文字輸出用)
  
  def standard(self):
    if (SolarShortPaperRecord.paper_record == None):
      SolarShortPaperRecord.paper_record = SolarShortPaperRecord(file_name = '../sample/solar_short_00.jpg')
      print('create SolarShortPaperRecord standard');
    return SolarShortPaperRecord.paper_record
 