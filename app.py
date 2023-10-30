import os
from flask import Flask, request, render_template, send_from_directory, url_for

app = Flask(__name__)

# Specify the folder where uploaded photos will be stored
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create a list to store uploaded file names
uploaded_files = []

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']

    if file.filename == '':
        return "No selected file"

    if file:
        # Save the uploaded file to the upload folder
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        
        # Append the uploaded file name to the list
        uploaded_files.append(file.filename)
        
        return render_template('upload_success.html')

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/list')
def list_files():
    return render_template('list.html', files=uploaded_files)

if __name__ == '__main__':
    app.run(debug=True)
