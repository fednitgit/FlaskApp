import io
import random
from flask import Flask
from flask import Markup
from flask import Flask
from flask import render_template
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

app = Flask(__name__)
@app.route("/") 
def home_view(): 
        return "<h1>Welcome to My website!</h1><br/><a href='/plot.png'>1. Chart.js Chart</a><br/><a href='/plot.png'>2. Plot Chart</a>"

@app.route("/HTMLChart")
def chart():
  labels = ["January","February","March","April","May","June","July","August"]
  values = [10,9,8,7,6,4,7,8]
  return render_template('chart.html', values=values, labels=labels)

@app.route('/plot.png')
def plot_png():
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_figure():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    xs = range(100)
    ys = [random.randint(1, 50) for x in xs]
    axis.plot(xs, ys)
    return fig
@app.route("/PlotChart")
def plotchart():
  return render_template('plotChart.html')

if __name__ == "__main__":
  app.run()
