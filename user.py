from datetime import datetime
import functools
import os;
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
import mysql.connector

bp = Blueprint('user', __name__, url_prefix='/')
try:
    conn = mysql.connector.connect(host='localhost', password='root', user='root', database='trip_plan', port='8889')
    db = conn.cursor(buffered=True)
    print("Connected to Db");
except Exception as e:
    print("not connected to database")




@bp.route('/login', methods=('GET', 'POST'))
def login():

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        error = None
        db.execute(
            'SELECT * FROM User WHERE Email=\''+email+"'"
        )
        user = db.fetchone()
        if user is None:
            error = 'Incorrect email.'
        elif not (user[4] == password):
            error = 'Incorrect password.'
        if error is None:
            session.clear()
            session['email'] = user[3]
            return "success"

        flash(error)

    return render_template('user/login.html')


@bp.route('/register', methods=('GET', 'POST'))
def register():

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        address = request.form['address']
        phone = request.form['phone']
        # birthday = datetime.strftime(request.form['birthday'],'%Y,%m,%d')
        birthday = request.form['birthday']
        url = None
        if request.files and request.files['image']:
            print(request.files)
            image = request.files['image']
            url = os.path.join("/Users/rewant/PycharmProjects/TripPlanner/imageuploads", image.filename)
            image.save(url)
            print("Image saved")


       # finalimage= FileContents(name=image.filenamem,data=image.read());

        print(name, email, password, address, phone,url, birthday)
        error = None
        db.execute(
             'SELECT * FROM User WHERE Email=\''+email+"'"
        )
        check = db.fetchone()
        if check:
            error = "User Already exists"
            flash(error)
            return redirect(request.url)
        # if url is None:
        #     url= None
        #     db.execute(
        #         'INSERT INTO USER(Name,Email,Password,Address,Phone,Birthday) values (%s,%s,%s,%s,%d,%s)',
        #         (name, email, password, address, phone, birthday)
        #     )
        # else:

        db.execute("SELECT MAX(UserID) from User")
        userid1=db.fetchone();
       # userid=db.lastrowid;
        print(userid1[0]);
        userid1=userid1[0]+1
        db.execute(
            'INSERT INTO User(UserID, Name,Email,Password,Address,Phone,Photograph,Birthday) '
            'values (%s,%s,%s,%s,%s,%s,%s,%s)',
            (userid1,name, email, password, address, phone, url, birthday)
        )

        conn.commit();
        return render_template('user/login.html')
        # user = db.fetchone()
        # if user is None:
        #     error = 'Incorrect email.'
        # elif not (user[4] == password):
        #     error = 'Incorrect password.'
        # if error is None:
        #     session.clear()
        #     session['email'] = user[3]
        #     return "success"

        flash(error)

    return render_template('user/register.html')