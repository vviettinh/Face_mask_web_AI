from flask import Flask, redirect, url_for, render_template, session, request, flash, jsonify
from datetime import timedelta, datetime, date

import sys
from database.User import User
import uuid

from database.Data import Data
#from Database.sql import SQL_Server
import os
import base64
import hashlib
from flask_ngrok import run_with_ngrok
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
#sql = SQL_Server()
run_with_ngrok(app)
app.config['SECRET_KEY'] = 'mykey'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:/Database/user.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.permanent_session_lifetime = timedelta(minutes=5)
#db = SQLAlchemy(app)
Data = Data()
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session.permanent = True
        user = request.form['name']
        pw = request.form['pass']
        password = hashlib.md5(pw.encode()).hexdigest()
        if User.find_user(user, password):
            session['user'] = user
            session['password'] = password
            return redirect(url_for("home"))
        else:
            flash('Không tìm thấy tài khoản hoặc mật khẩu trùng')
            return render_template('login.html')
    else:
        if 'user' in session and 'password' in session:
            return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/home')
def home():
    if 'user' in session and 'password' in session:
        # get list camera
        query = 'SELECT * FROM Camera'
        listCamera = Data.select(query)

        # get infor of camera includes:  use smartphone, use laptop,  others...
        thietbi = listCamera[0][0]

        # get infor of chart (list statis about emotion)

        query = "SELECT LoaiFace, COUNT(*) AS SoLuong FROM Face"
        
        query += " where ThietBi= {} and Ngay ='{}' and Kip={}".format(
            0, str(date.today()), -1)
        query += " GROUP BY LoaiFace"
        
        listFace = Data.select(query)
        print(listFace)

        data1 = [0, 0]
        for obj in listFace:
            data1[int(obj[0])] = obj[1]
        print(data1)

        # get list image of first face
        query = "SELECT image FROM Face where"
        query += " LoaiFace={} and ThietBi= {} and Ngay='{}' and Kip={}".format(
            0, 0,str(date.today()), -1)

        listImage = Data.select(query)
        print(listImage)
        return render_template('home.html', listCamera=listCamera,
                               data1=data1, listImage=listImage)
    else:
        return redirect(url_for('index'))

@app.route('/info', methods=[ 'POST'])
def get_image_with_camera():
     if request.method == 'POST':
        try:
            data = request.get_json()
            id_cam = data['id_cam']
            date = data['time']
            shift = data['shift']
            e = int(data['face'][1])
            #print(data)
            query = "SELECT LoaiFace, COUNT(*) AS SoLuong FROM Face"
            query += " where ThietBi= {} and Ngay = '{}' and Kip={}".format(
                id_cam, date, shift)
            query += " GROUP BY LoaiFace"

            listFace = Data.select(query)
            print(listFace)
            #print(face[0])
            data = {}
            for face in listFace:
                data[str(face[0])] = face[1]

            query = "SELECT image FROM Face where"
            query += " LoaiFace = {} and ThietBi= {} and Ngay = '{}' and Kip = {}".format(
                e, id_cam, date, shift )
            print(query)
            listImage = Data.select(query)
            #print(listImage)
            data['image'] = [img[0] for img in listImage]
            #print(data)
            return jsonify(data)
        except Exception as e:
            print(e)
            return jsonify({'Status': 'Failed', 'msg': str(e)})
        
@app.route('/post', methods=["POST"])
def insert_data_to_db():
    if request.method == 'POST':
        try:
            data = request.get_json()
            id_cam = data['id_cam']
            # mask : 0, no mask : 1
            label = data['label']
            image = data['image']  # base64 (string)
            shift = data['shift']
            time =str( date.today())

            #face_dictionary = {'mask': 0, 'no mask': 1}
            #label = face_dictionary[label.lower()]

            directory = str(date.today())
            # Parent Directory path
            parent_dir = os.getcwd()
            # Path
            path = parent_dir+"/"+"static"+"/"+"image"+"/"+directory
            try:
                os.mkdir(path)
            except:
                print('Folder exist!')

            # Process base64 string
            filename = str(datetime.now())
            specialChars = "!#$%^&*():.- "
            for specialChar in specialChars:
                filename = filename.replace(specialChar, '')

            url_save_to_db = "static/image/"+directory+"/"+filename+".jpg"
            url_img = path+"/"+filename
            url_img += '.jpg'
            with open(url_img, "wb") as f:
                f.write(base64.b64decode(image.encode('utf-8')))
                
            query = "INSERT INTO Face (image, LoaiFace, ThietBi, Ngay, Kip) Values ('{}', '{}', '{}', '{}', '{}' )".format(url_save_to_db,
                                                                                            label, id_cam, time, shift)
            Data.insert(query)

            return jsonify({'id_cam': id_cam, 'label': label, 'image': url_save_to_db, 'time': time, 'shift': shift})
        except Exception as e:
            print(e)
            return jsonify({'Status': 'Failed', 'msg': str(e)})


@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('password', None)
    return redirect(url_for('index'))

@app.route('/register',methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        session.permanent = True
        name_user = request.form['name']
        pw = request.form['password']
        password = hashlib.md5(pw.encode()).hexdigest()
        email = request.form['email']
        if  not User.find_user(name_user, password):
            User.create_user(name_user,password,email) 
            flash("bạn đã đăng kí thành công")
            return render_template("register.html")
        else:
            flash('tài khoản đã tồn tại')
            return render_template("register.html")
    return render_template("register.html")
if __name__ == '__main__':
    # app.run(host='0.0.0.0', port='9999')
    #print(datetime.now())
    app.run()
    