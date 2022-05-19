import mpld3
from matplotlib.figure import Figure
from pycalphad import Database, binplot
import pycalphad.variables as v
from flask import request, app, jsonify
from  dataBase import check_database
from constants import HTTP_400_BAD_REQUEST

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
    if start and end and step:
        graph = mpld3.fig_to_html(plotting(first_elem, second_elem, va, start, end, step, vx, lines, dotes))
        return jsonify({'html_plot': graph})
    else:
        return jsonify({'error': HTTP_400_BAD_REQUEST}), 


def plotting(first_elem, second_elem, va, start, end, step, vx, lines, dotes):
    db = Database(check_database.db)
    if va:
        elements = [first_elem, second_elem, 'VA']
    else:
        elements = [first_elem, second_elem]
    line = False
    dote = False
    if lines:
        line = True
    if dotes:
        dote = True
        start = float(str(start.replace(',', '.')))
        end = float(str(end.replace(',', '.')))
        step = float(str(step.replace(',', '.')))
    phases= list(check_database.db.phases.keys())
    fig = Figure()
    axis = fig.add_subplot(2, 1, 1)
    axis.set_title("title")
    axis.set_xlabel("x-axis")
    axis.set_ylabel("y-axis")
    axis.grid()
    axes = fig.gca()
    binplot(db, 
            elements,
            phases,
            {v.X(vx):(start, end, step), v.T: (300, 2500, 10), v.P:101325, v.N: 1},
            plot_kwargs={'ax': axes, 
            'tielines':line,
            'scatter':dote
            })
    return fig