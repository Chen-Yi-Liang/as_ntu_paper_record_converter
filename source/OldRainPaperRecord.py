import cv2
import numpy as np
from RainPaperRecord import RainPaperRecord

class OldRainPaperRecord(RainPaperRecord):
  
  paper_record = None
  
  def __init__(self, image):
    super(OldRainPaperRecord, self).__init__(image)
    self.image_to_value = None # 圖形對應到數值的轉換矩陣(2x3)
    self.value_to_image = None # 數值對應到圖形的轉換矩陣(2x3)
    self.value_region = (0, 0, 20, 24 * 60)  # 圖形的裁切區域
    self.v_t0 = 9 # 起始時間(文字輸出用)
  
  # 過濾出網格點的mask計算
  def mask_grid(self):
    img = self.src_image
    
    # 濾除 r,g,b >= 0xE1 的部分
    mask_white = cv2.inRange(img, np.array([0xB1, 0xB1, 0xB1]), np.array([0xFF, 0xFF, 0xFF]))
    
    # 濾除 r <= 0x9F的部分
    mask_dark = cv2.inRange(img, np.array([0x00, 0x00, 0x00]), np.array([0xFF, 0xFF, 0x9F]))
    
    # 濾除 g > r & b > r 的部分
    r_cof = 1.1 #紅色比重係數
    mask_r = img[:,:,2] / r_cof
    mask_c = np.logical_and(img[:,:,1] > mask_r, img[:,:,0] > mask_r)
    mask_c = np.asarray(mask_c, dtype = "uint8") * 0xFF
    
    return cv2.bitwise_not(cv2.bitwise_or(cv2.bitwise_or(mask_white, mask_dark), mask_c))
  
  def standard(self):
    if (OldRainPaperRecord.paper_record == None):
      img = cv2.imread('../sample/old_rain_00.jpg')
      OldRainPaperRecord.paper_record = OldRainPaperRecord(img)
      print('create OldRainPaperRecord standard');
    return OldRainPaperRecord.paper_record
     
  # 計算圖形與數值之間的彼此轉換矩陣
  def create_image_value_matrix(self):
    if self.image_to_value is None:
      self.match()
      
      # m_value 為圖形轉為數值的矩陣
      # 刻度 X:0~1000(原數值0~20) Y:22*60(分鐘)
      m_value = np.array(\
      [[0, 0.033670034, -3.468013468],\
      [0.675710264, 0, -69.59815715],\
      [0, 0, 1]]);

      self.image_to_value = m_value @ self.image_matrix
      self.value_to_image = np.linalg.inv(self.image_to_value)     
      self.image_to_value = self.image_to_value[0:2]
      self.value_to_image = self.value_to_image[0:2]
      
  # 轉換圖片上的座標到數值座標
  def value_coordiante(self, image_coordiante):
    if self.image_to_value is None:
      self.create_image_value_matrix()

    return self.image_to_value @ np.array([image_coordiante[0], image_coordiante[1], 1])

  # 轉換數值座標到圖片上的座標
  def image_coordiante(self, value_coordiante):
    if self.value_to_image is None:
      self.create_image_value_matrix()

    return self.value_to_image @ np.array([value_coordiante[0], value_coordiante[1], 1])
    