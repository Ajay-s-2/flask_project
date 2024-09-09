
from flask import Flask,render_template,redirect,url_for,request
from flask_mysqldb import MySQL

app = Flask(__name__, template_folder="template", static_folder="static", static_url_path='/home.html')
#mysqlconnection
app.config["MYSQL_HOST"]="localhost"
app.config["MYSQL_USER"]="root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"]="flaskdb"
app.config["MYSQL_CURSORCLASS"]= "DictCursor"
mysql=MySQL(app)
#loding the home page
@app.route("/")
def home():
    con = mysql.connection.cursor()
    sql= "select * From users"
    con.execute(sql)
    res=con.fetchall()
    return render_template("home.html",datas =res)
#new user insert data
@app.route("/adduser",methods=["POST","GET"])
def adduser():
    if request.method=="POST":
        name=request.form["name"]
        age=request.form["age"]
        city=request.form["city"]
        cur=mysql.connection.cursor()
        cur.execute("insert into users (name,age,city) values(%s,%s,%s)",(name,age,city))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for("home"))
    return render_template("adduser.html")
#edite user
@app.route("/edituser/<string:id>",methods=["POST","GET"])
def edituser(id):
    if request.method=="POST":
        name=request.form["name"]
        age=request.form["age"]
        city=request.form["city"]
        cur=mysql.connection.cursor()
        cur.execute("update users set name=%s,age=%s,city=%s where id=%s",(name,age,city,id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for("home"))
    cur=mysql.connection.cursor()
    cur.execute("select * from users where id=%s",(id))
    res=cur.fetchone()
    return render_template("edituser.html",data=res)
#delete user
@app.route("/deleteuser/<string:id>",methods=["POST","GET"])
def deleteuser(id):
    cur=mysql.connection.cursor()
    cur.execute("delete from users where id=%s",(id))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for("home"))

if (__name__=='__main__'):
    app.run(debug=True)
