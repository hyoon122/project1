import cv2
import numpy as np

#space = np.zeros((500, 1000), dtype = np.uint8)
space = np.zeros((768, 1380), dtype = np.uint8)

line_color = 255
color = 255

#space = cv2.line(space, (100, 100), (800, 400), line_color, 3, 1)
#space2 = cv2.circle(space, (600, 200), 100, color, 4, 1)
#space3 = cv2.rectangle(space, (500, 200), (800, 400), color, 5, 1)
#space4 = cv2.ellipse(space, (200, 100), (400, 200), 0, 45, 250, color, 4)

obj1 = np.array([[300,500], [500, 500], [400, 600], [200, 600]])
obj2 = np.array([[600,500], [800, 500], [700, 600], [900, 600]])
space5 = cv2.polylines(space, [obj1], True, color, 3)
space5 = cv2.fillPoly(space, [obj2], color, 1)

#print(space.shape)
#print(space2.shape)
#print(space3.shape)
#print(space4.shape)
print(space5.shape)

#cv2.imshow('line', space)
#cv2.imshow('line', space2)
#cv2.imshow('line', space3)
#cv2.imshow('line', space4)
cv2.imshow('line', space5)

cv2.waitKey(0)
cv2.destroyAllWindows()
