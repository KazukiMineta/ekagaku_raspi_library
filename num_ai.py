import cv2
import numpy as np

# Canvas for drawing
canvas = np.zeros((200, 200), dtype=np.uint8)

drawing = False
last = None

def draw(event, x, y, flags, param):
    global drawing, last
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        last = (x, y)
    elif event == cv2.EVENT_MOUSEMOVE and drawing:
        cv2.line(canvas, last, (x, y), 255, 20)
        last = (x, y)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False

cv2.namedWindow("Draw")
cv2.setMouseCallback("Draw", draw)

# Create KNN
knn = cv2.ml.KNearest_create()

# Generate training data (0–9)
train = []
labels = []
for i in range(10):
    img = np.zeros((20, 20), dtype=np.uint8)
    cv2.putText(img, str(i), (2, 18), cv2.FONT_HERSHEY_SIMPLEX, 0.8, 255, 2)
    train.append(img.reshape(400).astype(np.float32))
    labels.append(i)

train = np.array(train)
labels = np.array(labels, dtype=np.float32)

knn.train(train, cv2.ml.ROW_SAMPLE, labels)

while True:
    cv2.imshow("Draw", canvas)
    key = cv2.waitKey(1)

    if key == ord('p'):
        img = cv2.resize(canvas, (20, 20)).reshape(1, 400).astype(np.float32)
        ret, result, neighbours, dist = knn.findNearest(img, k=1)
        print("Prediction:", int(result[0][0]))

    if key == ord('c'):
        canvas[:] = 0

    if key == ord('q'):
        break

cv2.destroyAllWindows()