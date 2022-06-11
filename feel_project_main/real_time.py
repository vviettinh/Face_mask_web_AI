import cv2,os,io
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from post import up_data    
import base64
from PIL import ImageGrab
#from torch import load_state_dict
import torch
path_model = os.getcwd()+"/best.pt"
#print(path_model)
#device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
model = torch.hub.load('ultralytics/yolov5', 'custom', path=path_model) 
path_video = os.getcwd()+"/class_python.mp4"
print(path_video)
id_cam=1    
device="Web_cam_2"
vidcap = cv2.VideoCapture(path_video)
val =2
while True:
    success,frame = vidcap.read()
    result = model(frame)
    result.print()
    #result.show()
    data =  result.pandas().xyxy[0]
    print(len(data["xmin"])) #1663
    for i in range(len(data["xmin"])):

        crop_img = frame[int(data["ymin"][i]):int(data["ymax"][i]), int(data["xmin"][i]):int(data["xmax"][i])]
        
        img_resize = cv2.resize(crop_img,(256,256))
        #cv2.imshow("name",img_resize)
        print(data["name"][i])
        label= 1
        if(data["name"][i] =="Mask"):
            label = 0
        up_data(id_cam,img_resize,label)
    
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
vidcap.release()