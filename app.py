from flask import Flask, request, url_for, render_template,redirect, flash
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('kevin.html')

@app.route("/home/<id>")
def home(id):
     return "<h1>hola</h1>"

if __name__=='__main__':

    app.run(port=5000,debug=True)