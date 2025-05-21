from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from app.orchestrator import run_script_generation
from app.utils.installer_utils import get_installer_type

from dotenv import load_dotenv
import os
import logging

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
# --- Logging Config ---
log_path = os.path.join(os.getcwd(), 'logs', 'aipackager.log')
logging.basicConfig(
    filename=log_path,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(os.getcwd(), "app", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs('logs', exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def home():
    return render_template('upload.html')


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('installer')
    if file and file.filename.endswith(('.exe', '.msi')):
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)


        # --- Extract App Name and Version from filename ---
        base = os.path.splitext(filename)[0]
        parts = base.split('_')
        app_name = parts[0].replace('-', ' ').title()
        version = parts[1] if len(parts) > 1 else "Unknown"
        installer_type = get_installer_type(filename)

        # --- Generate Script Content ---
        script_content = run_script_generation(app_name, version, installer_type)

        # Save the script to the appropriate directory
        script_path = os.path.join('downloads', app_name, version, 'Deploy-Application.ps1')
        os.makedirs(os.path.dirname(script_path), exist_ok=True)
        with open(script_path, 'w') as script_file:
            script_file.write(script_content)

        # Provide the download link to the user
        return send_from_directory(os.path.dirname(script_path), 'Deploy-Application.ps1', as_attachment=True)

    #return code 400 if the installer tpye is wrong.
    return "Invalid file. Please upload a .exe or .msi.", 400


@app.route('/download/<app>/<version>/<filename>')
def download(app, version, filename):
    path = os.path.join('downloads', app, version)
    return send_from_directory(path, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
