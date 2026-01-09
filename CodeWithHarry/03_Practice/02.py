letter = '''
Dear <|NAME|>,
You are selected!
<|DATE|>'''

print(letter.replace("<|NAME|>", "Rachit").replace("<|DATE|>", "2026-01-09"))