import json
from flask import Flask, render_template, request, jsonify, url_for, redirect, \
    flash
import numpy as np
from mds_calculator import get_mds

app = Flask(__name__)
app.config['SECRET_KEY'] = 'harp'


@app.route('/', methods=['GET', 'POST'])
def get_graph():
    subjects = [(i, str(f"Subject {i}")) for i in range(1, 317)]
    if request.method == "POST":
        subject_id = request.form["subject_id"]
        data_path = f'subjects_distance_matrix/subject_{subject_id}.json'
        dissimilarity_matrix = np.array(
            json.loads(open(data_path, "r").read()))
        mds_matrix = get_mds(dissimilarity_matrix)
        mds_matix = json.dumps(mds_matrix.tolist())
        return render_template(
            'index.html',
            data=mds_matix,
            subjects=subjects
        )
    return render_template('index.html', subjects=subjects)
