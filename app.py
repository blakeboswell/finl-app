from flask import Flask, render_template, request
from plot import create_plot
import pandas as pd

app = Flask(__name__)
tickers = pd.read_csv('https://s3.amazonaws.com/quandl-static-content/Ticker+CSV%27s/WIKI_tickers.csv')


@app.route('/', methods=['GET', 'POST'])
def index():
	"""
	the main page of the app

	POST:
		validate input symbol and create heroku plot

	GET:
		load search bar

	"""
	if request.method == 'POST' and 'symbol' in request.form:
		symbl = request.form['symbol'].upper()
		if 'WIKI/'+ symbl in tickers['quandl code'].values:
			try:
				name = tickers.loc[tickers['quandl code'] == 'WIKI/' + symbl, 'name'].values[0]
				script, div = create_plot(symbl, name)
				return render_template('index.html', place_holder= 'Input Stock Symbol...', 
							plot_script=script, plot_div=div)
			except:
				return render_template('index.html', 
					place_holder='An error has occured.')
		else:
			return render_template('index.html', 
				place_holder='Stock Symbol not recognized. Please try again...')
	else:
		return render_template('index.html', place_holder='Input Stock Symbol...')


if __name__ == '__main__':
	app.run(debug=True)
