import cv2

image = cv2.imread("1X6A1549.JPG") 

if image is None:
    print("Image not found")
else:
    print("Image loaded Successfully ")
    cropped= image[100:200,50:150]
    cv2.imshow("rotated cropped",cropped)
    cv2.waitKey(0)
    cv2.destroyAllWindows()