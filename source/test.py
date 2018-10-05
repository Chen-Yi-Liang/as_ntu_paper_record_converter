import cv2
import numpy as np
import matplotlib.pyplot as pyplot
from RainPaperRecord import RainPaperRecord
from PressurePaperRecord import PressurePaperRecord
from TemperaturePaperRecord import TemperaturePaperRecord
from HumidityPaperRecord import HumidityPaperRecord
from SolarShortPaperRecord import SolarShortPaperRecord
from SolarLongPaperRecord import SolarLongPaperRecord
from SolarMediumPaperRecord import SolarMediumPaperRecord
from OldRainPaperRecord import OldRainPaperRecord
from PaperRecordTools import *
    
def test_rain():
  files = [\
    '../sample/rain_01.png',\
    '../sample/rain_02.png',\
    '../sample/rain_03.png']

  for file_name in files:
    r = RainPaperRecord(file_name)
    show_draw_data(r)

  cv2.waitKey(0)
  
def test_old_rain():
  files = [\
    '../sample/old_rain_01.jpg',\
    '../sample/old_rain_02.jpg',\
    '../sample/old_rain_03.jpg',\
    '../sample/old_rain_04.jpg',\
    '../sample/old_rain_05.jpg']
    
  for file_name in files:
    r = OldRainPaperRecord(file_name)
    show_draw_data(r)

  cv2.waitKey(0)
  
def test_pressure():
  files = [\
    '../sample/pressure_01.png',\
    '../sample/pressure_02.png',\
    '../sample/pressure_03.png',\
    '../sample/pressure_04.png'];
    
  for file_name in files:
    r = PressurePaperRecord(file_name)
    show_draw_data(r)

  cv2.waitKey(0)
  
def test_temperature():
  files = [\
    '../sample/temp_01.png',\
    '../sample/temp_02.png',\
    '../sample/temp_03.png',\
    '../sample/temp_04.png',\
    '../sample/temp_05.png'];
    
  for file_name in files:
    r = TemperaturePaperRecord(file_name)
    show_draw_data(r)

  cv2.waitKey(0)
  
def test_humidity():
  files = [\
    ['../sample/temp_01.png','humidity_01'],\
    ['../sample/temp_02.png','humidity_02'],\
    ['../sample/temp_03.png','humidity_03'],\
    ['../sample/temp_04.png','humidity_04'],\
    ['../sample/temp_05.png','humidity_05']];    
    
  for file in files:
    r = TemperaturePaperRecord(file_name = file[0], name = file[1])
    show_draw_data(r)

  cv2.waitKey(0)
  
def test_solar_short():
  files = [\
    '../sample/solar_short_01.jpg',\
    '../sample/solar_short_02.jpg',\
    '../sample/solar_short_03.jpg'];
    
  for file_name in files:
    r = SolarShortPaperRecord(file_name)
    show_draw_solar_data(r)

  cv2.waitKey(0)
  
def test_solar_long():
  files = [\
    '../sample/solar_long_01.jpg',\
    '../sample/solar_long_02.jpg'];
    
  for file_name in files:
    r = SolarLongPaperRecord(file_name)
    show_draw_data(r)

  cv2.waitKey(0)
  
def test_solar_medium():
  files = [\
    '../sample/solar_medium_01.jpg',\
    '../sample/solar_medium_02.jpg'];
    
  for file_name in files:
    r = SolarMediumPaperRecord(file_name)
    show_draw_solar_data(r)

  cv2.waitKey(0)
 
#test_old_rain() 
#test_rain()
#test_pressure()
#test_temperature()
#test_humidity()
test_solar_long()
#test_solar_medium()
#test_solar_short()

#draw_match(OldRainPaperRecord(cv2.imread('../sample/old_rain_03.jpg')), 'old_rain_03', write_image = True)
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

