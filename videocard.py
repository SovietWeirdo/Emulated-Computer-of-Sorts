import pygame
from RAM import vram

card_info = {
  "loadScreenState": 0
}

def start():
  pygame.init()
  pygame.display.set_caption('Screen')
  startADDRESS = 23808
  count = 0
  for i in range(768):
    address = hex(startADDRESS)
    address = address[2:6]
    address = address.upper()
    vram[address] = 1
    startADDRESS += 1
    count += 1

def frame(display):
  vramAddress = 23807
  for y in range(24):
    for x in range(32):
      vramAddress += 1
      address = hex(vramAddress)  
      address = address[2:6]
      address = address.upper()
      if vram[address] == 1:
        pygame.draw.rect(display,(255,255,255),(x*10,y*10,(x+1)*10,(y+1)*10))
      else:
        pygame.draw.rect(display,(0,0,0),(x*10,y*10,(x+1)*10,(y+1)*10))
      pygame.display.update()

def loadScreen(display):
  if card_info["loadScreenState"] == 0:
    card_info["loadScreenState"] = 1
  else:
    card_info["loadScreenState"] = 0
  vramAddress = 23807
  for address in range(768):
    vramAddress += 1
    address = hex(vramAddress)  
    address = address[2:6]
    address = address.upper()
    vram[address] = card_info["loadScreenState"]
  frame(display)