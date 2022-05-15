from http.client import HTTPException
import os, json, csv
from flask import Flask, render_template, request, jsonify
from benfordslaw import benfordslaw
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import uuid
import matplotlib



app = Flask(
    __name__,
    static_folder="static",
    template_folder="templates"
)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['SECRET_KEY'] = 'secret!'

def getFolderPath():
    return os.path.dirname(os.path.abspath(__file__))

@app.errorhandler(Exception)
def handle_error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    return jsonify(error=str(e)), code
    
@app.route('/')
def home_page():
    return render_template('index.html')


@app.route('/getBenfordAnalysis', methods=['POST'])
def getBenfordAnalysis():
    data = request.get_json()  
    X = np.asarray(data)
    bl = benfordslaw(alpha=0.05, method='chi2')
    results = bl.fit(X)
    figures = bl.plot(title='Random data')

    fig = figures[0]
    canvas = FigureCanvas(fig)
    folder = getFolderPath() 
    fileid = str(uuid.uuid4())
    canvas.print_figure(folder + r'/static/' + fileid + '.png')
    #image = np.frombuffer(canvas.tostring_rgb(), dtype='uint8')
    return fileid

if __name__ == '__main__' :
    # app.run()
    matplotlib.use('Agg')
    app.run(host="0.0.0.0",port=80)
