import cv2

image = cv2.imread("1X6A1549.JPG") 

if image is None:
    print("Image not found")
else:
    print("Image loaded Successfully ")
    print(image.shape)
    pt1=(100,5000)
    pt2=(200,2500)
    color=(255,0,0)
    line=cv2.line(image,pt1,pt2,color,50)
    cv2.imshow("line",line)
    cv2.waitKey(0)
    cv2.destroyAllWindows()