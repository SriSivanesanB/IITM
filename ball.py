import cv2
import argparse
import collections
import imutils
arg = argparse.ArgumentParser()
arg.add_argument("-v", "--video")
args = vars(arg.parse_args())
v = cv2.VideoCapture(args["video"])
ballbottom = (29, 86, 6)
balltop = (64, 255, 255)
path = collections.deque(maxlen=10) 
while True:
	frm = v.read()
	frm = frm[1] 
	if frm is None:
		break
	frm = imutils.resize(frm, width=800)
	blur = cv2.GaussianBlur(frm, (11, 11), 0)
	h = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
	filter = cv2.inRange(h, ballbottom, balltop)
	filter = cv2.erode(filter, None, iterations=2)
	filter = cv2.dilate(filter, None, iterations=2)
	c = cv2.findContours(filter.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
	c = imutils.grab_contours(c)
	center = None
	if len(c) > 0:
		cen = max(c, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(cen)
		M = cv2.moments(cen)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
		if radius > 10:
			cv2.circle(frm, center, 5, (0, 0, 0), -1)
	path.appendleft(center)
	for i in range(1, len(path)):
		if path[i - 1] is None or path[i] is None:
			continue
		cv2.line(frm, path[i - 1], path[i], (255,255,255), 2)
	cv2.imshow("Ball Track", frm)
	key = cv2.waitKey(1) & 0xFF
	if key == ord("0"):
		break
cv2.destroyAllWindows()