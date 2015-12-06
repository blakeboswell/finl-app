from flask import Flask, render_template, request
from plot import create_plot

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == 'POST' and 'symbol' in request.form:
		try:
			script, div = create_plot(request.form['symbol'].upper())
			return render_template('index.html', plot_script=script, plot_div=div)
		except:
			return render_template('index.html')	
	else:
		return render_template('index.html')


if __name__ == '__main__':
	app.run()
