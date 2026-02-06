from secrets import token_hex

from src.links.interfaces import CodeGeneratorPort


class CodeGenerator(CodeGeneratorPort):
    def __init__(self):
        self.len = 5

    def generate(self):
        return token_hex(self.len)
