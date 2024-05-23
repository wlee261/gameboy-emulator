import json

from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class Operand:

    immediate: bool
    name: str
    bytes: int
    value: int | None
    adjust: Literal["+", "-"] | None

    def create(self, value):
        return Operand(immediate=self.immediate,
                       name=self.name,
                       bytes=self.bytes,
                       value=value,
                       adjust=self.adjust)


@dataclass
class Instruction:

    opcode: int
    immediate: bool
    operands: list[Operand]
    cycles: list[int]
    bytes: int
    mnemonic: str
    comment: str = ""

    def create(self, operands):
        return Instruction(opcode=self.opcode,
                           immediate=self.immediate,
                           operands=operands,
                           cycles=self.cycles,
                           bytes=self.bytes,
                           mnemonic=self.mnemonic)


with open('opcodes.json', 'r') as file:
    json_data = json.load(file)


def parseOperands(operands: list[Operand]):
    parsedOperands = []
    for operand in operands:
        parsedOperands.append(Operand(immediate=operand.get('immedate'), name=operand.get(
            'name'), bytes=operand.get('bytes'), value=operand.get('value'), adjust=operand.get('adjust')))
    return parsedOperands


# two sets of instructions -> cbprefixed and unprefixed
unprefixed = json_data["unprefixed"]
cbprefixed = json_data["cbprefixed"]

unprefixed_instructions = {}
cbprefixed_instructions = {}

for opcode, instruction in unprefixed.items():
    operands = instruction["operands"]
    parsedOperands = parseOperands(operands)
    unprefixed_instructions[int(opcode, 16)] = Instruction(opcode=instruction.get('opcode'), mnemonic=instruction.get('mnemonic'), bytes=instruction.get(
        'bytes'), cycles=instruction.get('cycles'), operands=parsedOperands, immediate=instruction.get('immediate'), comment=instruction.get('comment'))

for opcode, instruction in cbprefixed.items():
    operands = instruction["operands"]
    parsedOperands = parseOperands(operands)
    cbprefixed_instructions[int(opcode, 16)] = Instruction(opcode=instruction.get('opcode'), mnemonic=instruction.get('mnemonic'), bytes=instruction.get(
        'bytes'), cycles=instruction.get('cycles'), operands=parsedOperands, immediate=instruction.get('immediate'), comment=instruction.get('comment'))

# for key, value in unprefixed_instructions.items():
#     print(key, value, '\n')

print(unprefixed_instructions[0xff])
