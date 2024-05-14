from flask import Flask

from scripts.routes import routes
from scripts.api_data import api_data
from scripts.api_auth import api_auth

from scripts.db_helpers import make_default_db, get_client

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configuration du répertoire des templates
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['TEMPLATE_FOLDER'] = 'app/templates'

app.register_blueprint(routes)
app.register_blueprint(api_data)
app.register_blueprint(api_auth)

if __name__ == '__main__':
    # make_default_db()
    
    app.run(debug=True)