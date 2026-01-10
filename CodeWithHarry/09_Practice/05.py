list=["Lion","Donkey"]

with open("list.txt", "r") as f:
    content = f.read()
    
for word in list:
    content = content.replace(word, "######")

with open("list.txt", "w") as f:
    f.write(content)