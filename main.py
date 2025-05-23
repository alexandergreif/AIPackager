from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from app.orchestrator import run_script_generation
from app.utils.installer_utils import get_installer_type
from app.agents.script_agent import generate_psadt_script
import uuid, os, logging

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


@app.route("/", methods=["GET", "POST"])
def upload():
    #add some functionality that the user can give his instructions to the model.
    # like providing installer details, silent switches or any config files which should be used
    #for the package. Also add maybe custom registry keys for the special Organization you are part of.
    # extract the name of the application, Version, and installer type.
    # Get the installer type by using installer_utils.py get_installer_type().
    # We work with the PackageID 0001 which is always four digits. It has to be unique
    # because we will handle the whole packaging process flow with it.

    #upload the file, get the information about the software which has been uploaded via get_installer_type
    # also maybe use a function to extract the install switches?
    #create a package request via the package request handler.

    user_instructions = ""


@app.route("/result/<packageID>")
def result(packageID):

    return render_template("result.html", script=content, id=id)


@app.route('/download/<packageID>')
def download(packageID):
    #if you visit the route with the package ID, the download for your package starts.
    path = os.path.join('downloads', app, version)
    return send_from_directory(path, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
