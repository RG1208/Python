import cv2

image = cv2.imread("1X6A1549.JPG") 

if image is None:
    print("Image not found")
else:
    print("Image loaded Successfully ")
    print(image.shape)
    pt1=(3000,900) #(width,height) top,left
    pt2=(950,3000) #(width,height) bottom,right
    color=(255,0,0)
    rectangle=cv2.rectangle(image,pt1,pt2,color,50)
    cv2.imshow("rectangle",rectangle)
    cv2.waitKey(0)
    cv2.destroyAllWindows()