import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Add parent directory to Python path for building.shared (only if not in Docker)
if not os.path.exists('/app/building'):
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, parent_dir)

from flask import Flask
from flask_migrate import Migrate
from common import db
from config import DevConfig
from auth.api import auth_bp
from shared.error_handlers import register_error_handlers
from shared.middleware import log_request
from shared.middleware import *
from shared.utils import *
import threading
from handler import IAMActionHandlers


app = Flask(__name__)

auth_middleware = create_auth_middleware(
    auto_auth=True,
    public_endpoints=[
        '/auth/login',
        '/auth/register',
        '/auth/refresh-token'
    ]
)
auth_middleware.init_app(app)

# Register error handlers
register_error_handlers(app)

# Load config
app.config.from_object(DevConfig)

# Initialize SQLAlchemy
db.init_app(app)
migrate = Migrate(app, db)


# Register middleware  # ��
log_request(app)

# Global variables
rpc_server = None
rpc_thread = None


# Define RPC handlers
def handle_iam_request(request_data: dict) -> dict:
    action = request_data.get('action')
    
    handler = getattr(IAMActionHandlers, action, None)
    with app.app_context():
        try:
            if handler:
                try:
                    result = handler(request_data)
                    return result
                except Exception as e:
                    print(f"Lỗi xử lý action: {str(e)}")
                    return None
            else:
                print(f"Action không được hỗ trợ: {action}")
                return None
        except Exception as e:
            print(f"Lỗi: {str(e)}")
            return None

# Start RabbitMQ initialization
def init_rabbitmq():
    # Add RPC servers
    rpc_manager.init_app(app)
    rpc_manager.add_rpc_server_with_app('iam', 'iam_requests', handle_iam_request)

# Start RabbitMQ initialization
init_rabbitmq()

# Register blueprints
app.register_blueprint(auth_bp)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)