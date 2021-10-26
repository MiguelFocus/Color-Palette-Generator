import os
from werkzeug.utils import secure_filename
from flask import Flask, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from colorthief import ColorThief
from wtforms import FileField, SubmitField


# Create From
class UploadfileForm(FlaskForm):
    file = FileField("File")
    submit = SubmitField("Submit")


# Chose the folder where you want to save the images, and the allowed extensions
UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


# Initiate Flask and Bootstrap
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = "YOUR_KEY"
Bootstrap(app)

# This is the image that first shows as a demonstration
filename = "Astronauta.jpg"


def allowed_file(file_name):
    """ Checks if the file is in the allowed extensions"""
    if file_name.rsplit('.', 1)[1].lower() not in ALLOWED_EXTENSIONS:
        flash("File not supported.")
    return '.' in file_name and \
           file_name.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def rgb_to_hex(rgb):
    """ RGB to HEX"""
    return '#' + '%02x%02x%02x' % rgb


def check_colors(file):
    """Checks the most used colors"""
    color_thief = ColorThief(f"static/images/{file}")
    palette = color_thief.get_palette(color_count=10)
    hex_palette = []
    for color in palette:
        hex_color = rgb_to_hex(color)
        hex_palette.append(hex_color)
    return hex_palette


@app.route("/", methods=["GET", "POST"])
def demo():
    global filename
    form = UploadfileForm()
    file = form.file.data
    palette1 = check_colors(filename)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        palette2 = check_colors(filename)
        return redirect(url_for('demo', filename=filename, colors=palette2))
    return render_template("index.html", form=form, filename=filename, colors=palette1)


if __name__ == "__main__":
    app.run(debug=True)
