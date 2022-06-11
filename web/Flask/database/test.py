import os
from datetime import datetime,date
print(os.getcwd())
#/home/viettinh/Desktop/learing/AI/Project/Face_mask_web/BTL-python/web/Flask/database/User.py
path = "{}/Face_mask_web/BTL-python/web/Flask/database/data.db".format(os.getcwd())
print(path)
print(date.today())
now = datetime.now()
print(now.strftime("%H"))