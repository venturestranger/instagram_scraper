import cv2
import numpy as np
import sys

age_list = [0, 4, 8, 15, 25, 38, 48, 60]
gender_list = ['M', 'F']

def display_img(image):
	cv2.imshow('Image', image)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

# Face detection using haar cascade algorithms
def haar_cascade_detect_face(file_name):
	detector = cv2.CascadeClassifier('./config/haarcascade_frontalface_default.xml')
	try:
		image = cv2.imread(file_name)
	except:
		raise Exception("No File")
	else:
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		faces = detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(5, 5))
		return image, faces

# Age and gender detection on the given set of faces
def dnn_detect_age_gender(image, faces):
	results = []
	age_net = cv2.dnn.readNet('./config/deploy_age.prototxt', './config/age_net.caffemodel')
	gender_net = cv2.dnn.readNet('./config/deploy_gender.prototxt', './config/gender_net.caffemodel')

	idx = None
	square = 0
	for i in range(len(faces)):
		(x, y, w, h) = faces[i]
		if w * h > square:
			square = w * h
			idx = i
	
	if idx != None:
		(x, y, w, h) = faces[idx]
		roi = image[y:y+h, x:x+w]
		blob = cv2.dnn.blobFromImage(roi, 1.0, (227, 227), (78.4263377603, 87.7689143744, 114.895847746), swapRB=False)

		age_net.setInput(blob)
		preds = age_net.forward()
		age = age_list[preds[0].argmax()]

		gender_net.setInput(blob)
		preds = gender_net.forward()
		gender = gender_list[preds[0].argmax()]

		return age, gender
	else:
		return -1, "N"

def face_detect(file_name):
	return dnn_detect_age_gender(*haar_cascade_detect_face(file_name))

"""
if __name__=="__main__":
	if len(sys.argv) > 1:
		print(solve(sys.argv[1]))
"""
