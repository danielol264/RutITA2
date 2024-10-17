from flask import Flask, request, url_for, render_template
from flask_mysqldb import MySQL
app = Flask(__name__)
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='rutita'
mysql=MySQL(app)
@app.route("/")
def index():
    info= selectSQL('select Nombre,Ap_pat,Ap_Mat from Persona')
    return render_template('login.html',info=info)
@app.route("/login")
def login():
    usuario=request.form['Usuario']
    contraseña=request.form['Contraseña']
    return

def selectSQL(scrip):
    cursor=mysql.connection.cursor()
    cursor.execute('{}'.format(scrip))
    return cursor.fetchall()
if __name__=='__main__':

    app.run(port=5000,debug=True)