from flask import Flask, request, url_for, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('login.html')


if __name__=='__main__':

    app.run(port=5000,debug=True)