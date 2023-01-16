import cv2 

   
# Initializing the HOG person 
hog = cv2.HOGDescriptor() 
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector()) 
   

def _detect(image):
    # Detecting all humans 
    (humans, _) = hog.detectMultiScale(image,  
                                        winStride=(5, 5), 
                                        padding=(3, 3), 
                                        scale=1.1)
    # getting no. of human detected
    print('Human Detected : ', len(humans))
    
    # Drawing the rectangle regions
    for (x, y, w, h) in humans: 
        cv2.rectangle(image, (x, y),  
                  (x + w, y + h),  
                  (0, 0, 255), 2) 
        print("tọa độ x, y, w, h:", x, y , w , h)
    cv2.imwrite("detected.png", image) 
