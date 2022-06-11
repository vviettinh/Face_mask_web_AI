import requests
import base64
from datetime import datetime,date
import json
import cv2


def convert_imgarr2base64(img_arr):
    """
    Convert numpy array image to string base64
    Parameters:
        -img_arr: array of image.
    """
    try:
        _, img_encoded = cv2.imencode('.jpg', img_arr)
        jpg_as_text = base64.b64encode(img_encoded).decode('utf-8')
        return jpg_as_text
    except:
        return None




def to_shift(hour):
    """
    Convert day to shift
    -1 is outside of school hours
    """
    
    if 7 <= hour < 9:
        return 1
    if 9 <= hour < 11:
        return 2
    if 12 <= hour < 14:
        return 3
    if 14 <= hour < 16:
        return 4
    if 16 <= hour < 18:
        return 5
    if 18 <= hour < 20:
        return 6
    return -1


def up_data(id_cam, img, label):
    '''
        image: str, label: int, id_cam: int, time, shift: int
    '''
    url = "http://127.0.0.1:5000/post"
    data = {"id_cam": id_cam, "label": label}
    base64img = convert_imgarr2base64(img)
    if base64img is not None:
        data["image"] = base64img
        now = datetime.now()
        hour = now.strftime("%H")
        data["shift"] = to_shift(int(hour))
        #print(to_shift(str(date.today())))
        response = requests.post(url, json=data)
        print("Status code: ", response.status_code)
        print("Printing Entire Post Request")
        print(response.json())
        

