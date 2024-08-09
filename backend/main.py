from flask import Flask,render_template,redirect
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()
# mydatabase connection 
local_server=True
app=Flask(__name__)
app.secret_key="TusharAdling"

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/dbname'

app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:@localhost/covid'
db=SQLAlchemy(app)


class Test(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/usersignup")
def usersignup():
    return render_template("usersignup.html")

@app.route("/userlogin")
def userlogin():
    return render_template("userlogin.html")


# testing wherther db is connected or not
@app.route("/test")
def test():
    try:
        a=Test.query.all()
        print(a)
        return 'MY DATABASE IS CONNECTED'
    
    except Exception as e:
        return f'MY DATABASE IS NOT CONNECTED {e}'
    

app.run(debug=True)