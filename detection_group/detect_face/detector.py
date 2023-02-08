from typing import List
import cv2 

from logger import logger

# Load the cascade
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
   
# Initializing the HOG person 
hog = cv2.HOGDescriptor() 
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector()) 
   

def _detect(img_id, image) -> List[dict]:
    height  = image.shape[0]
    width = image.shape[1]
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.1,4)

    # getting no. of face detected
    print('Face Detected : ', len(faces))
    
    data = []
    log = ""
    # Drawing the rectangle regions
    for (x, y, w, h) in faces: 
        cv2.rectangle(image, (x, y),  
                  (x + w, y + h),  
                  (0, 0, 255), 2) 
        log = log + f" - position x={x}, y={y}, w={w}, h={h}"
        data.append({
            "x": float(x),
            "y": float(y),
            "width_of_obj": float(w),
            "height_of_obj": float(h),
            "width_of_img": float(width),
            "height_of_img": float(height),
        })
    logger.info(f"img_id {img_id} - Face Detected: {len(faces)}{log}")
    # cv2.imwrite("detected.png", image) 
    return data
    # cv2.imwrite("detected.png", image) 
