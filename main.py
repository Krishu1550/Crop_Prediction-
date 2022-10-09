from flask import Flask,render_template,redirect,request,url_for, Markup
import numpy as np
import pandas as pd
# This is a sample Python script.
# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from utils import fetch_city_data, model_value, fertilizer_dic

app = Flask(__name__)

@app.route('/')
def home():
   return render_template('index.html')
@app.route('/crop')
def crop():
   return render_template('crop.html')
@app.route('/fertilizer')
def fertilizer():
   return render_template('fertilizer.html')


@app.route('/crop_prediction',methods=['POST','GET'])
def crop_prediction():
   final_prediction=None
   if request.method == 'POST':
      N = int(request.form['nitrogen'])
      P = int(request.form['phosphorous'])
      K = int(request.form['pottasium'])
      ph = float(request.form['ph'])
      rainfall = float(request.form['rainfall'])

      # state = request.form.get("stt")
      city = request.form.get("city")
      if fetch_city_data(city) != None:
         temperature, humidity = fetch_city_data(city)
         data = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
         my_prediction = model_value(data)
         final_prediction = my_prediction[0]
   return render_template('crop_result.html',prediction=final_prediction)


@app.route('/fertilizer_predict',methods=['POST','GET'])
def fertilizer_predict():

    crop_name = str(request.form['cropname'])
    N = int(request.form['nitrogen'])
    P = int(request.form['phosphorous'])
    K = int(request.form['potassium'])


    df = pd.read_csv('./Model/fertilizer.csv')

    nr = df[df['Crop'] == crop_name]['N'].iloc[0]
    pr = df[df['Crop'] == crop_name]['P'].iloc[0]
    kr = df[df['Crop'] == crop_name]['K'].iloc[0]

    n = nr - N
    p = pr - P
    k = kr - K
    temp = {abs(n): "N", abs(p): "P", abs(k): "K"}
    max_value = temp[max(temp.keys())]
    if max_value == "N":
        if n < 0:
            key = 'NHigh'
        else:
            key = "Nlow"
    elif max_value == "P":
        if p < 0:
            key = 'PHigh'
        else:
            key = "Plow"
    else:
        if k < 0:
            key = 'KHigh'
        else:
            key = "Klow"

    response = Markup(str(fertilizer_dic[key]))

    return render_template('fertilizer_result.html', recommendation=response)

@app.route('/disease')
def disease():
   return 'Site is under construction'


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
   app.run('0.0.0.0', port=80, debug=True)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/