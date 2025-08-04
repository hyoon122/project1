import cv2
print("OpenCV version:", cv2.__version__)
print("Has cv2.legacy:", hasattr(cv2, "legacy"))
print("Available trackers:", dir(cv2.legacy) if hasattr(cv2, "legacy") else "No legacy module")
