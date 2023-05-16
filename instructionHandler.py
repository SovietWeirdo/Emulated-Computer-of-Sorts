from ROM import rom
from RAM import ram, vram
import sys, time
from pygame import mixer

instructionHanderData = {
  "instruction": "",
  "any_flag": False,
  "jmp_flag": False,
  "mov_flag": False,
  "mov_address/mov_data": True,
  "mov_address": '0000',
  "wait_flag": False,
  "print_flag": False,
  "playaudio_flag": False,
  "audiopath": ''
}
def handle(address):
  tryExecute = False
  if address in rom:
    tryExecute = True
  else:
    sys.exit("address not in rom")
  if tryExecute and instructionHanderData["jmp_flag"] == True:
    instruction = rom[address]
    if len(instruction) == 4:
      instructionHanderData["instruction"] += str(instruction)
      instructionHanderData["instruction"] = ""
      instructionHanderData["jmp_flag"] = False
      instructionHanderData["any_flag"] = False
      goto = int(instruction, 16)
      goto -= 1
      instruction = hex(goto)
      instruction = instruction[2:6]
      instruction = instruction.upper()
      return instruction
    else:
      sys.exit("ERROR: attempted to add instruction to JMP address")
  if tryExecute and instructionHanderData["mov_flag"] == True:
    if instructionHanderData["mov_address/mov_data"] == True:
      target_address = rom[address]
      instructionHanderData["instruction"] += str(target_address) + " "
      instructionHanderData["mov_address/mov_data"] = False
      instructionHanderData["mov_address"] = str(target_address)
      return address
    else:
      data = rom[address]
      if instructionHanderData["mov_address"] in ram:
        ram[instructionHanderData["mov_address"]] = data
        instructionHanderData["mov_flag"] = False
        instructionHanderData["mov_address/mov_data"] = True
        instructionHanderData["mov_address"] = '0000'
        instructionHanderData["any_flag"] = False
        return address
      elif instructionHanderData["mov_address"] in vram:
        vram[instructionHanderData["mov_address"]] = data
        instructionHanderData["mov_flag"] = False
        instructionHanderData["mov_address/mov_data"] = True
        instructionHanderData["mov_address"] = '0000'
        instructionHanderData["any_flag"] = False
        return address
      else:
        sys.exit("ERROR: Invalid address for MOV operation")
  if tryExecute and instructionHanderData["wait_flag"] == True:
    instruction = rom[address]
    try:
      time.sleep(float(instruction))
    except:
      sys.exit("ERROR: invalid time for wait")
    instructionHanderData["any_flag"] = False
    instructionHanderData["wait_flag"] = False
    instructionHanderData["instruction"] = ''
    return address
  if tryExecute and instructionHanderData["print_flag"] == True:
    instruction = rom[address]
    print(instruction)
    instructionHanderData["instruction"] = ""
    instructionHanderData["print_flag"] = False
    instructionHanderData["any_flag"] = False
    return address
  if tryExecute and instructionHanderData["playaudio_flag"] == True:
    instructionHanderData["audiopath"] = rom[address]
    audio = mixer.Sound(instructionHanderData["audiopath"])
    audio.play()
    instructionHanderData["audiopath"] = ''
    instructionHanderData["playaudio_flag"] = False
    instructionHanderData["any_flag"] = False
    return address
  if tryExecute and instructionHanderData["any_flag"] == False:
    instruction = rom[address]
    if instruction == "nop":
      pass
    if instruction == "jmp":
      instructionHanderData["instruction"] += "jmp "
      instructionHanderData["jmp_flag"] = True
      instructionHanderData["any_flag"] = True
    if instruction == "mov":
      instructionHanderData["instruction"] += "mov "
      instructionHanderData["mov_flag"] = True
      instructionHanderData["any_flag"] = True
    if instruction == "wait":
      instructionHanderData["instruction"] += "wait "
      instructionHanderData["wait_flag"] = True
      instructionHanderData["any_flag"] = True
    if instruction == "print":
      instructionHanderData["instruction"] += "print "
      instructionHanderData["print_flag"] = True
      instructionHanderData["any_flag"] = True
    if instruction == "aplay":
      instructionHanderData["instruction"] += "play "
      instructionHanderData["playaudio_flag"] = True
      instructionHanderData["any_flag"] = True
    if instruction == "brk":
      sys.exit("BRK command found: brk is used to stop the computer")
    return address