from ROM import rom
import sys

instructionHanderData = {
  "instruction": "",
  "any_flag": False,
  "jmp_flag": False,
  "mov_flag": False
}
def handle(address):
  tryExecute = False
  if address in rom:
    tryExecute = True
  else:
    sys.exit("address not in rom")
  print(address)
  if tryExecute and instructionHanderData["jmp_flag"] == True:
    instruction = rom[address]
    if len(instruction) == 4:
      instructionHanderData["instruction"] += str(instruction)
      instructionHanderData["instruction"] = ""
      instructionHanderData["jmp_flag"] = False
      if instructionHanderData["mov_flag"] == False:
        instructionHanderData["any_flag"] = False
      return str(instruction)
    else:
      sys.exit("ERROR: attempted to add instruction to JMP address")
    instructionHanderData["jmp_flag"] = False
  if tryExecute and instructionHanderData["any_flag"] == False:
    instruction = rom[address]
    if instruction == "nop":
      pass
    if instruction == "jmp":
      instructionHanderData["instruction"] += "jmp "
      instructionHanderData["jmp_flag"] = True
      instructionHanderData["any_flag"] = True
    if instruction == "brk":
      sys.exit("BRK command found: brk is used to stop the computer")
    return address