import cv2

# Load the cascade
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
# Read the input image
img = cv2.imread('test3.jpg')


# Convert into grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Detect faces
faces = face_cascade.detectMultiScale(gray, 1.1,4)

# Draw rectangle around the faces
for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
    print("tọa độ x, y, w, h:", x, y , w , h)
# eyes = eye_cascade.detectMultiScale(gray, 1.1, 4)
# for (ex, ey, ew, eh) in eyes:
#     cv2.rectangle(img, (ex, ey), (ex + ew, ey + eh), (255, 0, 0), 2)

# Display the output
cv2.imshow('img', img)
cv2.imwrite('result.jpg',img)
cv2.waitKey()
