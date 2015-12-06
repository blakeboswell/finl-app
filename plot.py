from flask import Markup
import requests

from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import components

import numpy as np
import pandas as pd

def create_plot(symbl):
	'''
	build bokeh plot, return (script, div)
	'''
	plot = figure(title=symbl + ' Closing Price', tools='wheel_zoom, pan', 
				  responsive=True, plot_width=1000,
				  plot_height=500, x_axis_type='datetime')
	df = get_data(symbl)
	plot.line(df['date'], df['close'])
	script, div = components(plot, CDN)

	return Markup(script), Markup(div)


def get_data(symbl):
	'''
	get stock data from quandl, return date and {date, close}
	'''
	api_url = 'https://www.quandl.com/api/v1/datasets/WIKI/%s.json' % symbl
	session = requests.Session()
	session.mount('http://', requests.adapters.HTTPAdapter(max_retries=3))
	raw_json = session.get(api_url).json()
	# raw_json['data']: [date, open, high, low, close, volume, ex-dividend, splitratio, adjopen, adjhigh, adjlow, adjclose, adjvolume]
	df = pd.DataFrame({
			'date' : np.array([x[0] for x in raw_json['data']], dtype=np.datetime64),
			'close' : np.array([x[4] for x in raw_json['data']]),
		})
	return df