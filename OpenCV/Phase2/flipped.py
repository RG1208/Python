import cv2

image = cv2.imread("1X6A1549.JPG") 

if image is None:
    print("Image not found")
else:
    print("Image loaded Successfully ")
    flipped = cv2.flip(image,0 ) #0,1,-1
    cv2.imshow("flipped",flipped)
    cv2.waitKey(0)
    cv2.destroyAllWindows()