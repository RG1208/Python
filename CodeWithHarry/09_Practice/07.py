with open("log.txt", "r") as f:
    lines= f.readlines()
    
lineno=1
for line in lines:
    if "python" in line.lower():
        print(f"Yes python is present in line number {lineno}")
        break
    lineno+=1