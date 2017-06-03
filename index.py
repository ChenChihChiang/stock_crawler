from flask import Flask, render_template, request, redirect, url_for, send_from_directory, g
from bs4 import BeautifulSoup
import os
import requests
import pandas as pd
import numpy
import json

df = pd.DataFrame()

prices = dict()

app = Flask(__name__)

dirpath = os.path.join(app.root_path,'download')

@app.route('/')
def index():
    
    filename = request.args.get('filename')

    return render_template('index.html', filename=filename)

@app.route('/crawler', methods=['POST'])
def crawler():

	#filename = request.args.get('filename')
	num = request.form.get('num')

	for j in range(2001,2018):

		for i in range(1,13):

			if i > 9 :

				res_post = requests.post("http://www.tse.com.tw/exchangeReport/STOCK_DAY_AVG?response=json&date="+str(j)+str(i)+"01&stockNo="+str(num)+"&_=1496303801885")	
			
			else:

				res_post = requests.post("http://www.tse.com.tw/exchangeReport/STOCK_DAY_AVG?response=json&date="+str(j)+"0"+str(i)+"01&stockNo="+str(num)+"&_=1496303801885")

			stock_data = json.loads(res_post.text)

			if "data" in stock_data:
			
				price = stock_data['data']
				price.pop()
				price = dict(price)
				prices.update(price)

	pricesjson = json.dumps(prices)

	with open("./download/"+str(num)+".txt", 'w') as f:
		f.write(pricesjson)

	return render_template('index.html', filename=prices, num=num)

@app.route('/download', methods=['POST'])
def download():

	filename = request.form.get('num')+".txt"

	#filename = filename+".txt"

	return send_from_directory(dirpath,filename,as_attachment=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=7000,debug=True)
    