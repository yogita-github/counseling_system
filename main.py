from flask import Flask, render_template, url_for ,request,redirect
import numpy as np
import pickle
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE
import data
import file
import datalist
from datetime import date

import pandas as pd

app = Flask(__name__)


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
    name = request.form['name']
    town = request.form['town']
    pin = request.form['pin']
    country = request.form['country']
    vitals = [age, sbp, hbp, h_rate, glc, spo2, temp_c]
    res = predict(gender,age, sbp, hbp, h_rate, glc, spo2, temp)
    if (res[0] == 1):
        result = "healthy"
        # this every line is changed
        data, phy, medi, nutri, meds, syms = rec("healthy")
    elif(res[0] == 2):
        result = "High BP"
        data, phy, medi, nutri, meds, syms = rec("highbp")
    elif(res[0] == 3):
        result = "LOW BP"
        data, phy, medi, nutri, meds, syms = rec("lowbp")
    elif(res[0] == 4):
        result = "High Sugar"
        data, phy, medi, nutri, meds, syms = rec("highsugar")
    elif(res[0] == 5):
        result = "Low Sugar"
        data, phy, medi, nutri, meds, syms = rec("lowsugar")
    elif(res[0] == 6):
        result = "Low Oxygen"
        data, phy, medi, nutri, meds, syms = rec("lowoxy")
    elif(res[0] == 7):
        result = "High Temperature"
        data, phy, medi, nutri, meds, syms = rec("hightemp")
    elif(res[0] == 8):
        result = "Heartbeat is High"
        data, phy, medi, nutri, meds, syms = rec("highheartbeat")
    elif(res[0] == 9):
        result = "Risk"
        data, phy, medi, nutri, meds, syms = rec("risk")
    # result = data.con[res[0]-1]
    # print(phy)
    # a variable syms is added
    if(gender == '1'):
        g = 'female'
    elif(gender == '0'):
        g='male'
    return render_template('report.html', res = result, zipped_data = zip(vitals, datalist.vals), data = data, phy = phy, meds = meds, medi = medi, nutri=nutri, syms=syms, name = name, pin = pin, country = country, gender = g, town = town)

@app.route('/forms', methods=['POST', 'GET'])
def form():
    return render_template('forms.html')

def rec(stri):
    parsed = file.parsed[stri]
    physical = file.physical[stri]
    meditation = file.meditation[stri]
    nutris = file.nutris[stri]
    meds = file.meds[stri]
    syms = file.syms[stri] #this line is added
    return parsed, physical, meditation, nutris, meds, syms 

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



def predict(g,a,s,h,hr,gl,sp,temp):
    p = np.array([[g,a,s,h,hr,gl,sp,temp]])
    pickled_model = pickle.load(open('hhcs_rfc.sav', 'rb'))

    return(pickled_model.predict(p))

if __name__ == '__main__':
    app.run(debug=True)