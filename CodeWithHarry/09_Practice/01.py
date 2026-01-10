with open("poem.txt") as file:
    content = file.read()
    if "twinkle" in content:
        print("Twinkle is present")
    else:
        print("Twinkle is not present")