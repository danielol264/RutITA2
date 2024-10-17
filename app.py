from flask import Flask, request, url_for, render_template,redirect, flash
from flask_mysqldb import MySQL
from models.modelo import modelo
from models.User import User
app = Flask(__name__)
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='rutita'
mysql=MySQL(app)
@app.route("/")
def index():
    return render_template('login.html')
@app.route("/login",methods=['POST'])
def login():
    usuario=User(0,request.form['Usuario'],request.form['Contraseña'])    
    usuario_logeado=modelo.login(mysql,usuario)
    if usuario_logeado != None:
            if usuario_logeado.contraseña:
                id=usuario_logeado.id
                return redirect(url_for('home',id=id)) 
            else:
                flash('error!!! contraseña incorrecta')
                return render_template('login.html')
    else:
            flash('error!!! usuario no enncontrado')    
            return render_template('login.html')

@app.route("/home/<id>")
def home(id):
     return "<h1>hola</h1>"
def selectSQL(scrip):
    cursor=mysql.connection.cursor()
    cursor.execute('{}'.format(scrip))
    return cursor.fetchall()
if __name__=='__main__':

    app.run(port=5000,debug=True)