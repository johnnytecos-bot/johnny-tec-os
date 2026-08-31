from flask import Flask
from flask_cors import CORS
from routes.whatsapp_routes import whatsapp_bp
from routes.call_routes import call_bp
from routes.status_routes import status_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(whatsapp_bp)
app.register_blueprint(call_bp)
app.register_blueprint(status_bp)


@app.route("/")
def health_check():
    return {"status": "Johnny TEC OS is running"}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    
