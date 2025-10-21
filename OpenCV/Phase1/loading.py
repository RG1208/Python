import cv2

image = cv2.imread("1X6A1549.JPG") #function to load an image

if image is None:
    print("ERROR: Image not found")
else:
    print("Image loaded successfully")
    shape=image.shape
    print(shape)
    gray= cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imshow("Window",gray) #function to show image
    cv2.waitKey(0) #function to keep image until any key is pressed
    cv2.destroyAllWindows() #function to destroy opened image window
    
    cv2.imshow("Window",image) #function to show image
    cv2.waitKey(0) #function to keep image until any key is pressed
    cv2.destroyAllWindows() #function to destroy opened image window
    saved=cv2.imwrite("Output.jpg",image ) #function to save an image
    if saved:
        print("image saved successfully")
    else:
        print("couldnot save image")
    
