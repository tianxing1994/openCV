# -*- coding: utf-8 -*-
import sys
import numpy as np
import cv2
import math
import matplotlib.pyplot as plt


def show_image(image, win_name='input iamge'):
    cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
    cv2.imshow(win_name, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return


def sobel_canny(image):
    blurred = cv2.GaussianBlur(image, (3, 3), 0)
    gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)

    gradx = cv2.Sobel(gray, cv2.CV_16SC1, 1, 0)
    grady = cv2.Sobel(gray, cv2.CV_16SC1, 0, 1)
    edge_output = cv2.Canny(gradx, grady, 50, 150)

    # 彩色边缘
    # dst = cv.bitwise_and(image, image, mask=edge_output)
    # cv.imshow("Color Edge", dst)
    return edge_output


# 霍夫极坐标变换：直线检测
def hough_line(image, rho, theta, threshold):
    # 宽、高
    rows, cols = image.shape

    L = round(math.sqrt(pow(rows - 1, 2.0) + pow(cols - 1, 2.0))) + 1

    num_theta = int(180.0 / theta)

    num_rho = int(2 * L / rho + 1)
    accumulator = np.zeros((num_rho, num_theta), np.int32)
    # show_image(cv2.convertScaleAbs(accumulator), 'accumulator')

    # 对于 accumulator 中的每一个点, 将为其投票的 image 中的点记录下来. 以便后面在图像中显示它们.
    accu_dict = {}
    for num_rho_r in range(num_rho):
        for num_theta_c in range(num_theta):
            accu_dict[(num_rho_r, num_theta_c)] = []

    # 投票计数
    for y in range(rows):
        for x in range(cols):
            if image[y, x]==255:
                for num_theta_c in range(num_theta):
                    the_rho = x * math.cos(theta * num_theta_c / 180.0 * math.pi) + y * math.sin(theta * num_theta_c / 180.0 * math.pi)
                    # 计算投票哪一个区域. the_rho 取值范围为 [-L, L]. 因此这里加上 L. 使之成为正数.
                    n = int(round(the_rho + L) / rho)
                    accumulator[n, num_theta_c] += 1
                    accu_dict[(n, num_theta_c)].append((x, y))

    lines = []
    for num_rho_r in range(num_rho):
        for num_theta_c in range(num_theta):
            if accumulator[num_rho_r, num_theta_c] > threshold:
                line_rho = num_rho_r * rho - L
                line_theta = theta * num_theta_c / 180.0 * math.pi
                lines.append(((line_rho, line_theta),))

    result = np.array(lines)
    return result


def python_HoughLines():
    # image_path = 'dataset/lena.png'
    image_path = 'dataset/contours.png'
    image_bgr = cv2.imread(image_path)
    image_gray = sobel_canny(image_bgr)

    lines = hough_line(image_gray, 1, 1, 120)
    # print(lines)

    for line in lines:
        rho, theta = line[0]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))

        cv2.line(image_bgr, (x1, y1), (x2, y2), (0, 0, 255), 2)
    show_image(image_bgr, 'real hough')

    return image_bgr

def real_HoughLinesP():
    # image_path = 'dataset/lena.png'
    image_path = 'dataset/contours.png'
    image_bgr = cv2.imread(image_path)
    image_gray = sobel_canny(image_bgr)
    lines = cv2.HoughLinesP(image_gray, 1, 1, 120)

    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(image_bgr, (x1, y1), (x2, y2), (0, 0, 255), 2)
    show_image(image_bgr)
    return image_bgr


def real_HoughLines():
    # image_path = 'dataset/lena.png'
    image_path = 'dataset/contours.png'
    image_bgr = cv2.imread(image_path)
    image_gray = sobel_canny(image_bgr)

    lines = cv2.HoughLines(image_gray, 1, np.pi / 180, 120)
    # print(lines)

    for line in lines:
        rho, theta = line[0]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))

        cv2.line(image_bgr, (x1, y1), (x2, y2), (0, 0, 255), 2)
    show_image(image_bgr, 'real hough')
    return


if __name__ == "__main__":
    python_HoughLines()



