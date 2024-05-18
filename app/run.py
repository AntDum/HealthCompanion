from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint
from scripts.api_auth import api_auth
from scripts.api_data import api_data
from scripts.db_helpers import get_client, make_default_db
from scripts.routes import routes

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Configuration du répertoire des templates
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["TEMPLATE_FOLDER"] = "app/templates"

swagger_ui_blueprint = get_swaggerui_blueprint(
    "/swagger", "/static/swagger.json", config={"app_name": "Access API"}
)

app.register_blueprint(routes)
app.register_blueprint(swagger_ui_blueprint, url_prefix="/swagger")
app.register_blueprint(api_data, url_prefix="/api")
app.register_blueprint(api_auth, url_prefix="/auth")

if __name__ == "__main__":
    # make_default_db(True)

    app.run(debug=True)
