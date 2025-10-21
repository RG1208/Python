import cv2

image = cv2.imread("1X6A1549.JPG") 

if image is None:
    print("Image not found")
else:
    print("Image loaded Successfully ")
    (h,w )=image.shape[:2]
    center = (1650,1370)
    color=(255,0,0)
    radius= 370
    circle =cv2.circle(image,center,radius,color,20 )
    cv2.imshow("circle",circle)
    cv2.waitKey(0)
    cv2.destroyAllWindows()