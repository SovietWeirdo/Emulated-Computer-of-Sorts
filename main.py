from ROM import rom
from RAM import vram, ram
import videocard
import pygame
DISPLAYSURF = pygame.display.set_mode((320,240))
pygame.display.set_caption("SovietEmulated")
import time
import sys
import instructionHandler

videocard.start()
videocard.frame(DISPLAYSURF)

def sys_loop():
  # to start at address 8000 put the PC at 32767
  programCounter = 32765
  while True:
    time.sleep(0)
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
    pygame.display.update()
    programCounter += 1
    programAddress = hex(programCounter)
    programAddress = programAddress[2:6]
    programAddress = programAddress.upper()
    programAddress = instructionHandler.handle(programAddress)
    programCounter = int(programAddress,16)
    if programAddress == 'FFFF':
      sys.exit("Tried to access memory out of the 0000-FFFF range")
    #videocard.loadScreen(DISPLAYSURF)
    videocard.frame(DISPLAYSURF)

if __name__ == '__main__':
  sys_loop()