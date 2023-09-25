#!/usr/bin/env python
# -*- coding=utf-8 -*-

import cv2
import threading
import RecvImg

IP = '' # 默认使用本地IP
re_port = '5555' # 接收端口
se_port = '5556' # 发送端口

re_img = RecvImg._RecvImg(IP,re_port)
se_cmd = RecvImg._SendCmd(IP,se_port)

def user_input_thread():
    while True:
        value = int(input()) # 获得要设置的亮度
        se_cmd.lightValueSet(value) # 发送设置亮度的指令

def zmq_receive_thread():
    while True:
        frame = re_img.imgProcessing()              
        cv2.imshow('img',frame) # 显示接收的图像
        cv2.waitKey(1)


# 创建线程
user_input_thread = threading.Thread(target=user_input_thread)
zmq_receive_thread = threading.Thread(target=zmq_receive_thread)

# 启动线程
user_input_thread.start()
zmq_receive_thread.start()

# 等待线程结束
user_input_thread.join()
zmq_receive_thread.join()


