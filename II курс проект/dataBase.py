from matplotlib.style import available
from pycalphad import Database
from requests import get
from flask import jsonify, app, get, post
import os

db = []

@app.get('/db')
def check_database():
    for filename in os.listdir("/Users/uliaandreeva/projects/api/databases"):
       db.append(filename)
    available_bases = db

    if name_of_db in available_bases:
        currentdb = Database("/databases" + name_of_db)
        elements = currentdb.elements
        for i in range(0, len(elements)):
            if elements[i] == "VA" or elements[i] == "/":
                elements.pop(i)
        return jsonify({
        'elements': elements,
        'db': currentdb,
        })
    else:
        return jsonify({'error': 'This database is currently unavailable'})






        