from flask import request
import time

def log_request(app):
    @app.before_request
    def before():
        request.start_time = time.time()

    @app.after_request
    def after(response):
        duration = round(time.time() - request.start_time, 4)
        print(f"{request.method} {request.path} - {response.status_code} - {duration}s")
        return response