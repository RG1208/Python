marks = []

m1 = int(input("Enter marks of subject 1: "))
m2 = int(input("Enter marks of subject 2: "))
m3 = int(input("Enter marks of subject 3: "))
m4 = int(input("Enter marks of subject 4: "))
m5 = int(input("Enter marks of subject 5: "))
m6 = int(input("Enter marks of subject 6: "))

marks.append(m1)
marks.append(m2)
marks.append(m3)
marks.append(m4)
marks.append(m5)
marks.append(m6)

sorted_marks = marks.sort()
print("Sorted marks:", marks)