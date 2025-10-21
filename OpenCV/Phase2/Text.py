import cv2

image = cv2.imread("1X6A1549.JPG") 

if image is None:
    print("Image not found")
else:
    print("Image loaded Successfully ")
    text=cv2.putText(image,"PAPA MUMMY",(1000,1000),cv2.FONT_HERSHEY_COMPLEX,10,(0,255,0),10)
   
    cv2.imshow("adding text",text)
    cv2.waitKey(0)
    cv2.destroyAllWindows()