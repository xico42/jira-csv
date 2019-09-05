import os

from flask import Flask, escape, request, after_this_request
from flask import render_template
from flask import request
from flask import send_file
from jira import JIRA
import tempfile

from generate_csv import load_issues, export_to_csv
from dotenv import load_dotenv

app = Flask(__name__)


@app.route('/')
def home(name=None):
    return render_template('home.html', name=name)


@app.route('/generate', methods=['POST'])
def generate_csv():
    load_dotenv()
    auth = (os.getenv('JIRA_EMAIL'), os.getenv('JIRA_API_KEY'))
    jira = JIRA(os.getenv('JIRA_URL'), basic_auth=auth)
    query = request.form["query"]

    issues = load_issues(jira, query)

    temp = tempfile.NamedTemporaryFile("w+")
    export_to_csv(issues, temp)

    @after_this_request
    def cleanup(response):
        temp.close()
        return response

    return send_file(temp.name, attachment_filename="output.csv", as_attachment=True, mimetype="text/plain")
