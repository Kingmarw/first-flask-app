from flask import Flask,render_template,request,redirect,session
# database SQL lite
import sqlite3

app = Flask(__name__)
app.secret_key = "12324"

@app.route("/")
def home():
    db = sqlite3.connect('app.db')
    cr = db.cursor()
    cr.execute("select * from users")
    if 'user' in session:
        return render_template("index.html",page=f"home {session['user']}")
    else:
        return render_template("index.html",page=f"home")
# methods=['POST']

@app.route("/reg")
def reg():
    return render_template("reg.html", page="register page")


@app.route("/register",methods=['POST'])
def apireg():
    db = sqlite3.connect("app.db")
    cr = db.cursor()
    name = request.form.get('name')
    password = request.form.get('pass')
    cr.execute("CREATE TABLE if not exists users(user_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, password TEXT)")
    cr.execute("INSERT INTO users(name,password) VALUES (?,?)",(name,password))
    db.commit()
    db.close()
    return redirect("/reg")

@app.route("/login")
def login():
    return render_template("login.html",page="Login")

@app.route("/logapi", methods=['POST'])
def logapi():
    db = sqlite3.connect("app.db")
    cr = db.cursor()
    name = request.form.get("name")
    password = request.form.get("password")
    cr.execute("select * from users")
    dataFetch = cr.fetchall()
    def loginForm():
        for userInfo in dataFetch:
            if name == userInfo[1] and password == userInfo[2]:
                session['user'] = name
                return redirect("/")
        return render_template("err.html",page="error page")
    result = loginForm()
    db.close()
    return result

if __name__ == "__main__":
    app.run(debug=True)