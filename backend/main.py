from flask import Flask,render_template,redirect,flash,request, url_for
from flask.globals import request
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, login_user, UserMixin, logout_user
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
        user=User.query.filter_by(srfid=srfid).first()
        emailUser=User.query.filter_by(email=email).first()
        if user or emailUser:
            flash("Email or Srfid already present","warning")
            return render_template("usersignup.html")
        # print(srfid,email,phone,password)
        new_user = db.session.execute(
            text("INSERT INTO `user` (`srfid`, `email`, `password`, `phone`) VALUES (:srfid, :email, :password, :phone)"),
            {"srfid": srfid, "email": email, "password": encpassword, "phone": phone}
        )
        db.session.commit()  # Commit the transaction
        flash("Sign in Success","success")
        return render_template("userlogin.html")
    return render_template("usersignup.html")


@app.route('/userlogin',methods=['POST','GET'])
def userlogin():
    if request.method=="POST":
        srfid=request.form.get('srf')
        email=request.form.get('email')
        password=request.form.get('password')
        user=User.query.filter_by(srfid=srfid).first()
        if user and check_password_hash(user.password,password):
            login_user(user)
            flash("Login Success","info")
            return render_template("index.html")
        else:
            flash("Invalid Credentials","danger")
            return render_template("userlogin.html")
        


    return render_template("userlogin.html")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logout Successful","Warning")
    return redirect(url_for('userlogin'))






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