from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_bootstrap import Bootstrap

from scripts.routes import routes
from scripts.api_data import api_data

app = Flask(__name__)
app.secret_key = 'your_secret_key'
bootstrap = Bootstrap(app)


# Configuration du répertoire des templates
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['TEMPLATE_FOLDER'] = 'app/templates'

app.register_blueprint(routes)
app.register_blueprint(api_data)

if __name__ == '__main__':
    app.run(debug=True)