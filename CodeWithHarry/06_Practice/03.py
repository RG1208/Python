query=input("Enter your query: ")

p1= "lottery"
p2= "prize"
p3="buy now"
p4="click this"

if (p1 in query) or (p2 in query) or (p3 in query) or (p4 in query):
    print("This is a spam mail")
else:
    print("This is not a spam mail")