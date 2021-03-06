import cv2 as cv
import numpy as np


def show_image(image, win_name='input image'):
    cv.namedWindow(win_name, cv.WINDOW_NORMAL)
    cv.imshow(win_name, image)
    cv.waitKey(0)
    cv.destroyAllWindows()
    return


def make_ploygon():
    # 新建 512*512 的空白图片
    image = np.zeros((512, 512, 3), np.uint8)
    # 平面点集
    points = np.array([[200, 250],
                       [250, 300],
                       [300, 270],
                       [270, 200],
                       [120, 240]], np.int32)

    points = points.reshape((-1, 1, 2))

    # 绘制填充的多边形
    cv.fillPoly(image, [points], (255, 255, 255))
    return image


def demo1():
    image = make_ploygon()
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    # 二值化
    ret, thresh = cv.threshold(gray, 127, 255, cv.THRESH_BINARY)
    # 图片轮廓
    _, contours, _ = cv.findContours(thresh, 2, 1)
    contour = contours[0]
    # 寻找凸包并绘制凸包（轮廓）
    hull = cv.convexHull(contour)

    length = len(hull)
    for i in range(length):
        print(hull[i][0], hull[(i + 1) % length][0])
        cv.line(image, tuple(hull[i][0]), tuple(hull[(i + 1) % length][0]), (0, 255, 0), 2)

    show_image(image)
    return


def demo2():
    image = make_ploygon()
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    # 二值化
    ret, thresh = cv.threshold(gray, 127, 255, cv.THRESH_BINARY)
    # 图片轮廓
    _, contours, _ = cv.findContours(thresh, 2, 1)
    contour = contours[0]
    # returnPoints=False. 返回凸包点在 contour 中的索引.
    hull = cv.convexHull(contour, returnPoints=False)

    length = len(hull)
    for i in range(length):
        index1 = hull[i][0]
        index2 = hull[(i + 1) % length][0]
        cv.line(image, tuple(contour[index1][0]), tuple(contour[index2][0]), (0, 255, 0), 2)
    show_image(image)
    return


def demo3():
    """
    凸包缺陷检测. 计算凹陷进去的点的距离.
    :return:
    """
    image = make_ploygon()
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    # 二值化
    ret, thresh = cv.threshold(gray, 127, 255, cv.THRESH_BINARY)
    # 图片轮廓
    _, contours, _ = cv.findContours(thresh, 2, 1)
    contour = contours[0]
    # returnPoints=False. 返回凸包点在 contour 中的索引.
    hull = cv.convexHull(contour, returnPoints=False)

    hull_defects = cv.convexityDefects(contour, convexhull=hull, convexityDefects=None)

    length = len(hull_defects)
    for i in range(length):
        data = hull_defects[i][0]
        index1 = data[0]
        index2 = data[1]
        index3 = data[2]
        distance = data[3]
        print(distance)
        cv.line(image, tuple(contour[index1][0]), tuple(contour[index2][0]), (0, 255, 0), 2)
        cv.circle(image, center=tuple(contour[index3][0]), radius=5, color=(0, 0, 255))
    show_image(image)
    return


if __name__ == '__main__':
    demo3()
