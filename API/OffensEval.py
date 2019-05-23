import argparse
import os
import zipfile
from flask import Flask, request, Response, redirect, url_for, render_template, send_file
from werkzeug.utils import secure_filename
from API.scripts.tokens_and_lemmas_module import compute_tokens_and_lemmas
from API.scripts.punctuation_module import compute_punctuation
from API.scripts.upper_lower_module import compute_upper_lower
from API.scripts.sentiments_module import compute_sentiments
from API.scripts.compute_word_scores import compute_word_scores
from API.scripts.model_prediction import compute_prediction

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = set(['csv'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def render_main():
    return render_template('main.html')


@app.route('/word_scores')
def render_word_scores():
    return render_template('word_scores.html')


@app.route('/get_word_scores', methods=['GET', 'POST'])
def get_word_scores():
    if request.method == 'POST':
        f = request.files.getlist('file')
        if len(f) == 2:
            if allowed_file(f[0].filename) and allowed_file(f[1].filename):
                if not os.path.exists(app.config['UPLOAD_FOLDER'] + request.remote_addr):
                    os.mkdir(app.config['UPLOAD_FOLDER'] + request.remote_addr)
                path = app.config['UPLOAD_FOLDER'] + request.remote_addr
                secured_filenames = []
                for file in f:
                    filename = secure_filename(file.filename)
                    secured_filenames.append(filename)
                    file.save(path + "/" + filename)
                try:
                    compute_word_scores(path + "/" + secured_filenames[0], path + "/" + secured_filenames[1],
                                        path + "/result_words.csv")
                except Exception:
                    os.remove(path + "/" + secured_filenames[0])
                    os.remove(path + "/" + secured_filenames[1])
                    return Response("File does not have required structure"), 400
                os.remove(path + "/" + secured_filenames[0])
                os.remove(path + "/" + secured_filenames[1])
                return send_file(path + "/result_words.csv", mimetype="text/csv",
                                 attachment_filename='result_words.csv', as_attachment=True), 200
            return Response('Only .csv files are allowed.'), 400
        return Response('Two files are required'), 400
    return redirect(url_for('render_word_scores'))


@app.route('/prediction')
def render_prediction():
    return render_template('prediction.html')


@app.route('/get_prediction', methods=['GET', 'POST'])
def get_prediction():
    # get prediction from existing model
    if request.method == 'POST':
        return
    return redirect(url_for('render_prediction'))


@app.route('/punctuation_scores')
def render_punctuation():
    return render_template('punctuation_scores.html')


@app.route('/get_punctuation_scores', methods=['GET', 'POST'])
def get_punctuation():
    if request.method == "POST":
        f = request.files['file']
        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            if not os.path.exists(app.config['UPLOAD_FOLDER'] + request.remote_addr):
                os.mkdir(app.config['UPLOAD_FOLDER'] + request.remote_addr)
            path = app.config['UPLOAD_FOLDER'] + request.remote_addr
            f.save(path + "/" + filename)
            try:
                compute_punctuation(path + "/" + filename, path + "/result_punctuation.csv")
            except Exception:
                os.remove(path + "/" + filename)
                return Response("File does not have required structure"), 400
            os.remove(path + "/" + filename)
            return send_file(path + "/result_punctuation.csv", mimetype="text/csv",
                             attachment_filename='result_punctuation.csv', as_attachment=True), 200
    return redirect(url_for('render_punctuation'))


@app.route('/sentiment_scores')
def render_sentiments():
    return render_template('sentiment_scores.html')


@app.route('/get_sentiments_scores', methods=['GET', 'POST'])
def get_sentiments():
    if request.method == 'POST':
        f = request.files['file']
        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            if not os.path.exists(app.config['UPLOAD_FOLDER'] + request.remote_addr):
                os.mkdir(app.config['UPLOAD_FOLDER'] + request.remote_addr)
            path = app.config['UPLOAD_FOLDER'] + request.remote_addr
            f.save(path + "/" + filename)
            try:
                compute_sentiments(path + "/" + filename, path + "/result_sentiments.csv")
            except Exception:
                os.remove(path + "/" + filename)
                return "File does not have required structure", 400
            os.remove(path + "/" + filename)
            return send_file(path + "/result_sentiments.csv", mimetype="text/csv",
                             attachment_filename='result_sentiments.csv', as_attachment=True), 200
    return redirect(url_for('render_sentiments'))


@app.route('/tokens_lemmas')
def render_tokens_lemmas():
    return render_template('tokens_lemmas.html')


@app.route('/get_tokens_lemmas', methods=['GET', 'POST'])
def get_tokens_lemmas():
    if request.method == "POST":
        f = request.files['file']
        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            if not os.path.exists(app.config['UPLOAD_FOLDER'] + request.remote_addr):
                os.mkdir(app.config['UPLOAD_FOLDER'] + request.remote_addr)
            path = app.config['UPLOAD_FOLDER'] + request.remote_addr
            f.save(path + "/" + filename)
            try:
                compute_tokens_and_lemmas(path + "/" + filename, path + "/result_tokens.csv",
                                          path + "/result_lemmas.csv")
            except Exception:
                os.remove(path + "/" + filename)
                return "File does not have required structure", 400
            with zipfile.ZipFile(path + '/tokens_lemmas_results.zip', 'w') as myzip:
                myzip.write(path + "/result_tokens.csv", "result_tokens.csv")
                myzip.write(path + "/result_lemmas.csv", "result_lemmas.csv")
            os.remove(path + "/" + filename)
            os.remove(path + "/result_tokens.csv")
            os.remove(path + "/result_lemmas.csv")
            return send_file(path + "/tokens_lemmas_results.zip"), 200
    return redirect(url_for('render_tokens_lemmas'))


@app.route('/upper_lower_scores')
def render_upper_lower_scores():
    return render_template('upper_lower_scores.html')


@app.route('/get_upper_lower_scores', methods=['GET', 'POST'])
def get_upper_lower():
    if request.method == "POST":
        f = request.files['file']
        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            if not os.path.exists(app.config['UPLOAD_FOLDER'] + request.remote_addr):
                os.mkdir(app.config['UPLOAD_FOLDER'] + request.remote_addr)
            path = app.config['UPLOAD_FOLDER'] + request.remote_addr
            f.save(path + "/" + filename)
            try:
                compute_upper_lower(path + "/" + filename, path + "/result_upper_lower_scores.csv")
            except Exception:
                os.remove(path + "/" + filename)
                return "File does not have required structure", 400
            os.remove(path + "/" + filename)
            return send_file(path + "/result_upper_lower_scores.csv", mimetype="text/csv",
                             attachment_filename='result_upper_lower_scores.csv', as_attachment=True), 200
    return redirect(url_for('render_upper_lower_scores'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--port',
        type=int,
        default=5000,
        help='Value of the port used by OffensEval.'
    )
    parser.add_argument(
        '--host',
        type=str,
        default='localhost',
        help='Value of the host used by OffensEval.'
    )
    args = parser.parse_args()
    app.run(host=args.host, port=args.port, threaded=True, debug=True)
