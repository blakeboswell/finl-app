from flask import Markup
import requests
import datetime

from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import components
from bokeh.models import NumeralTickFormatter

import numpy as np
import pandas as pd

def create_plot(symbl, name):
	"""
	method for creating bokeh plot

	Args:
		symbl: valid stock ticker symbol
		name: company name, used for plot title

	Returns:
		(script, div) bokeh script and div markup

	"""
	plot = figure(title=name, tools='wheel_zoom, pan', 
				  responsive=True, plot_width=1000,
				  plot_height=500, x_axis_type='datetime')
	df = get_data(symbl)
	plot.line(df['date'], df['close'], legend='Closing Price')
	plot.legend.orientation = 'top_left'
	plot.legend.background_fill_alpha = 0.0
	plot.yaxis[0].formatter = NumeralTickFormatter(format='$0.00')
	script, div = components(plot, CDN)
	return Markup(script), Markup(div)


def get_data(symbl):
	"""
	method for requesting data from quandl api
    
	Args:
		symbl: valid stock ticker symbol

	Returns:
		{date, closing price}
       
	"""
	end_date = datetime.datetime.now()
	start_date = end_date + datetime.timedelta(-30)
	api_url = 'https://www.quandl.com/api/v3/datasets/WIKI/%s.json?api_key=t-drH_WSpLdRenh1o86E&start_date=%s&end_date=%s' \
				% (symbl, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
	session = requests.Session()
	session.mount('http://', requests.adapters.HTTPAdapter(max_retries=3))
	raw_json = session.get(api_url).json()['dataset']
	df = pd.DataFrame({
			'date' : [x[0] for x in raw_json['data']],
			'close' : np.array([x[4] for x in raw_json['data']]),
		})
	df['date'] = pd.to_datetime(df['date'])
	return df