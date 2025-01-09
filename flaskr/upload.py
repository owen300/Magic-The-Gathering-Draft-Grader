import os
from flask import Blueprint, Flask, flash, g, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

from flaskr.auth import login_required
from Parser import logHandler

UPLOAD_FOLDER = 'Logs'#folder for the logs

ALLOWED_EXTENSIONS = {'txt','log'}#we only want log files being uploaded

logs=logHandler()#create an instance of the loghandler

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER#define upload folder

bp = Blueprint('upload', __name__, url_prefix='/upload')

def allowed_file(filename):#checks if the file is one of the right type
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@bp.route('/', methods=['GET', 'POST'])
@login_required
def upload_file(): #upload file page
    if request.method == 'POST':
        
        if 'file' not in request.files:#checks if user has uploaded the file
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']#get the file
        
        
        if file.filename == '':#makes sure the file was selected
            flash('No selected file')
            return redirect(request.url)
        
       
        if file and allowed_file(file.filename):#if the file exists and its a log
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))# save the file
            flash(f"File '{filename}' uploaded successfully!") 
            logs.add_user_data(username=g.user['username'], data=filename)#put the filename in the users part of the json
            #return redirect(url_for('Home.index', name=filename))
    
    
    return render_template('upload.html')
    
#from flask import send_from_directory

# @bp.route('/<name>')
# def download_file(name):
#     return send_from_directory(app.config["UPLOAD_FOLDER"], name)

# bp.add_url_rule(
#     "/<name>", endpoint="download_file", build_only=True
# )