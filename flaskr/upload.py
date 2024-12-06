import os
from flask import Blueprint, Flask, flash, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

from flaskr.auth import login_required

UPLOAD_FOLDER = 'Logs'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','log'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
bp = Blueprint('upload', __name__, url_prefix='/upload')
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@login_required
@bp.route('/', methods=['GET', 'POST'])
def upload_file(): 
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
            flash(f"File '{filename}' uploaded successfully!")
            return redirect(url_for('upload.download_file', name=filename))
    
    
    return render_template('upload.html')
    
from flask import send_from_directory

@bp.route('/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

bp.add_url_rule(
    "/<name>", endpoint="download_file", build_only=True
)