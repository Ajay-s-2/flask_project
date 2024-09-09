from flask import Flask, render_template, redirect, url_for, request
from flask_mysqldb import MySQL

app = Flask(__name__, template_folder="template", static_folder="static")

# MySQL connection
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "flaskdb"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
mysql = MySQL(app)

# Loading the home page
@app.route("/")
def home():
    cur = mysql.connection.cursor()
    sql = "SELECT * FROM users"
    cur.execute(sql)
    res = cur.fetchall()
    cur.close()  # Always close the cursor
    return render_template("home.html", datas=res)

# New user insert data
@app.route("/adduser", methods=["POST", "GET"])
def adduser():
    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        city = request.form["city"]
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (name, age, city) VALUES (%s, %s, %s)", (name, age, city))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for("home"))
    return render_template("adduser.html")

# Edit user
@app.route("/edituser/<string:id>", methods=["POST", "GET"])
def edituser(id):
    cur = mysql.connection.cursor()
    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        city = request.form["city"]
        cur.execute("UPDATE users SET name=%s, age=%s, city=%s WHERE id=%s", (name, age, city, id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for("home"))

    cur.execute("SELECT * FROM users WHERE id=%s", (id,))
    res = cur.fetchone()
    cur.close()
    return render_template("edituser.html", data=res)

# Delete user
@app.route("/deleteuser/<string:id>", methods=["POST", "GET"])
def deleteuser(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE id=%s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for("home"))

if __name__ == '__main__':
    app.run(debug=True)
