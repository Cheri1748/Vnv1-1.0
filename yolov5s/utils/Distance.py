import math
import cv2
import numpy as np
import pygame
import time
'''
这段代码用于在图像上可视化目标的位置，并计算目标在相机坐标系下的三维坐标。这些计算可以用于测量目标与相机之间的距离或执行其他需要三维坐标信息的任务。
'''
def draw_measure_line(xyxy,conf, img, size, label,  color=None):
    """
    绘制测距线，并显示目标与相机之间的距离。
    :param xyxy:左上右下
    :param img:图像
    :param size 字体大小
    :param color:
    :param label:
    :param intrinsics_matrix:内参，intrinsics_matrix = [960, 540,775.9, 776.9]  # cx,cy,fx,fy
    :return:目标的位置
    """
    x_in_cam =[]
    y_in_cam = []
    z_in_cam = []
    distance = []
    h = 3  # 相机地面高度，单位：米
    alpha = 0  # 安装俯仰角，单位：度

    # 内参
    intrinsics_matrix = [1574.1, 984.0897, 4965.9, 4965.9]  # cx, cy, fx, fy  #[960, 540, 775.9, 776.9]
    cx, cy, fx, fy = intrinsics_matrix  # ux 和 uy:相机光心在图像上的水平和垂直坐标。 fx 和 fy:相机的水平和垂直焦距。
    pi = math.pi  # 这行代码导入了Python的数学库 math 并定义了π的值，用于后续的三角函数计算。

    for i, box in enumerate(xyxy):
        # 选目标点
        x1, y1, x2, y2 = [int(i) for i in box]
        # 计算质心坐标
        if x1 < img.shape[1] // 2:  # xyxy[0]是左上角点横坐标，xyxy = [xmin, ymin, xmax, ymax]
            # Left side of the frame，判断目标框是否完全位于左半平面
            if x2 < img.shape[1] // 2:  # 目标框完全位于左半平面
                x = int(x2)  # 右下角点横坐标
                y = int(y2)  # 右下角点纵坐标
            else:  # 目标框压着图像的中心线
                x = int((x1 + x2) // 2)  # 目标框左上角点和右上角点的横坐标中点
                y = int(y2)  # 左下角点纵坐标
        else:
            # Right side of the frame，判断目标框是否完全位于右半平面
            if x1 > img.shape[1] // 2:  # 目标框完全位于右半平面
                x = int(x1)  # 左下角点横坐标
                y = int(y2)  # 左下角点纵坐标
            else:  # 目标框压着图像的中心线
                x = int((x1 + x2) // 2)  # 目标框左上角点和右上角点的横坐标中点
                y = int(y2)  # 左下角点纵坐标

        Q_pie = [x - cx, y - cy]# 计算了目标中心点在图像坐标系下相对于相机光心 (cx, cy) 的偏移。(x,y)是像素平面目标的点
        beta = math.atan(Q_pie[1] / fy) * 180 / pi #目标点在相机坐标系中的俯仰角度
        gama = alpha + beta # 计算了角度 gama，其中 alpha 是一个常数。beta_pie是角度

        if gama == 0:
            gama = 0.01

        O2P = round(h / math.tan(gama * pi / 180), 1) # 它与目标在相机坐标系中的距离有关。该值是相机地面高度 h 除以角度 gama 的正切值

        # 计算目标在相机坐标系下的三维坐标，包括 x_in_cam、y_in_cam 和 z_in_cam。这些坐标表示目标在相机坐标系中的位置。
        z_in_cam = (h / math.sin(gama * 180 / pi)) * math.cos(beta * pi / 180) # 前半部分相机到目标的视线距离,OD
        x_in_cam = z_in_cam * (x - cx) / fx # 目标在相机坐标系中的水平坐标,PQ
        y_in_cam = z_in_cam * (y - cy) / fy # 目标在相机坐标系中的垂直坐标,
        distance = round(math.sqrt(O2P ** 2 + x_in_cam ** 2), 2) # 这个距离是通过计算直角三角形的斜边来估算的，其中 O2P 是垂直方向上的距离，x_in_cam 是水平方向上的距离。distance 存储了估算得到的距离值，精确到小数点后两位。

        # #绘制测距线
        connect_point_x = int(img.shape[1] // 2)
        line_color = (74,198,191)
        cv2.line(img, (int(x),int(y) ), (connect_point_x, img.shape[0]), line_color, thickness=1) # 起点是目标中心坐标 (int(x), int(y))，终点是connect_point_x和图像的底部 (img.shape[0])

        if distance < 0:
            distance = "unknown"
        cv2.putText(img, str(distance) + 'm', (int(x + size), int(y)), cv2.FONT_HERSHEY_SIMPLEX, fontScale=size, color=(50,236,229),
                    thickness=2)

    return np.asarray([x_in_cam, y_in_cam, z_in_cam]),distance


