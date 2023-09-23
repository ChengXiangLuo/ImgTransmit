import Connect2PC as C2PC
import cv2
import threading
import RPi.GPIO as gpio
import time

# gpio.cleanup()
gpio.setmode(gpio.BCM)
gpio.setup(19,gpio.OUT)
gpio.setup(13,gpio.OUT)
gpio.output(19,False)
global cam_light # 舌诊灯的亮度 1-100
cam_light = 50

IP = '192.168.137.1'
image_PORT = '5555' # 上传图像端口
order_PORT = '5556' # 接受指令端口

# 初始化摄像头
cap = cv2.VideoCapture(0)  # 使用默认摄像头，如果有多个摄像头，请适当更改索引
cap.set(3, 640)  # 设置帧宽度
cap.set(4, 480)  # 设置帧高度

connect2pc = C2PC._connect2PC(IP,image_PORT,order_PORT)

# 上传图像给PC
def uploadIMG_thread():
    while True:
        ret, frame = cap.read()  # 读取一帧图像
        # cv2.imshow('img', frame)
        connect2pc.imageUpload(frame)   #上传图像

# 处理PC发送的指令
def receCMD_thread():
    global cam_light
    while True:
        cam_light = int(connect2pc.PcCommandProcess())
        if cam_light<0:
            cam_light = 10
        elif cam_light>100:
            cam_light = 100 
            

# 设置亮度
def light_set():
    global cam_light
    while True:
        time.sleep(cam_light/10000)
        gpio.output(13,False)
        time.sleep((100-cam_light)/10000)
        gpio.output(13,True)

uploadIMG_thread = threading.Thread(target=uploadIMG_thread)
receCMD_thread = threading.Thread(target=receCMD_thread)
light_set = threading.Thread(target=light_set)

uploadIMG_thread.start()
receCMD_thread.start()
light_set.start()

uploadIMG_thread.join()
receCMD_thread.join()
light_set.join()