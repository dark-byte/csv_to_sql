from flask import Flask, render_template, send_from_directory, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired
from main import process_csv

ALLOWED_EXT = set(['csv'])

def allowed_files(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT

app = Flask(__name__)
app.config['SECRET_KEY'] = "mysecretkeyisthis"
app.config['UPLOAD_FOLDER'] = 'static/files'

class UploadFileForm(FlaskForm):
    file = FileField('File', validators=[InputRequired()])
    submit = SubmitField("Upload File")

@app.route("/", methods = ['GET', 'POST'])
def home():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        if file and allowed_files(file.filename):
            save_location = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
            file.save(save_location)
            output_file = process_csv(save_location)
            return send_from_directory('static/output', output_file)
    return render_template('index.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
