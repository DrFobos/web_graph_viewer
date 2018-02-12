import excel_reader
from db_function import write2db, read_from_db
from additional_func import allowed_file
from flask import Flask, request, redirect, render_template, flash, jsonify


ID = 1
app = Flask(__name__)


# generate home page of application
@app.route('/')
def index():
    global ID
    data = sorted(read_from_db(), key=lambda k: k['id'], reverse=True)
    nodes = next(item for item in data if item["id"] == ID)['content']['nodes']
    edges = next(item for item in data if item["id"] == ID)['content']['edges']
    return render_template('home.html', data=data, nodes=nodes, edges=edges)


# process upload request from client and return data to rewrite some elements on web page
@app.route('/upload_file', methods=['POST'])
def upload_file():
    global ID

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            nodes, edges = excel_reader.read_excel_file(file, excel_reader.clear_branches)
            ID = write2db(file, nodes, edges)

    data = read_from_db(id_asked=ID)

    return jsonify(data[0])


# process request to change active graph and return data to draw new one
@app.route('/change_graph', methods=['POST'])
def change_graph():
    global ID
    ID = int(request.form['send_id'])
    data = read_from_db(id_asked=ID)
    nodes = data[0]['content']['nodes']
    edges = data[0]['content']['edges']

    return jsonify({
        'nodes': nodes,
        'edges': edges
    })

# Uncomment to prevent browser caching and see changes in static files

import os
from flask import url_for


@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    app.run(port=2016, debug=True)
