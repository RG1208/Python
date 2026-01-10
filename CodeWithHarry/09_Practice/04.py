word = "Donkey"

with open("donkey.txt", "r") as f:
    content = f.read()
print(content)
updated_content = content.replace("Donkey", "######")

with open("donkey.txt", "w") as f:
    f.write(updated_content)