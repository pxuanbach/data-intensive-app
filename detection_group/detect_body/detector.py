from typing import List
import cv2 

from logger import logger

   
# Initializing the HOG person 
hog = cv2.HOGDescriptor() 
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector()) 
   

def _detect(img_id, image) -> List[dict]:
    height  = image.shape[0]
    width = image.shape[1]
    # Detecting all humans 
    (humans, _) = hog.detectMultiScale(image,  
                                        winStride=(5, 5), 
                                        padding=(3, 3), 
                                        scale=1.1)
    # getting no. of human detected
    print('Human Detected : ', len(humans))
    
    data = []
    log = ""
    # Drawing the rectangle regions
    for (x, y, w, h) in humans: 
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
    logger.info(f"img_id {img_id} - Human Detected: {len(humans)}{log}")
    cv2.imwrite("detected.png", image) 
    return data
    # cv2.imwrite("detected.png", image) 
