from __future__ import annotations

from enum import Enum
from string import ascii_letters
from collections import deque

nameble = ascii_letters + "-_"


class Token:
    type: TokenType
    value: str

    def __init__(self, type: str, value: str = "") -> None:
        self.type = type
        self.value = value
    
    def __repr__(self) -> str:
        value = f'"{self.value}"' if self.value else ''

        return f"{self.type}({value})"


class TokenType(Enum):
    LEFT_BRACKET = 0
    RIGHT_BRACKET = 1
    SLASH = 2
    VALUE_STRING = 3
    STRING = 4
    NAME = 5
    EQUAL = 6
    COLON = 7


class Tokenizer:
    def tokenize(self, text: str) -> deque[Token]:
        i = 0
        tokens = deque()

        while i < len(text):
            symbol = text[i]

            if symbol == "<":
                tokens.append(Token(TokenType.LEFT_BRACKET))
            elif symbol == ">":
                tokens.append(Token(TokenType.RIGHT_BRACKET))
            elif symbol == "/":
                tokens.append(Token(TokenType.SLASH))
            elif symbol in "'\"" or symbol == "v" and text[i + 1] in "'\"":                      
                if symbol == "v":
                    j = i + 2
                else:
                    j = i + 1

                string = ""
                next_symbol = text[j]
                quote_symbol = text[j - 1]

                while next_symbol != quote_symbol:
                    string += next_symbol

                    j += 1
                    next_symbol = text[j]

                i = j
                
                if symbol == "v":
                    tokens.append(Token(TokenType.VALUE_STRING, string))
                else:
                    tokens.append(Token(TokenType.STRING, string))
            elif symbol in nameble:
                j = i + 1
                string = symbol
                next_symbol = text[j]
                
                while next_symbol in nameble:
                    string += next_symbol

                    j += 1
                    next_symbol = text[j]

                i = j - 1

                tokens.append(Token(TokenType.NAME, string))
            elif symbol == "=":
                tokens.append(Token(TokenType.EQUAL))
            elif symbol == ":":
                tokens.append(Token(TokenType.COLON))

            i += 1

        return tokens
