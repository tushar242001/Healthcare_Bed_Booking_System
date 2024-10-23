from flask import Flask,render_template,redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
import pymysql
from sqlalchemy import text
pymysql.install_as_MySQLdb()
# mydatabase connection 
local_server=True
app=Flask(__name__)
app.secret_key="TusharAdling"

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/dbname'

app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:@localhost/covid'
db=SQLAlchemy(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'userlogin'



class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    srfid = db.Column(db.String(200), unique=True)
    email = db.Column(db.String(200))
    password = db.Column(db.String(1000))
    phone = db.Column(db.Integer)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/usersignup',methods=['POST','GET'])
def usersignup():
    if request.method=="POST":
        srfid=request.form.get('srf')
        email=request.form.get('email')
        password=request.form.get('password')
        phone=request.form.get('phone')
        encpassword=generate_password_hash(password,method='pbkdf2:sha256')
        # print(srfid,email,phone,password)
        new_user = db.session.execute(
            text("INSERT INTO `user` (`srfid`, `email`, `password`, `phone`) VALUES (:srfid, :email, :password, :phone)"),
            {"srfid": srfid, "email": email, "password": encpassword, "phone": phone}
        )
        db.session.commit()  # Commit the transaction
      
    return render_template("usersignup.html")


@app.route('/userlogin',methods=['POST','GET'])
def userlogin():
    if request.method=="POST":
        srfid=request.form.get('srf')
        email=request.form.get('email')
        password=request.form.get('password')
        user=User.query.filter_by(srfid=srfid).first()
        print(user)
        if user and check_password_hash(user.password,password):
            login_user(user)
            return 'Login Success'
        else:
            return 'login failed'
    return render_template("userlogin.html")












@app.route("/hospitalsignup")
def hospitalsignup():
    return render_template("hospitalsignup.html")

@app.route("/hospitallogin")
def hospitallogin():
    return render_template("hospitallogin.html")

@app.route("/adminlogin")
def adminlogin():
    return render_template("adminlogin.html")

@app.route("/adminsignup")
def adminsignup():
    return render_template("adminsignup.html")



app.run(debug=True)