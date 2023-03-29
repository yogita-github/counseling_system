from flask import Flask, render_template, url_for ,request,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user,LoginManager,login_required,logout_user,current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
import numpy as np
import pickle
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE
import data
import file
import datalist

import pandas as pd

app = Flask(__name__)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False,unique=True)
    password = db.Column(db.String(80), nullable=False)

class RegistrationForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder":"Username"})
    
    password = PasswordField(validators=[InputRequired(),Length(
        min=4 , max=20)], render_kw={"placeholder":"Password"})
    
    submit = SubmitField('Register')

    def validate_username(self,username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        
        if existing_user_username:
            raise ValidationError(
                'That username already exists.Please choose a different one.')
        
class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder":"Username"})
    
    password = PasswordField(validators=[InputRequired(),Length(
        min=4 , max=20)], render_kw={"placeholder":"Password"})
    
    submit = SubmitField("Login")


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def forms():
    gender = request.form['gender']
    age = request.form['age']
    sbp = request.form['sbp']
    hbp = request.form['hbp']
    spo2 = request.form['spo2']
    temp_c = int(request.form['temp'])
    temp = temp_c*9/5+32
    h_rate = request.form['h_rate']
    glc = request.form['glc']
    vitals = [age, sbp, hbp, h_rate, glc, spo2, temp_c]
    res = predict(gender,age, sbp, hbp, h_rate, glc, spo2, temp)
    if (res[0] == 1):
        result = "healthy"
        data, phy, medi, nutri, meds = rec("healthy")
        
    elif(res[0] == 2):
        result = "High BP"
        data, phy, medi, nutri, meds = rec("highbp")
    elif(res[0] == 3):
        result = "LOW BP"
        data, phy, medi, nutri, meds = rec("lowbp")
    elif(res[0] == 4):
        result = "High Sugar"
        data, phy, medi, nutri, meds = rec("highsugar")
    elif(res[0] == 5):
        result = "Low Sugar"
        data, phy, medi, nutri, meds = rec("lowsugar")
    elif(res[0] == 6):
        result = "Low Oxygen"
        data, phy, medi, nutri, meds = rec("lowoxy")
    elif(res[0] == 7):
        result = "High Temperature"
        data, phy, medi, nutri, meds = rec("hightemp")
    elif(res[0] == 8):
        result = "Heartbeat is High"
        data, phy, medi, nutri, meds = rec("highheartbeat")
    elif(res[0] == 9):
        result = "Risk"
        data, phy, medi, nutri, meds = rec("risk")
    # result = data.con[res[0]-1]
    # print(phy)
    return render_template('report.html', res = result, zipped_data = zip(vitals, datalist.vals), data = data, phy = phy, meds = meds, medi = medi, nutri=nutri)

@app.route('/forms', methods=['POST', 'GET'])
def form():
    return render_template('forms.html')

def rec(stri):
    parsed = file.parsed[stri]
    physical = file.physical[stri]
    meditation = file.meditation[stri]
    nutris = file.nutris[stri]
    meds = file.meds[stri]
    print(nutris)
    return parsed, physical, meditation, nutris, meds

@app.route('/tips', methods=['POST', 'GET'])
def tips():
    return render_template('tips.html')

@app.route('/posts', methods=['POST', 'GET'])
def posts():
    return render_template('post.html')

@app.route('/post1', methods=['POST', 'GET'])
def post1():
    return render_template('post1.html')

@app.route('/post2', methods=['POST', 'GET'])
def post2():
    return render_template('post2.html')

@app.route('/post3', methods=['POST', 'GET'])
def post3():
    return render_template('post3.html')



@app.route('/about', methods=['POST', 'GET'])
def about():
    return render_template('about.html')

@app.route('/extended_about', methods=['POST', 'GET'])
def ex_ab():
    return render_template('extended_about.html')

@app.route('/recommendations', methods=['POST', 'GET'])
def recommend():
    return render_template('recommendations.html')

@app.route('/faqs', methods=['POST', 'GET'])
def faqs():
    return render_template('faq.html')


@app.route('/log',methods=['POST','GET'])
def log():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
    return render_template('log.html',form=form)

@app.route('/logout',methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('logi'))

@app.route('/register', methods=['POST','GET'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('logi'))

    return render_template('register.html', form=form)

@app.route('/dashboard',methods=['POST','GET'])
@login_required
def dashboard():
    return render_template('dashboard.html')

    if form.validate_on_submit():
      hashed_password = bcrypt.generate_password_hash(form.password.data)
      new_user = User(username=form.username.data, password=hashed_password)
      db.session.add(new_user)
      db.session.commit()
      return redirect(url_for('log'))

    return render_template('register.html',form=form)

def predict(g,a,s,h,hr,gl,sp,temp):
    p = np.array([[g,a,s,h,hr,gl,sp,temp]])
    pickled_model = pickle.load(open('hhcs_rfc.sav', 'rb'))

    return(pickled_model.predict(p))

if __name__ == '__main__':
    app.run(debug=True)