#!/usr/bin/env python
# -*- coding=utf-8 -*-

import cv2
import threading
import RecvImg

IP = ''
re_port = '5555'
se_port = '5556'

re_img = RecvImg._RecvImg(IP,re_port)
se_cmd = RecvImg._SendCmd(IP,se_port)

def user_input_thread():
    while True:
        value = int(input())
        se_cmd.lightValueSet(value)

def zmq_receive_thread():
    while True:
        frame = re_img.imgProcessing()              
        cv2.imshow('img',frame)
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


