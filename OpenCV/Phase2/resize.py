import cv2

image = cv2.imread("1X6A1549.JPG") 

if image is None:
    print("Image not found")
else:
    print("Image loaded Successfully ")
    resize = cv2.resize(image,(300,300) ) #width,height 
    cv2.imshow("original",image)
    cv2.imshow("resize",resize)
    cv2.waitKey(0)
    cv2.destroyAllWindows()