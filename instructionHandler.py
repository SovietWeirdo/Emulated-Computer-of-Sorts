from ROM import rom
from RAM import ram, vram
import sys

instructionHanderData = {
  "instruction": "",
  "any_flag": False,
  "jmp_flag": False,
  "mov_flag": False,
  "mov_address/mov_data": True,
  "mov_address": '0000'
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
    if instruction == "brk":
      sys.exit("BRK command found: brk is used to stop the computer")
    return address
