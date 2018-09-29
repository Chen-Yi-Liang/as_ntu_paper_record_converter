import math
import cv2
import numpy as np
from SolarPaperRecord import SolarPaperRecord

class SolarMediumPaperRecord(SolarPaperRecord):
  
  paper_record = None
  
  def __init__(self, image):
    super(SolarMediumPaperRecord, self).__init__(image)
    self.image_to_value = None # 圖形對應到數值的轉換矩陣(2x3)
    self.value_to_image = None # 數值對應到圖形的轉換矩陣(2x3)

    self.image_r = 0.
    self.image_x0 = 1253. # 估算出來06:00時的中心位置
    self.image_y0 = 1899.
    
    # 計算時間方向的 dot 向量
    self.min_v = (577. - 1253., 408. - 1899.)
    self.v_len = math.sqrt(self.min_v[0] * self.min_v[0] + self.min_v[1] * self.min_v[1])
    self.min_v = (self.min_v[0] / self.v_len / self.v_len * 12 * 60, \
                  self.min_v[1] / self.v_len / self.v_len * 12 * 60);
    
    # 計算燒洞方向的 dot 向量
    self.r_v = (408. - 1899., 1253. - 577.)
    self.r_v = (self.r_v[0] / self.v_len, self.r_v[1] / self.v_len);
    
    # 轉換 x,y => min,r
    self.v_matrix = np.array([ \
      [self.r_v[0], self.r_v[1], -(self.image_x0 * self.r_v[0] + self.image_y0 * self.r_v[1])], \
      [self.min_v[0], self.min_v[1], -(self.image_x0 * self.min_v[0] + self.image_y0 * self.min_v[1])], \
      [0, 0, 1]]);
    self.inv_v_matrix = np.linalg.inv(self.v_matrix)
    
    self.min_r = -88 # 容許的最小燒孔與圓心距離
    self.max_r = 48.75448697 # 容許的最大燒孔與圓心距離
    
    self.value_region = (self.min_r, 0, self.max_r, 12 * 60)  # 圖形的裁切區域
  
  def standard(self):
    if (SolarMediumPaperRecord.paper_record == None):
      img = cv2.imread('../sample/solar_medium_00.jpg')
      SolarMediumPaperRecord.paper_record = SolarMediumPaperRecord(img)
      print('create SolarMediumPaperRecord standard');
    return SolarMediumPaperRecord.paper_record
 
   # 轉換圖片上的座標到數值座標
  def value_coordiante(self, image_coordiante):
    self.create_image_value_matrix()
    if self.image_matrix is None:
      return None
    
    # 投影轉換    
    v0 = self.image_matrix @ np.array([image_coordiante[0], image_coordiante[1], 1])
    v1 = self.v_matrix @ v0
    return v1

  # 轉換數值座標到圖片上的座標
  def image_coordiante(self, value_coordiante):
    self.create_image_value_matrix()
    if self.image_matrix is None:
      return None

    v0 = self.inv_v_matrix @ np.array([value_coordiante[0], value_coordiante[1], 1])
    v1 = self.image_matrix_inv @ v0
    
    return v1
