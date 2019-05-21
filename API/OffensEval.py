import argparse
import os
from flask import Flask, request, Response, flash, redirect, url_for, render_template
from werkzeug.utils import secure_filename


app = Flask(__name__)
UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = set(['csv'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/word_scores')
def render_word_scores():
    return render_template('word_scores.html')


@app.route('/get_word_scores', methods=['GET', 'POST'])
def get_word_scores():
    return


# @app.route('/prediction')
# def render_prediction():
#     return render_template('prediction.html')
#
#
# @app.route('/get_prediction', methods=['GET', 'POST'])
# def get_prediction():
#     # train the model and then get prediction
#     return
#
#
# @app.route('/data_processing')
# def render_data_processing():
#     return render_template('data_processing.html')
#
#
# @app.route('/get_data_processing', methods=['GET', 'POST'])
# def get_processed_data():
#     return


@app.route('/punctuation_scores')
def render_punctuation():
    return render_template('punctuation_scores.html')


@app.route('/get_punctuation_scores', methods=['GET', 'POST'])
def get_punctuation():
    return


@app.route('/sentiment_scores')
def render_sentiments():
    return render_template('sentiment_scores.html')


@app.route('/get_sentiments_scores', methods=['GET', 'POST'])
def get_sentiments():
    return


@app.route('/tokens_lemmas')
def render_tokens_lemmas():
    return render_template('tokens_lemmas.html')


@app.route('/get_tokens_lemmas', methods=['GET', 'POST'])
def get_tokens_lemmas():
    if request.method == "POST":
        f = request.files['file']
        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            if not os.path.exists(app.config['UPLOAD_FOLDER']+request.remote_addr):
                os.mkdir(app.config['UPLOAD_FOLDER']+request.remote_addr)
            f.save(app.config['UPLOAD_FOLDER']+request.remote_addr+"/"+filename)
            return Response('file uploaded successfully'), 200


@app.route('/upper_lower_scores')
def render_upper_lower_scores():
    return render_template('upper_lower_scores.html')


@app.route('/get_upper_lower_scores', methods=['GET', 'POST'])
def get_upper_lower():
    return


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
    app.run(host=args.host, port=args.port, threaded=True)
