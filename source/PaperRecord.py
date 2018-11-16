import cv2
import numpy as np
from pathlib import Path

class PaperRecord:
  
  # 建構式(指定圖片)
  def __init__(self, image = None, file_name = None, name = None):
    self.src_image = image  # 原始圖片
    self.file_name = file_name # 圖形的檔案名稱
    self.name = name # 圖形的名稱
        
    # 多形自動處理
    if issubclass(type(self.src_image), str):
      self.file_name = Path(self.src_image)
      self.src_image = None
    elif issubclass(type(self.src_image), Path):
      self.file_name = self.src_image
      self.src_image = None
            
    # 資料補足
    if (self.src_image is None) and (self.file_name is not None):
      self.src_image = cv2.imread(str(self.file_name))
    
    if (self.name is None) and (self.file_name is not None):
      self.name = str(self.file_name).split('.')[-2].split('/')[-1].split('\\')[-1].split(':')[-1]
      
    if (self.name is None):
      self.name = ("id:0x%0X" % id(self))
    
    self.surf_key = None   # surf輸出的Key
    self.surf_desc = None  # surf輸出的座標
    self.surf_param = 1000 # surf計算時的閥值參數
    self.match_param = 0.7 # 計算match時的閥值
    self.image_matrix = None # 圖形轉換矩陣(從此圖轉換到standard)
    self.image_matrix_inv = None # 圖形轉換矩陣(從standard轉換到此圖)
    self.value_region = (0, 0, 1, 1)  # 圖形的裁切區域
    self.v_t0 = 0 # 起始時間(文字輸出用)
    
  def standard(self):
    return None
   
  # 過濾出紙張背景色彩
  def mask_background(self):
    return None
    
  # 過濾出網格點的mask計算(白色表示為網格區域)
  def mask_grid(self):
    return None
  
  # 過濾出文字與紀錄線的mask計算(白色表示為文字與紀錄線)
  def mask_text(self):
    return None
  
  # 轉換圖片上的座標到數值座標
  def value_coordiante(self, image_coordiante):
    return None

  # 轉換數值座標到圖片上的座標
  def image_coordiante(self, value_coordiante):
    return None
    
  # 轉換text mask上有值的座標
  def text_value_coordiantes(self):
  
    mask = self.mask_text()
    coordiantes = cv2.findNonZero(mask)
    
    # 裁切出text_array中的點
    text_array = []
    for point in coordiantes:
      try:
        v = self.value_coordiante(point[0])
        if v[0] >= self.value_region[0] and v[0] < self.value_region[2]:
          if v[1] >= self.value_region[1] and v[1] < self.value_region[3]:
            text_array.append(v)
      except:
        pass
    return text_array
  
  # 計算兩點是否可以算是折線的連線
  def can_connect(self, p1, p2):
    return True
  
  # 計算最長折線
  def max_value_line(self):
    
    text_array = self.text_value_coordiantes()
    
    # 每一行y建立一個array儲存x
    yarray = []
    for i in range(self.value_region[1], self.value_region[3]):
      yarray.append([])
    
    for v in text_array:
      index = int(v[1] + 0.5)
      if (index >= self.value_region[3]):
        continue
      yarray[index].append(v[0])
    
    for i in range(self.value_region[1], self.value_region[3]):
      yarray[i].sort()
      yarray[i] = self.near_point_combine(yarray[i], 2.)
      
    result = []
    for i in range(self.value_region[1], self.value_region[3]):
      for y in yarray[i]:
        result.append([y, float(i)])
       
    # 計算最長折線
    for i in range(len(result)):
      parent_j = -1
      parent_dx = 0
      for j in range(i):
        dy = abs(result[i][0] - result[j][0])
        dx = abs(result[i][1] - result[j][1])
        if (self.can_connect(result[i], result[j])):  # 可以連續的條件
          if (parent_j == -1):
            parent_j = j
            parent_dx = dx
          elif (result[j][2] > result[parent_j][2]):
            parent_j = j
            parent_dx = dx
          elif (result[j][2] == result[parent_j][2] and dx < parent_dx):
            parent_j = j
            parent_dx = dx
      if (parent_j == -1):
        result[i].append(1)
        result[i].append(-1)
      else:
        result[i].append(1 + result[parent_j][2])
        result[i].append(parent_j)
        
    # 找出最長的摺線終點 max_i
    max_i = -1
    if (len(result) > 0):
      max_i = 0
      for i in range(1, len(result)):
        if (result[i][2] > result[max_i][2]):
          max_i = i
        
    # 抽出最長的折線
    max_p = max_i
    out_text = []
    while (max_p != -1):
      out_text.insert(0, [result[max_p][0], result[max_p][1]])
      max_p = result[max_p][3]

    return out_text
  
  # 將a中的值，相近的點值合併。
  def near_point_combine(self, a, distence):
 
    if (len(a) == 0): return []

    out = []  
    last_v = a[0]
    sum_v = last_v
    count_v = 1
    
    for i in range(1, len(a)):
      v = a[i]
      if v - last_v > distence:
        out.append(sum_v / count_v)
        last_v = v
        sum_v = last_v
        count_v = 1
      else:
        last_v = v
        sum_v += last_v
        count_v += 1
    
    out.append(sum_v / count_v)
    return out
  
  def match_gray(self):
    return cv2.cvtColor(self.src_image, cv2.COLOR_BGR2GRAY)
  
  # 過濾出網格點
  def filter_grid_gray(self):
    
    img = self.src_image
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    mask = self.mask_grid()
    if (mask is None):
      return gray
      
    return cv2.bitwise_or(gray, cv2.bitwise_not(mask))
  
  # 過濾出文字與紀錄線
  def filter_text_gray(self):

    img = self.src_image
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    mask = self.mask_text()
    if (mask is None):
      return gray
    
    return cv2.bitwise_or(gray, cv2.bitwise_not(mask))

  # 經過surf計算 key_query, desc_query
  def surf(self):
    
    if (self.surf_key is None) or (self.surf_desc is None):
      surf = cv2.xfeatures2d.SURF_create(self.surf_param)
      self.surf_key, self.surf_desc = surf.detectAndCompute(self.match_gray(), None)
    return self.surf_key, self.surf_desc
  
  # 跟standard比較計算match
  # 計算結果儲存在self.good_matches
  def match(self):
  
    if self.image_matrix_inv is not None :
      return
  
    s = self.standard()
    s.surf()
    self.surf()
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(s.surf_desc,self.surf_desc, k=2)
    
    self.good_matches = []
    for m,n in matches:
      if m.distance < self.match_param * n.distance:
        self.good_matches.append(m)
  
    # RANSAC計算最佳轉換
    good = self.good_matches
    key1 = s.surf_key
    key2 = self.surf_key
    src_pts = np.float32([ key1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
    dst_pts = np.float32([ key2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)
    self.image_matrix_inv, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
    
    if (self.image_matrix_inv is not None):
      # 移除形變項目，讓正反轉換正確
      self.image_matrix_inv[2][0] = 0.
      self.image_matrix_inv[2][1] = 0.
      # m_image 為圖形轉換的矩陣
      self.image_matrix = np.linalg.inv(self.image_matrix_inv)
    
  # 傳回兩張圖surf比對的結果
  def match_image(self):
  
    self.match()
    
    s = self.standard()
    gray1 = s.src_image.copy()
    gray2 = self.src_image.copy()
    key1 = s.surf_key
    key2 = self.surf_key
    good_list = []
    for g in self.good_matches:
      good_list.append([g])
      
    h,w,c = gray1.shape
    pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
    dst = cv2.perspectiveTransform(pts,self.image_matrix_inv)
    gray2 = cv2.polylines(gray2,[np.int32(dst)],True,255,3, cv2.LINE_AA)
    return cv2.drawMatchesKnn(gray1,key1,gray2,key2,good_list,None, flags=2)
  