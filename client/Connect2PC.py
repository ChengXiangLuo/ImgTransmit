import cv2
import zmq
import base64
import re

class _connect2PC:
    """连接Pc
    IP: ip设置
    TX2PC_PORT: 发送端口
    RX2PC_PORT: 接收端口
    """
    def __init__(self,IP,TX2PC_PORT,RX2PC_PORT):
        self.context = zmq.Context()
        # zmq 对象使用TCP通讯协议
        self.send_socket = self.context.socket(zmq.PUSH)
        self.rece_socket = self.context.socket(zmq.PULL)
        # zmq 对象和视频接收端建立TCP通讯协议
        self.send_socket.connect(f'tcp://{IP}:{TX2PC_PORT}')
        self.rece_socket.connect(f'tcp://{IP}:{RX2PC_PORT}')

    """上传图像数据流
    frame: 摄像头获得的图像
    """
    def imageUpload(self,frame):
        _, buffer = cv2.imencode('.jpg', frame)  # 把图像数据转换为JPEG格式并编码
        jpg_as_text = base64.b64encode(buffer)  # 把编码后的图像数据转换为base64编码
        # 发送图像数据给视频接收端
        self.send_socket.send(jpg_as_text)
    
    """_summary_
    处理PC发送的指令

    Returns:
        要设置的亮度
    """
    #处理PC发送的指令
    def PcCommandProcess(self):
        data = self.rece_socket.recv_string()
        # print(data)
        if data.startswith('cam_light'):
            dec = re.findall(r'-?\d+',data)
            return dec[0]
            
    
    
     

