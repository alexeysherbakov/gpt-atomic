from flask import Flask, render_template, request, jsonify, redirect, url_for, make_response
from flask_sqlalchemy import SQLAlchemy
from text import main
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__, static_folder='static')
app.secret_key = 'hellosarpens'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)

class Userlogpass(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    #ДБ пользователей

class Datahistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    input = db.Column(db.String(100), unique=False)
    output = db.Column(db.String(100))
    #ДБ запросов-ответов GPT

with app.app_context():
    db.create_all()


@app.route("/login", methods=['GET'])
def login():
    return render_template('login.html')


@app.route("/logins", methods=['POST'])
def logins():
    form_get_data = {"username": request.form.get("usr"), "password":request.form.get("pas")}
    print(form_get_data)
    exists = db.session.query(Userlogpass).filter_by(username=form_get_data["username"], password=form_get_data["password"]).first()
    if exists:
        resp = make_response(redirect( url_for('get') ))
        resp.set_cookie('cookishki', form_get_data['username'], max_age=600)
        return resp
    else:
        return redirect(url_for('reg'))
    

@app.route("/reg", methods=['GET'])
def reg():
    return render_template('reg.html')


@app.route("/regs", methods=['POST'])
def regs():
    usr = request.form.get('usr')
    pas = request.form.get('pas')
    if usr in db.session.query(Userlogpass):
        return +redirect(url_for('login'))
    elif usr == pas:
        return render_template('reg.html')
    else:
        reg_data = Userlogpass(username=usr, password=pas)
        db.session.add(reg_data)
        db.session.commit()
        return redirect( url_for('login') )


@app.route('/get')
def get():
    if request.cookies.get('cookishki') is None:
        return redirect( url_for('login') )
    else:
        return render_template('get.html')


@app.route('/process', methods=['POST'])
@limiter.limit("50 per day")
def process():
    input_data = request.form['input_data']
    reply_content = main(input_data)
    output_data = f'<h4>Я: {input_data} </h4> {reply_content}'
    db_data = Datahistory(input=input_data, output=reply_content)
    db.session.add(db_data)
    db.session.commit()
    return jsonify(output_data=output_data)


@app.route('/history')
def history():
    dbdata = db.session.query(Datahistory).all()
    return render_template('history.html', dbdata=dbdata)