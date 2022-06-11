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
id_cam=3
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
        x = int(data["xmin"][i])
        y = int(data["ymin"][i])
        w = int(data["xmax"][i])
        h = int(data["ymax"][i])
        frame = cv2.rectangle(frame, (x+10,y+5), (w+10,h+5), (255,0,0), 2)
        img_resize = cv2.resize(crop_img,(256,256))
        frame = cv2.putText(frame,data["name"][i],(x+5, y-15),cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)
        
    #     up_data(id_cam,img_resize,label)
    cv2.imshow("name",frame)
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break
vidcap.release()