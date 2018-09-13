import cv2
import numpy as np
from PaperRecord import PaperRecord

class RainPaperRecord(PaperRecord):
  
  paper_record = None
  
  def __init__(self, image):
    super(RainPaperRecord, self).__init__(image)
    self.image_to_value = None # 圖形對應到數值的轉換矩陣(2x3)
    self.value_to_image = None # 數值對應到圖形的轉換矩陣(2x3)
    self.value_region = (0, 0, 20, 22 * 60)  # 圖形的裁切區域
  
  def standard(self):
    if (RainPaperRecord.paper_record == None):
      img = cv2.imread('../sample/rain_00.png')
      RainPaperRecord.paper_record = RainPaperRecord(img)
      print('create RainPaperRecord standard');
    return RainPaperRecord.paper_record
  
  # 過濾出網格點的mask計算
  def mask_grid(self):
    img = self.src_image
    
    # 濾除 r,g,b >= 0xE1 的部分
    mask_white = cv2.inRange(img, np.array([0xE1, 0xE1, 0xE1]), np.array([0xFF, 0xFF, 0xFF]))
    
    # 濾除 r <= 0x9F的部分
    mask_dark = cv2.inRange(img, np.array([0x00, 0x00, 0x00]), np.array([0xFF, 0xFF, 0x9F]))
    
    # 濾除 g > r & b > r 的部分
    r_cof = 1.1 #紅色比重係數
    mask_r = img[:,:,2] / r_cof
    mask_c = np.logical_and(img[:,:,1] > mask_r, img[:,:,0] > mask_r)
    mask_c = np.asarray(mask_c, dtype = "uint8") * 0xFF
    
    return cv2.bitwise_not(cv2.bitwise_or(cv2.bitwise_or(mask_white, mask_dark), mask_c))
  
  # 過濾出文字與紀錄線的mask計算(白色表示為文字與紀錄線)
  def mask_text(self):
  
    img = self.src_image
    
    # 濾除 r,g,b >= 0xE1 的部分
    mask_white = cv2.inRange(img, np.array([0xE1, 0xE1, 0xE1]), np.array([0xFF, 0xFF, 0xFF]))
  
    # 濾除 g > r & b > r 的部分
    mask_r = img[:,:,2]
    w, h = mask_r.shape
    mask_A0 = np.full((w, h), 0xA0)
    mask_c = np.logical_and(img[:,:,1] < mask_r, img[:,:,0] < mask_r)
    mask_c = np.logical_and(mask_c, mask_r > mask_A0)
    mask_c = np.asarray(mask_c, dtype = "uint8") * 0xFF
    return cv2.bitwise_not(cv2.bitwise_or(mask_white, mask_c))

  # 計算兩點是否可以算是折線的連線
  def can_connect(self, p1, p2):
    if (p2[1] < p1[1]):
      p = p1
      p1 = p2
      p2 = p
  
    dy = p2[0] - p1[0]
    dx = p2[1] - p1[1]

    if (dx == 0): return False
    
    if (p1[0] >= 19):
      if (p2[0] <= 1):
        return True    
    return (dy >= -dx * 0.01)
    
  # 計算圖形與數值之間的彼此轉換矩陣
  def create_image_value_matrix(self):
    if self.image_to_value is None:
      self.match()
      
      # m_value 為圖形轉為數值的矩陣
      # 刻度 X:0~1000(原數值0~20) Y:22*60(分鐘)
      m_value = np.array(\
      [[0.025348542, 0, -15.31051965],\
      [0, 0.008624069, -1.578204626],\
      [0, 0, 1]]);
      m_value[1] = m_value[1] * 60

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
    