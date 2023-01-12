import cv2

# Load the cascade

eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
# Read the input image
img = cv2.imread('eye.webp')


# Convert into grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Detect faces
eyes = eye_cascade.detectMultiScale(gray, 1.2,5)

# Draw rectangle around the faces

for (ex, ey, ew, eh) in eyes:
    cv2.rectangle(img, (ex, ey), (ex + ew, ey + eh), (255, 0, 0), 2)
    print("tọa độ x, y, w, h:", ex, ey , ew , eh)
# Display the output
cv2.imshow('img', img)
cv2.imwrite('result.jpg',img)
cv2.waitKey()
