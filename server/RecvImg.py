#!/usr/bin/env python
# -*- coding=utf-8 -*-

import cv2
import zmq
import base64
import numpy as np


class _RecvImg:
    """设置接收图像的IP和端口,IP为空则默认绑定本地IP
    """
    def __init__(self,IP,port):
        self.IP = IP
        self.port = port
        if IP == '':
            bind_str = 'tcp://*:' + str(port)
        elif IP != '':
            bind_str = 'tcp://' + str(IP) +':'+ str(port) 
        self.context = zmq.Context()        
        self.recv_socket = self.context.socket(zmq.PULL)
        self.recv_socket.bind(bind_str)  # 绑定接口

    """收到传来的数据流后解析成图像，返回图像
    """  
    def imgProcessing(self):
        frame = self.recv_socket.recv_string() #接收TCP传输过来的一帧视频图像数据
        img = base64.b64decode(frame) #把数据进行base64解码后储存到内存img变量中
        npimg = np.frombuffer(img, dtype=np.uint8) #把这段缓存解码成一维数组
        source = cv2.imdecode(npimg, 1) #将一维数组解码为图像source
        return source
        

class _SendCmd():
    """设置发送指令的IP和端口,IP为空则默认绑定本地IP
    """
    def __init__(self,IP,port):
        self.IP = IP
        self.port = port
        if IP == '':
            bind_str = 'tcp://*:' + str(port)
        elif IP != '':
            bind_str = 'tcp://' + str(IP) +':'+ str(port)
        self.context = zmq.Context()
        self.send_socket = self.context.socket(zmq.PUSH)
        self.send_socket.bind(bind_str)

    """发送调节舌诊探头亮度的指令,亮度范围0-100
    """
    def lightValueSet(self,value):
        if(value>100 or value<0):
            value = 50
            print('value is out of range')
        send_str = 'cam_light:' + str(value) 
        self.send_socket.send_string(send_str)
    

