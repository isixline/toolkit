from flask import Flask, send_from_directory
from flask_cors import CORS
from process import collate_graph

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = './temp'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/files/<path:filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# return utf-8 encoded json
@app.route('/graph')
def graph():
    graph = collate_graph()
    return graph

if __name__ == '__main__':
    app.run(port=5002)
