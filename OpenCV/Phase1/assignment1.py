import cv2

image = cv2.imread("1X6A1549.JPG")

if image is None:
    print("Image not found")

else:
    print("Image loaded successfully")
    location=input("Enter the location to save image: ")
    choice = input("do you want to save or show the image: ")
    gray= cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    if choice == "show":
        cv2.imshow("Assignment-1",gray)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    elif choice == "save":
        saved = cv2.imwrite(location,gray)
        if saved:
            print("Image saved Successfully")
        else:
            print("Cannot save Image")