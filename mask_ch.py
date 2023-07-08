import cv2
import numpy as np

img = cv2.imread("mask1.jpg")
img = cv2.resize(img, (600, 800))
g_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, img = cv2.threshold(g_img, 180, 255, cv2.THRESH_BINARY) 

w = 50
h = 50
step = 5
histograms = []
for y in range(0, 800, step):     
    for x in range(0, 600, step):      
        roi = img[y:y + h, x:x + w]
        if np.any(roi == 255):
            hist = cv2.calcHist([roi], [0], None, [256], [0, 256])
            histograms.append((x, y, hist))

threshold = 0.3
selected_points = []
for i in range(len(histograms)):
    for j in range(i + 1, len(histograms)):
        x1, y1, hist1 = histograms[i]
        x2, y2, hist2 = histograms[j]
        distance = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
        if distance > threshold:
            selected_points.append((x1, y1))
            selected_points.append((x2, y2))

num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(img, connectivity=8)

max_area = 0
max_area_index = 0
for i in range(1, num_labels):
    area = stats[i, cv2.CC_STAT_AREA]
    if area > max_area:
        max_area = area
        max_area_index = i

mask = np.zeros_like(labels, dtype=np.uint8)
mask[labels == max_area_index] = 255
last_img = cv2.cvtColor(g_img, cv2.COLOR_GRAY2BGR)
last_img[mask == 255] = (255, 0, 0)

cv2.imshow("Last_img", last_img)
cv2.waitKey(0)
cv2.destroyAllWindows()