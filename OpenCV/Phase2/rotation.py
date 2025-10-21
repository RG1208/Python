import cv2

image = cv2.imread("1X6A1549.JPG") 

if image is None:
    print("Image not found")
else:
    print("Image loaded Successfully ")
    (h,w )=image.shape[:2]
    center = (w//2,h//2 )
    M= cv2.getRotationMatrix2D(center,50,1.0)
    rotated=cv2.warpAffine(image,M,(w,h))
    cv2.imshow("rotated",rotated)
    cv2.waitKey(0)
    cv2.destroyAllWindows()