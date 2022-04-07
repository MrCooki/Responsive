
from flask import Flask, session, render_template, request, url_for, redirect
import settings
import hashlib
import secrets
app = Flask(__name__)

@app.route("/", methods=['GET'])
@app.route("/<settings_hash>", methods=['GET'])
def index(settings_hash = None):
    if settings_hash is not None: 
        return

    return render_template('index.html')


@app.route('/headers_settings', methods=['GET','POST'])
@app.route('/headers_settings/<settings_hash>', methods=['GET','POST'])
def headers_settings(settings_hash = None):
    if request.method == 'GET':
        if settings_hash is None:
            
            shash = hashlib.new('sha256')
            shash.update(secrets.token_bytes(32))
            return render_template('header_settings.html', headers=settings.DEFAULT_HEADERS, hash=shash.hexdigest())
        else:
            file_data = load_setings(settings_hash)
            return render_template('header_settings.html', headers=file_data, hash=settings_hash)
        
    if request.method == 'POST':
        data = request.form.getlist('header')
        configid = request.form.get('configID')
        save_settings(configid, data)
        return redirect('/headers_settings/'+ configid)


def load_setings(search_hash):

    filename = hashlib.new('sha256')
    filename.update(str.encode(search_hash))
    filename = settings.CONFIG_SAVE_LOCATION + "/" + filename.hexdigest() + ".txt"
    file_data = open(filename, 'r')
    return file_data

def save_settings(hash, data):

    filename = hashlib.new('sha256')
    filename.update(str.encode(hash))
    filename = settings.CONFIG_SAVE_LOCATION + "/" + filename.hexdigest() + ".txt"
    file_data = open(filename, 'w')
    for d in data:
        file_data.write(d+"\n")
    return 
app.run(host='0.0.0.0', port='8000', debug=True)