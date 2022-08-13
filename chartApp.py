import io
import random
from flask import Flask
from flask import Markup
from flask import Flask
from flask import render_template
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, TextBox, RangeSlider
import numpy as np
import mpld3

app = Flask(__name__)
@app.route("/") 
def home_view(): 
        return "<h1>Welcome to My website!</h1><br/><a href='/HTMLChart'>1. Chart.js Chart</a><br/><a href='/PlotChart'>2. Plot Chart</a><br/><a href='/InteractiveGraph'>3. Interactive Graph</a>"

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

@app.route("/InteractiveGraph")
def renderInteractiveGraph():
         g = InteractiveGraph()
         mpld3.save_html(g,"test.html")
         mpld3.fig_to_html(g)
         return 'test.html'

class InteractiveGraph:
  def __init__(self, point_amt = 5):
    self.point_amt = point_amt
    self.function = "x**2"
    self.x_min = 0
    self.x_max = 10
    self.draw_gui()
    
    plt.show()
        
  def draw_gui(self):
    """Add GUI elements to the figure"""
    self.fig = plt.figure()
    self.ax = self.fig.subplots()
    plt.subplots_adjust(left = 0.15, bottom = 0.25)
    self.ax.set_title("Dynamic Graph")
    self.ax.set_xlabel("x axis")
    self.ax.set_ylabel("y axis")
    x, y = self.get_coords()
    self.plot, = self.ax.plot(x, y, color="blue", marker="o")
    axesFunctionText = plt.axes([0.1, 0.01, 0.5, 0.05])
    self.textFunction = TextBox(axesFunctionText, label="y =", initial=self.function)
    self.textFunction.on_submit(self.get_function)
    axesXRange = plt.axes([0.1, 0.08, 0.5, 0.05])
    self.sliderXRange = RangeSlider(axesXRange, label="x range", valmin=0, valmax=50, valinit=(self.x_min, self.x_max), valstep=1)
    self.sliderXRange.on_changed(self.set_x_range)
    self.pointsLabel = plt.figtext(0.75, 0.08, "Points: "+str(self.point_amt))
    axesDecrease = plt.axes([0.70, 0.01, 0.1, 0.05])
    axesIncrease = plt.axes([0.81, 0.01, 0.1, 0.05])
    self.btnDecrease = Button(axesDecrease, 'Decrease',color="red")
    self.btnIncrease = Button(axesIncrease, 'Increase', color = "green")
    self.btnIncrease.on_clicked(self.increase)
    self.btnDecrease.on_clicked(self.decrease)
        
  def get_coords(self):
    """Get coordinates for the points to draw"""
    xs = np.linspace(self.x_min, self.x_max, self.point_amt)
    ys = [eval(self.function) for x in xs]
    return xs, ys
  def set_x_range(self, event):
    """Set the visible range on the x axis"""
    self.x_min = event[0]
    self.x_max = event[1]
    self.draw()
  def increase(self, event):
    """Increase the number of points"""
    self.point_amt += 1
    self.pointsLabel.set_text("Points: "+str(self.point_amt))
    self.draw()
  def decrease(self, event):
    """Decrease the number of points"""
    if self.point_amt > 1:
        self.point_amt -= 1
        self.pointsLabel.set_text("Points: "+str(self.point_amt))
        self.draw()
  def get_function(self, text):
    """Update the function"""
    if self.function != text:
      self.function = text
      self.draw()
  def draw(self):
    """Redraw the plot"""
    x, y = self.get_coords()
    self.plot.set_xdata(x)
    self.plot.set_ydata(y)
    x_incr = (self.x_max-self.x_min)/10
    y_incr = (max(y) - min(y))/10
    self.ax.set(xlim=(self.x_min-x_incr,self.x_max+x_incr), ylim=(min(y)-y_incr, max(y)+y_incr))




if __name__ == "__main__":
  app.run()
