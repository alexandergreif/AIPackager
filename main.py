from flask import Flask, render_template, request, redirect, url_for
from app.orchestrator import run_script_generation
import os

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(os.getcwd(), "app", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('installer')
    if file and file.filename.endswith(('.exe', '.msi')):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        generated_script = run_script_generation(file.filename)
        return f"""
        <h2 class='mt-4'>Script Generated:</h2>
        <pre class='bg-light p-3 border rounded'>{generated_script}</pre>
        <a href='/' class='btn btn-secondary mt-3'>Upload Another</a>
        """
    return "Invalid file. Please upload a  .exe or .msi", 400


if __name__ == '__main__':
    app.run(debug=True)
