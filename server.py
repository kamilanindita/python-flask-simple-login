from flask import Flask,render_template, request, url_for, redirect, session
from flask_mysqldb import MySQL


app = Flask(__name__)
app.config["MYSQL_HOST"]="localhost"
app.config["MYSQL_DB"]="website_crud"
app.config["MYSQL_USER"]="root"
app.config["MYSQL_PASSWORD"]=""
app.config["MYSQL_CURSORCLASS"]="DictCursor"
mysql = MySQL(app)

app.secret_key = 'qazxsw123%*#(^@'



@app.route("/")
def index():
    title="Index"
    return render_template("index.html",title=title)
    
@app.route("/home")
def home():
    if session :
        title="Home"
        return render_template("home.html",title=title)    
    
    else:
        return redirect(url_for("index"))
    
@app.route("/register",methods=["GET","POST"])
def register():
    if request.method=='GET' :
        title="Register"
        return render_template("register.html",title=title)
        
    else:
        name=request.form["name"]
        email=request.form["email"]
        password=request.form["password"]
       
        data=(name,email,password)
        query="INSERT INTO users (name,email,password) VALUES (%s,%s,%s)"
        cur = mysql.connection.cursor()
        cur.execute(query,data)
        mysql.connection.commit()
        cur.close()
        
        session['name']=name
        session['email']=email
        
        return redirect(url_for('home'))
  

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=='GET' :
        title="Login"
        return render_template("login.html",title=title)
        
    else:
        email=request.form["email"]
        password=request.form["password"]
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email= %s",(email,))
        user = cur.fetchone()
        cur.close()
  
        if user :
            if user['password']==password :
                session['name']=user['name']
                session['email']=email
            
                return redirect(url_for('home'))
            else:
                return "password wrong!"
        
        else:
            return "user not found!"


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))
    
if __name__ == '__main__':
    app.run(debug=True)
