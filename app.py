from flask import Flask, render_template, request, redirect, url_for, jsonify
import configparser
import os

app = Flask(__name__)

CONFIG_FILE = os.path.expanduser('~/.config/wayfire.ini')

def load_config():
    config = configparser.ConfigParser(interpolation=None)  # Disable interpolation
    config.read(CONFIG_FILE)
    return config

@app.route('/')
def index():
    config = load_config()
    return render_template('index.html', config=config)

@app.route('/update_option', methods=['POST'])
def update_option():
    section = request.form['section']
    option = request.form['option']
    value = request.form['value']
    
    config = load_config()

    if section not in config.sections():
        config.add_section(section)

    config.set(section, option, value)

    try:
        with open(CONFIG_FILE, 'w') as configfile:
            config.write(configfile)
        return jsonify(status='success')
    except Exception as e:
        return jsonify(status='error', message=str(e))

if __name__ == '__main__':
    app.run(debug=True)

