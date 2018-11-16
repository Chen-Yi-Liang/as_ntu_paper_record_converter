import cv2
import numpy as np
import matplotlib.pyplot as pyplot
from pathlib import Path
from RainPaperRecord import RainPaperRecord
from PressurePaperRecord import PressurePaperRecord
from TemperaturePaperRecord import TemperaturePaperRecord
from HumidityPaperRecord import HumidityPaperRecord
from SolarShortPaperRecord import SolarShortPaperRecord
from SolarLongPaperRecord import SolarLongPaperRecord
from SolarMediumPaperRecord import SolarMediumPaperRecord
from OldRainPaperRecord import OldRainPaperRecord
from PaperRecordTools import *
    
# show and draw datas
def show_draw_datas(files, paperRecord, show_image = True,
    src = None, desc = None, write_append_name = '_out.png'):
    
  for file_name in files:
    # count write_name for check is need to write file
    write_name = None
    if (desc is not None) and (src is not None) and (write_append_name is not None):
      write_name = desc / file_name.relative_to(src)
      write_name = write_name.parent / (write_name.stem + write_append_name)
      write_path = write_name.parent
      if not write_path.exists():
        write_path.mkdir(parents = True)
        
    r = paperRecord(file_name)
    show_draw_data(r, show_image = show_image, write_name = write_name)
    
  # if show image than need waitKey
  if show_image and len(files) > 0 :
    cv2.waitKey(0)
    
def test_rain():
  files = [
    '../sample/rain_01.png',
    '../sample/rain_02.png',
    '../sample/rain_03.png']
  show_draw_datas(files, RainPaperRecord)
  
def test_old_rain():
  files = [
    '../sample/old_rain_01.jpg',
    '../sample/old_rain_02.jpg',
    '../sample/old_rain_03.jpg',
    '../sample/old_rain_04.jpg',
    '../sample/old_rain_05.jpg']  
  show_draw_datas(files, OldRainPaperRecord)

def test_tainan_rain():
  src = Path('../sample/tainan')
  desc = Path('../out/tainan')
  files = list(src.rglob('SiPlu-46741_201*.jpg')) + list(src.rglob('*.png'))
  show_draw_datas(files, RainPaperRecord, show_image = True)
  
def test_pressure():
  files = [
    '../sample/pressure_01.png',
    '../sample/pressure_02.png',
    '../sample/pressure_03.png',
    '../sample/pressure_04.png'];
  show_draw_datas(files, PressurePaperRecord)
  
def test_temperature():
  files = [
    '../sample/temp_01.png',
    '../sample/temp_02.png',
    '../sample/temp_03.png',
    '../sample/temp_04.png',
    '../sample/temp_05.png'];
  show_draw_datas(files, TemperaturePaperRecord)
  
def test_humidity():
  files = [
    '../sample/temp_01.png',
    '../sample/temp_02.png',
    '../sample/temp_03.png',
    '../sample/temp_04.png',
    '../sample/temp_05.png'];
  show_draw_datas(files, HumidityPaperRecord)

def test_solar_short():
  files = [
    '../sample/solar_short_01.jpg',
    '../sample/solar_short_02.jpg',
    '../sample/solar_short_03.jpg'];
  show_draw_datas(files, SolarShortPaperRecord)
  
def test_solar_long():
  files = [
    '../sample/solar_long_01.jpg',
    '../sample/solar_long_02.jpg'];
  show_draw_datas(files, SolarLongPaperRecord)
  
def test_solar_medium():
  files = [
    '../sample/solar_medium_01.jpg',
    '../sample/solar_medium_02.jpg'];
  show_draw_datas(files, SolarMediumPaperRecord)
 
#test_tainan_rain()
#test_old_rain() 
test_rain()
#test_pressure()
#test_temperature()
#test_humidity()
#test_solar_long()
#test_solar_medium()
#test_solar_short()

#draw_match(RainPaperRecord(cv2.imread('../sample/SiPlu-46741_20020531.jpg')), 'SiPlu-46741_20020531', write_image = True)
#draw_match(PressurePaperRecord(cv2.imread('../sample/pressure_02.png')), 'pressure_02', write_image = True)
#draw_match(SolarShortPaperRecord(cv2.imread('../sample/solar_short_02.jpg')), 'solar_short_02', write_image = True)
#cv2.waitKey(0)

#write_csv(RainPaperRecord(cv2.imread('../sample/rain_02.png')), 'rain_02')
#write_csv(PressurePaperRecord(cv2.imread('../sample/pressure_02.png')), 'pressure_02')
#write_csv(TemperaturePaperRecord(cv2.imread('../sample/temp_03.png')), 'temp_03')
#write_csv(HumidityPaperRecord(cv2.imread('../sample/temp_03.png')), 'humidity_03')
#write_solar_csv(SolarLongPaperRecord(cv2.imread('../sample/solar_long_01.jpg')), 'solar_long_01')
#write_solar_csv(SolarMediumPaperRecord(cv2.imread('../sample/solar_medium_01.jpg')), 'solar_medium_01')
#write_solar_csv(SolarShortPaperRecord(cv2.imread('../sample/solar_short_01.jpg')), 'solar_short_01')

#write_mask_text(RainPaperRecord(cv2.imread('../sample/rain_02.png')), 'rain_02', write_image = True )
#write_mask_text(PressurePaperRecord(cv2.imread('../sample/pressure_02.png')), 'pressure_02', write_image = True)
#write_mask_text(TemperaturePaperRecord(cv2.imread('../sample/temp_03.png')), 'temp_03', write_image = True)
#write_mask_text(HumidityPaperRecord(cv2.imread('../sample/temp_03.png')), 'humidity_03', write_image = True)
#write_mask_text(SolarLongPaperRecord(cv2.imread('../sample/solar_long_01.jpg')), 'solar_long_01', write_image = True)
#write_mask_text(SolarMediumPaperRecord(cv2.imread('../sample/solar_medium_01.jpg')), 'solar_medium_01', write_image = True)
#write_mask_text(SolarShortPaperRecord(cv2.imread('../sample/solar_short_01.jpg')), 'solar_short_01', write_image = True)
#cv2.waitKey(0)

