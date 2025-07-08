from flask import Flask
from flask_migrate import Migrate
from iam_service.common import db
from iam_service.config import DevConfig
from iam_service.auth.api import auth_bp
from building.shared.error_handlers import register_error_handlers

app = Flask(__name__)

# Register error handlers
register_error_handlers(app)

# Load config
app.config.from_object(DevConfig)

# Initialize SQLAlchemy
db.init_app(app)
migrate = Migrate(app, db)

# Register blueprints
app.register_blueprint(auth_bp)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)