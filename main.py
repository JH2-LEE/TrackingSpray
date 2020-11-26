import cv2
import numpy as np
import serial

# start serial communication: ubuntu usb port 0
arduino = serial.Serial("/dev/ttyACM0", 9600, bytesize=8)

# read image
cap = cv2.VideoCapture(2)

# width, height resolution
cap.set(3, 640)
cap.set(4, 480)

# dest size
dest = (640, 480)


def find_moment_pixel(img):
    """
    find moment pixel in binary image
    """
    src = img.copy()
    # chroma key image
    M = cv2.moments(src, True)
    global cx, cy
    cx = int(M["m10"] / M["m00"])
    cy = int(M["m01"] / M["m00"])
    src = cv2.circle(src, (cx, cy), 5, (0, 0, 0), -1)
    # return cx, cy
    return src


def transform(img):
    """
    return warp image from points to points
    """
    pts = np.float32([(136, 81), (31, 306), (620, 299), (511, 80)])
    pts_dest = np.float32([(0, 0), (0, 480), (640, 480), (640, 0)],)

    matrix = cv2.getPerspectiveTransform(pts, pts_dest)

    img_rst = cv2.warpPerspective(img, matrix, dest)
    return img_rst


def chromakey(img):
    """
    remove background color and return the binary image
    """
    rgb_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # h range (green)
    min_green = (80, 100, 100)
    max_green = (110, 245, 245)

    img_mask = cv2.inRange(rgb_hsv, min_green, max_green)
    img_mask = np.invert(img_mask)
    img_mask = img_mask.reshape(480, 640, 1)
    return img_mask


def cal_degrees(x, y):
    """
    calculate the degrees of servo motor using the pixel of spray
    x, y: pixel of image moment
    """
    degree = 180 - np.arctan2(y + 73, x - 320) * 180 / np.pi
    return degree


while True:
    ret, frame = cap.read()
    warp = transform(frame)
    chroma = chromakey(warp)
    src = find_moment_pixel(chroma)
    cv2.imshow("test", src)

    deg = cal_degrees(cx, cy)
    print(cx, cy, int(deg))

    # serial communication
    arduino.write([int(deg)])

    # keyboard
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break
    elif k == ord("s"):
        print("Image has saved.")
        # cv2.imwrite("raw_image.jpg", frame)
        cv2.imwrite("chroma_obj.jpg", frame)
    elif k == ord("p"):
        print("Find rectangle points")
        cv2.imwrite("blank.jpg", frame)
    elif k == ord("c"):
        arduino.write([int(deg)])

cap.release()
cv2.destroyAllWindows()
