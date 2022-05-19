from flask import Flask, render_template, redirect
from flask import request
import mpld3
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from pycalphad import Database, binplot
import pycalphad.variables as v
import random as rd


app = Flask(__name__)
db = Database("/Users/uliaandreeva/projects/api/databases/AlSi-86Mey.tdb")


@app.route('/')
def start():
    return render_template('form.html')


@app.route('/plot', methods=["GET", "POST"])
def get():
    first_elem = request.form.get('first_element')
    second_elem = request.form.get('second_element')
    va = request.form.get('VA')
    start = request.form.get('start')
    end = request.form.get('end')
    step = request.form.get('step')
    vx = request.form.get('Vx')
    lines = request.form.get('tielines')
    dotes = request.form.get('scatter')
    graph1 = mpld3.fig_to_html(plotting(first_elem, second_elem, va, start, end, step, vx, lines, dotes))
    html_file = open('./templates/pplot.html', 'w')
    html_file.write(graph1)
    html_file.close()
    return redirect("http://127.0.0.1:5500/templates/pplot.html")



def plotting(first_elem, second_elem, va, start, end, step, vx, lines, dotes):
    fig = Figure()
    axis = fig.add_subplot(2, 1, 1)
    axis.set_title("title")
    axis.set_xlabel("x-axis")
    axis.set_ylabel("y-axis")
    axis.grid()
    axes = fig.gca()
    #
    # Compute the phase diagram and plot it on the existing axes using the `plot_kwargs={'ax': axes}` keyword argument
    binplot(db, 
            ['AL', 'SI', 'VA'],  #все элементы, которые здесь представлены, должны изначально находиться хотя бы в одной фазе словаря db.phases, 
            db.phases,  #здесь по дефолту мы используем  все фазы , которые есть в файле, но у пользователя должна быть возможность вручную выключить те фазы из списка которые он захочет
            {v.X('AL'):(0, 1, 0.07), v.T: (300, 2500, 10), v.P:101325, v.N: 1},  #внутри v.X() lдолжен находиться любой элемент из списка на две строчки выше, Но не 'VA'. У пользователя должна быть возможность выбрать
            plot_kwargs={'ax': axes, 
            'tielines':True,  #выбирает показывать ли горизонтальные зеленые линии
            'scatter':True  #выбирает соединять ли точки линией
            })
    return fig


if __name__ == '__main__':
        app.run()
