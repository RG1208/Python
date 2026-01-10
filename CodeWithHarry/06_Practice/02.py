marks1 = int(input("Enter marks 1 of student: "))
marks2 = int(input("Enter marks 2 of student: "))
marks3 = int(input("Enter marks 3 of student: "))

total_marks = marks1 + marks2 + marks3
total_percentage = (total_marks / 300) * 100

if(total_percentage >= 40 and marks1>=33 and marks2>=33 and marks3>=33):
    print("you are passed")
else:
    print("you are failed")