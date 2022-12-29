from flask import Flask, redirect, render_template, request, jsonify, flash, url_for, session
from flask_session import Session
from dotenv import load_dotenv
import os
from errors.invalid import InvalidAPIUsage
from utils.check import allowed_file
from werkzeug.utils import secure_filename
from utils.score import get_scores
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


UPLOAD_FOLDER = 'uploads/'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

sess = Session()
sess.init_app(app)

load_dotenv()
@app.errorhandler(404)
def invalid(error):
    return render_template('404.html')

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify(message="Method Not Allowed"), 405

@app.errorhandler(InvalidAPIUsage)
def invalid_usage(error):
    return jsonify(error.to_dict()), 400

@app.route('/api', methods=['POST'])
def score():
    score = get_scores()
    if score > 0.5:
        return redirect(url_for('wrong'))
    else:
        return redirect(url_for('wrong'))


@app.route('/')
def home():
    return redirect('https://preview.webflow.com/preview/fractured-souls?utm_medium=preview_link&utm_source=dashboard&utm_content=fractured-souls&preview=d40a2baecf3512e77a2e7dbd190f3d64&workflow=preview')

@app.route('/success', methods=['GET'])
def success():
    return render_template('success.html')


@app.route('/wrong', methods=['GET'])
def wrong():
    return render_template('wrong.html')


@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('upload',
                                    filename=filename))
    return render_template('upload.html')

@app.route('/docs')
def docs():
    return redirect('https://documenter.getpostman.com/view/18833270/UVeAtoRi')

if __name__ == "__main__":
    app.run()