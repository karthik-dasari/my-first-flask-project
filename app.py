from flask import Flask,render_template,redirect,url_for,request,session
from flask_mysqldb import MySQL

app=Flask(__name__)

app.secret_key='abcdefghijklmnopqrstuvwxyz'

app.config['MYSQL_HOST']='127.0.0.1'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='data'

mysql=MySQL(app)

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/index')
def index():
    if session['loggedin']:
        return render_template('index.html')
    else :
        return f"Please login in"

@app.route('/logout') 
def logout(): 
    session['loggedin']=False
    session.pop('id', None) 
    session.pop('username', None) 
    return redirect('/login') 

@app.route('/login',methods =['GET', 'POST'])
def login():
    if request.method == 'POST':
        username=request.form['username']
        password=request.form['password']
        cursor=mysql.connection.cursor()
        if cursor.execute(' SELECT * FROM user_accounts WHERE username=%s or password=%s ',(username,password)):
            if cursor.execute(' SELECT * FROM user_accounts WHERE username=%s and password=%s ',(username,password)):
                account=cursor.fetchone()
                session['loggedin'] = True
                session['id'] = account[0]
                session['name'] = account[1]
                session['username'] = account[3]
                return redirect('/index')
            elif cursor.execute(' SELECT * FROM user_accounts WHERE username=%s ',(username,)):
                return render_template('login.html',msg="Wrong password",username=username)
            else :
                return f"Invalid"
        else :
            return f"Invalid"
    else :
        return render_template('login.html')

@app.route('/register',methods=['POST','GET'])
def register():
    if request.method == 'POST':
        name=request.form['name']
        username=request.form['username']
        email=request.form['email']
        password=request.form['password']
        cursor=mysql.connection.cursor()
        if cursor.execute(' SELECT * FROM user_accounts WHERE email=%s or username=%s ',(email,username)):
            if cursor.execute(' SELECT * FROM user_accounts WHERE email=%s and username=%s ',(email,username)):
                return render_template('register.html',msg="Email and Username already taken",name=name)
            elif cursor.execute(' SELECT * FROM user_accounts WHERE email=%s ',(email,)):
                return render_template('register.html',msg="Email already registered,try another email",name=name,username=username)
            elif cursor.execute(' SELECT * FROM user_accounts WHERE username=%s ',(username,)):
                return render_template('register.html',msg="Username already exists,try another username",name=name,email=email)
        else :
            cursor.execute(' INSERT INTO user_accounts (Name,Username,Email,Password) VALUES(%s,%s,%s,%s) ',(name,username,email,password))
        mysql.connection.commit()
        cursor.close()
        return f"Done!!!"
    else :
        return render_template('register.html')

@app.route('/forget password',methods=['POST','GET'])
def forget_password():
    return render_template('forget_password.html')

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8000, debug=False)