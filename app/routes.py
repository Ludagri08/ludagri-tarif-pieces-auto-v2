from flask import Flask, render_template, request
from .utils import rechercher_prix

app = Flask(__name__)

@app.route('/', methods=['GET'])
def client():
    reference = request.args.get('reference', '').strip()
    result = None
    if reference:
        result = rechercher_prix(reference)
    return render_template('client.html', result=result, reference=reference)

@app.route('/admin', methods=['GET'])
def admin():
    reference = request.args.get('reference', '').strip()
    result = None
    if reference:
        result = rechercher_prix(reference)
    return render_template('admin.html', result=result, reference=reference)