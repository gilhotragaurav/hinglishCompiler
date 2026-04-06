import re

# Token patterns
token_specification = [
    ('KEYWORD', r'\b(bolo|agar|warna|jabtak)\b'),
    ('NUMBER', r'\b\d+\b'),
    ('STRING', r'\".*?\"'),
    ('IDENTIFIER', r'\b[a-zA-Z_]\w*\b'),
    ('OPERATOR', r'[+\-*/><=]+'),
    ('NEWLINE', r'\n'),
    ('SKIP', r'[ \t]+'),
]

def tokenize(code):
    tokens = []
    for line in code.split("\n"):
        for token_type, pattern in token_specification:
            matches = re.findall(pattern, line)
            for match in matches:
                tokens.append((token_type, match))
    return tokens